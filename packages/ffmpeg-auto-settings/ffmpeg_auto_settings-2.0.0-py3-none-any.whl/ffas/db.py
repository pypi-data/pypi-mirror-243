# Copyright (C) 2023 liancea
#
# This file is part of ffmpeg-auto-settings.
#
# ffmpeg-auto-settings is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License Version 3 as published by the Free Software Foundation.
#
# ffmpeg-auto-settings is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with ffmpeg-auto-settings. If not, see
# <https://www.gnu.org/licenses/>.

import decimal
from decimal import Decimal
import sys
from typing import Optional, List
from sqlalchemy import Integer, JSON
from sqlalchemy import TypeDecorator
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy import event, create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from .misc import print_err, singleton, FFAS_PATH, generate_new_uid


SCHEMA_VERSION = 4


def type_constraint_generator(check_map: dict):
    """Create CheckConstraints tuple from limited check_map options"""
    implemented_options = {'notnull', 'isnull'}
    constraints = []
    for type, config in check_map.items():
        if not set(config).intersection(implemented_options):
            raise ValueError(f'{type} config needs one or more of: {implemented_options}')
        elif not set(config).issubset(implemented_options):
            raise ValueError(f'{type} config has unrecognized options (allowed: {implemented_options})')
        sql = f"NOT type = '{type}' OR "
        for column in config.get('isnull', {}):
            sql += f'{column} ISNULL AND '
        for column in config.get('notnull', {}):
            sql += f'{column} NOTNULL AND '
        assert sql.endswith(' AND ')
        sql = sql[:-5]
        constraints.append(CheckConstraint(sql))
    return tuple(constraints)


class Base(DeclarativeBase):
    pass


class SchemaInfo(Base):
    # schema_info should only contain a single row, this is enforced by the CheckConstraint
    __tablename__ = "schema_info"

    version: Mapped[int] = mapped_column(CheckConstraint(f"version = {SCHEMA_VERSION}"), primary_key=True)


class NormalizedDecimal(TypeDecorator):
    impl = Integer
    cache_ok = True

    def __init__(self, decimal_places):
        super().__init__()
        self.decimal_places = decimal_places

    def process_bind_param(self, value: Decimal, dialect):
        if value is None:
            return None
        try:
            # attempt to cut down to n decimal_places without loss,
            # then multiply with 10^decimal_places and cut decimal places (should be all zeroes now)
            quantized_decimal = value.quantize(
                Decimal(10) ** -self.decimal_places,
                context=decimal.Context(traps=[decimal.Inexact])
            )
            return int(quantized_decimal * (Decimal(10) ** self.decimal_places))
        except decimal.Inexact:
            raise ValueError('Decimal value is too precise to be stored in database')

    def process_result_value(self, value, dialect) -> Optional[Decimal]:
        if value is None:
            return None
        return Decimal(value) * (Decimal(10) ** -self.decimal_places)


class Video(Base):
    __tablename__ = "video"
    check_map = {  # ensure certain columns are set or not set depending on row type
        'source': {
            'isnull': ['encoder', 'preset', 'crf_e2', 'vmaf_e6', 'vmaf_harmonic_e6', 'variant']
        },
        'sample': {
            'notnull': ['variant'],
            'isnull': ['encoder', 'preset', 'crf_e2', 'vmaf_e6', 'vmaf_harmonic_e6']
        },
        'sample-encode': {
            'notnull': ['encoder', 'preset', 'crf_e2',  'variant']
        },
        'hstack': {
            'isnull': ['encoder', 'preset', 'crf_e2', 'vmaf_e6', 'vmaf_harmonic_e6', 'variant']
        },
        'full-encode': {
            'notnull': ['encoder', 'preset', 'crf_e2'],
            'isnull': ['variant']
        },
    }
    __table_args__ = (
        type_constraint_generator(check_map)
        + (UniqueConstraint('type', 'encoder', 'preset', 'crf_e2', 'variant'),)
    )
    _valid_types = ['source', 'sample', 'sample-encode', 'hstack', 'full-encode']
    _valid_types_sql = ', '.join(f"'{type}'" for type in _valid_types)

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: generate_new_uid())
    type: Mapped[str] = mapped_column(CheckConstraint(f'type in ({_valid_types_sql})'), index=True)
    encoder: Mapped[Optional[str]] = mapped_column(
        CheckConstraint("type IN (NULL, 'libx264', 'libx265')"),
        server_default=None,
        index=True
    )
    preset: Mapped[Optional[str]] = mapped_column(server_default=None, index=True)
    crf: Mapped[Optional[Decimal]] = mapped_column('crf_e2', NormalizedDecimal(2), index=True)
    vmaf: Mapped[Optional[Decimal]] = mapped_column('vmaf_e6', NormalizedDecimal(6), index=True)
    vmaf_harmonic: Mapped[Optional[Decimal]] = mapped_column('vmaf_harmonic_e6', NormalizedDecimal(6), index=True)
    variant: Mapped[Optional[str]] = mapped_column(index=True)
    additional: Mapped[Optional[dict]] = mapped_column(JSON, index=True)

    tags: Mapped[List["Tag"]] = relationship(back_populates="video", lazy="selectin")

    @property
    def filename(self):
        return str(self.path)

    @property
    def path(self):
        return FFAS_PATH / self.id

    def __init__(self, **kwargs):
        # if instantiated without id, fill in with default value
        if 'id' not in kwargs:
            value = self.__table__.c.id.default.arg
            # if default argument is callable, call it first
            if callable(value):
                value = value(None)
            kwargs['id'] = value
        super().__init__(**kwargs)


class Tag(Base):
    __tablename__ = 'tag'
    name: Mapped[str] = mapped_column(unique=True, primary_key=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("video.id"), primary_key=True)

    video: Mapped["Video"] = relationship(back_populates="tags", lazy="selectin")


@singleton
class Database:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{FFAS_PATH / 'db.sqlite3'}")
        self.Session = sessionmaker(self.engine)

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
            dbapi_connection.isolation_level = None  # autocommit mode

        @event.listens_for(self.engine, "begin")
        def do_begin(conn):
            # explicit begin when autocommiting with pysqlite
            # see https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-serializable
            conn.exec_driver_sql("BEGIN")

        self.ensure_structures()

    def ensure_structures(self):
        Base.metadata.create_all(self.engine)

        # ensure correct schema version or write it initially
        with self.Session.begin() as session:
            schema_info = session.scalars(select(SchemaInfo)).one_or_none()
            if schema_info:
                if schema_info.version != SCHEMA_VERSION:
                    print_err(f'Database schema mismatch! Required: {SCHEMA_VERSION}, found: {schema_info.version}')
                    print_err('Delete this project folder and start from scratch or install another ffas version.')
                    sys.exit(1)
            else:
                session.add(SchemaInfo(version=SCHEMA_VERSION))
