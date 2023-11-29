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

from dataclasses import dataclass
from pathlib import Path
from decimal import Decimal
from prettytable import PrettyTable
from humanize import naturalsize
from .videostore import VideoStore, NoResultFound
from .config import Config, get_configured_sample
from .misc import get_video_duration, get_video_stream_bitrate, FFmpegTimedelta, ensure_acceptable_ffmpeg


@dataclass
class VideoStub:
    preset: str
    crf: str = 'None'
    estimated_full_encode_size: str = ''  # don't show anything instead of "None" in PrettyTable
    estimated_full_encode_time: str = ''


def cmd_show_pairs(args):
    # a place to interpret args, if there were any
    # actual function is not here so it can be easily called from find-pairs
    show_pairs()


def show_pairs():
    # check if ffmpeg / ffprobe are usable
    ensure_acceptable_ffmpeg()

    store = VideoStore()
    config = Config()
    sample = get_configured_sample()

    # get source duration and video stream size
    source_duration = get_video_duration(store.get_video_by_tag('source').filename)
    source_video_stream_size = (
        get_video_stream_bitrate(store.get_video_by_tag('source').filename)
        * int(source_duration.total_seconds())
        / 8
    )

    results = [
        VideoStub('(source)', '', naturalsize(source_video_stream_size, binary=True))
    ]
    for preset in config['presets']:
        try:
            vmaf_max = Decimal(config['target_vmaf'] + config['vmaf_delta']).quantize(Decimal('1.00'))
            sample_encode = store.get_sample_encode_in_vmaf_range(
                config['encoder'],
                preset,
                sample,
                vmaf_min=config['target_vmaf'],
                vmaf_max=vmaf_max,
                use_harmonic=config['use_harmonic_mean']
            )

            # add info derived from file
            size_estimation = (
                Path(sample_encode.filename).stat().st_size
                * source_duration.total_seconds()
                / get_video_duration(sample_encode.filename).total_seconds()
            )
            sample_encode.estimated_full_encode_size = naturalsize(size_estimation, binary=True)

            time_estimation = (
                source_duration.total_seconds()
                / get_video_duration(sample_encode.filename).total_seconds()
                * float(sample_encode.additional['encoding-time'])
            )
            sample_encode.estimated_full_encode_time = str(FFmpegTimedelta(seconds=int(time_estimation)))

            results.append(sample_encode)
        except NoResultFound:
            results.append(VideoStub(preset=preset))

    t = PrettyTable()
    t.field_names = ['preset', 'crf', 'est. full length video size', 'est. full length encoding time']
    for video in results:
        t.add_row([
            video.preset,
            video.crf,
            video.estimated_full_encode_size,
            video.estimated_full_encode_time
        ])

    print(f'Sample: {sample.variant}')
    print(f"VMAF Range: {config['target_vmaf']} (+{config['vmaf_delta']})")
    print(t)
