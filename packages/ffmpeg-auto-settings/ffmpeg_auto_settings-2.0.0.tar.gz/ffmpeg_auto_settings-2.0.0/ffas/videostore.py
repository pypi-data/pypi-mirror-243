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

from .misc import singleton
from typing import Type, TypeVar, List
from decimal import Decimal
from .db import Database, Video, Tag
from sqlalchemy import select
# noinspection PyUnresolvedReferences
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


@singleton
class VideoStore:
    def __init__(self):
        self.db: Database = Database()

    def validate_files(self):
        # TODO:
        #   - ensure database entries are (still) backed by files
        #   - check for stray files that are not known to the database
        #   - check if file modify timestamps make sense (files that can only be created in a later step should have
        #     a later timestamp --> may uncover implementation bugs
        raise NotImplementedError

    def persist(self, obj: Video | Tag) -> None:
        """
        Persist new objects or changes to objects
        :param obj: Video or Tag
        """
        with self.db.Session() as session:
            session.merge(obj)
            session.commit()
            session.expunge_all()

    def delete(self, obj: Video | Tag) -> None:
        """
        Delete a Video or Tag

        Can actually delete other mapped objects, but that should not be useful.
        :param obj: Video or Tag object
        """
        with self.db.Session() as session:
            session.delete(obj)
            session.commit()

    VideoOrTag = TypeVar('VideoOrTag', Video, Tag)

    def get(
            self,
            cls: Type[VideoOrTag],
            multiple: bool = False, **fields
    ) -> VideoOrTag | List[VideoOrTag]:
        """
        Get Video or Tag object(s) matching fields

        Examples:
         - get(Video, type='source')
         - get(Video, type='sample-encode', variant='time-based scene_length=10 scene_count=3')
         - get(Tag, name='sometag')
        :param cls: Video or Tag
        :param multiple: If True, return results as list instead of a single object (may be empty)
        :param fields: filter by these attribute values
        :return: Video object, or a list of Video objects if `multiple` is True (may be empty)
        :raise AttributeError if a metadata key is not a valid Video attribute
        :raise NoResultFound if no results were found and `multiple` is False
        :raise MultipleResultsFound if more than one result was found and `multiple` is False
        """
        with self.db.Session() as session:
            query = select(cls)
            for key, value in fields.items():
                query = query.where(getattr(cls, key) == value)
            scalars = session.scalars(query)
            if multiple:
                result = scalars.all()
            else:
                result = scalars.one()
            session.expunge_all()
        return result

    def get_video_by_tag(self, tag_name: str) -> Video:
        """
        Get Video referenced by tag. Same as get(Tag, name=tag_name).video

        :param tag_name: tag name
        :return: Video
        """
        return self.get(Tag, name=tag_name).video

    def get_video(self, **fields) -> Video:
        """
        Get single Video matching fields. Same as get(Video, multiple=False, **fields)
        """
        return self.get(Video, multiple=False, **fields)

    def get_videos(self, **fields) -> List[Video]:
        """
        Get list of videos with matching fields. Same as get(Video, multiple=True, **fields)
        """
        return self.get(Video, multiple=True, **fields)

    def get_sample_encode_in_vmaf_range(
            self,
            encoder: str,
            preset: str,
            sample: Video,
            vmaf_min: float,
            vmaf_max: float,
            use_harmonic: bool
    ) -> Video:
        """
        Get Sample encode in vmaf target range

        :param encoder: Video.encoder value
        :param preset: Video.preset value
        :param sample: Associated sample
        :param vmaf_min: Minimal vmaf (numeric)
        :param vmaf_max: Maximum vmaf (numeric)
        :param use_harmonic: Whether to lookup harmonic mean
        :return: sample encode matching the criteria above
        :raise NoResultFound if no sample encodes matched
        """
        # convenience cast decimals in arguments
        vmaf_min = Decimal(vmaf_min)
        vmaf_max = Decimal(vmaf_max)

        # search for correct metric
        if use_harmonic:
            vmaf_attr = 'vmaf_harmonic'
        else:
            vmaf_attr = 'vmaf'

        with self.db.Session() as session:
            query = (
                select(Video)
                .where(Video.encoder == encoder)
                .where(Video.preset == preset)
                .where(Video.variant == sample.variant)
                .where(getattr(Video, vmaf_attr) >= vmaf_min)
                .where(getattr(Video, vmaf_attr) <= vmaf_max)
                .order_by(getattr(Video, vmaf_attr).asc())
                .limit(1)
            )
            result = session.scalars(query).one()
            session.expunge_all()
        return result

    def get_all_tags(self) -> List[Tag]:
        """
        Get all known tags. Same as get(Tag, multiple=True)
        """
        return self.get(Tag, multiple=True)

    def add_tag(self, tag_name: str, video: Video, replace: bool = False) -> None:
        """
        Add a tag to a Video
        :param tag_name: tag name
        :param video: Video
        :param replace: If True, replace any existing tags with that name
        """
        with self.db.Session() as session:
            if replace:
                try:
                    session.delete(self.get(Tag, name=tag_name))
                except NoResultFound:
                    pass
            new_tag = Tag(name=tag_name, video_id=video.id)
            session.add(new_tag)
            session.commit()

    def delete_tag(self, name: str) -> None:
        """
        Delete a tag by its name
        :param name: tag name
        :raise NoResultFound if no tag by that name exists
        """
        with self.db.Session() as session:
            tag = self.get(Tag, name=name)
            session.delete(tag)
            session.commit()
