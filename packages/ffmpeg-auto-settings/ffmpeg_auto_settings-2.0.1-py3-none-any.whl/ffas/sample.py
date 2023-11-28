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

from datetime import timedelta
import tempfile
from .misc import print_err, FFmpegTimedelta, run_ffmpeg_command, get_video_duration, ensure_acceptable_ffmpeg
from .videostore import VideoStore, Video
from .config import Config


def configure_sample(sample: Video) -> None:
    """
    Configures the sample to be used by find-pairs
    :param sample: sample Video
    :raises RuntimeError: if `sample_variant` is already configured and `overwrite` is not set
    """
    if sample.type != 'sample':
        raise ValueError('Video is not a sample')
    config = Config()
    config['sample_variant'] = sample.variant
    config.write_config()


def cmd_time_based_sample(args):
    # this monstrosity calculates the number of mentioned arguments that are set (not None)
    arguments_set = sum([int(getattr(args, arg) is not None) for arg in ['length', 'scene_length', 'scene_count']])
    if arguments_set != 2:
        print_err('Error: you need to set exactly 2 out of the following 3: `length`, `scene-length`, `scene-count`')
        return 1

    # calculate the missing argument
    if args.length is None:
        scene_length = FFmpegTimedelta.from_ffmpeg_time(args.scene_length)
        scene_count = int(args.scene_count)
        length = scene_length * scene_count
    elif args.scene_length is None:
        length = FFmpegTimedelta.from_ffmpeg_time(args.length)
        scene_count = int(args.scene_count)
        scene_length = length / scene_count
    else:  # else+assert instead of elif avoids IDE detecting reference-before-assignment
        assert args.scene_count is None
        length = FFmpegTimedelta.from_ffmpeg_time(args.length)
        scene_length = FFmpegTimedelta.from_ffmpeg_time(args.scene_length)
        scene_count = length // scene_length
        length = scene_count * scene_length  # recalculate length after integer division
        if length.total_seconds() != FFmpegTimedelta.from_ffmpeg_time(args.length).total_seconds():
            print_err(
                f'Note: Recalculated effective length as {str(length)} '
                f' -> {scene_count} scenes of {str(scene_length)}'
            )

    if scene_count < 1:
        print_err('Error: `scene_count` needs to be at least 1')
        return 1
    if scene_length <= timedelta(seconds=0):
        print_err('Error: `scene_length` needs to be longer than 0s')
        return 1

    # check if ffmpeg / ffprobe are usable
    ensure_acceptable_ffmpeg()

    # determine length of source
    store = VideoStore()
    source = store.get_video(type='source')
    source_length = get_video_duration(source.filename)

    # the source will be sampled like this: gap - scene - gap - scene - gap...
    # beginning and ending in a gap. all gaps will be of equal length
    # note, however, that the length will probably be overshot because ffmpeg is setup preserve original video,
    #   which decreases the cutting accuracy
    gap_length = (source_length - (scene_count * scene_length)) / (scene_count + 1)
    scene_offsets = [gap_length + ((scene_length + gap_length) * i) for i in range(scene_count)]

    with tempfile.TemporaryDirectory() as tempdir:
        for count, offset in enumerate(scene_offsets):
            print(f'extracting scene {count} ...')
            cmd_line = (
                'ffmpeg', '-hide_banner', '-loglevel', 'warning', '-stats',
                '-ss', str(offset),
                '-t', str(scene_length),
                '-i', source.filename,
                '-c', 'copy',
                '-sn',
                f'{tempdir}/{count}.mkv'
            )
            run_ffmpeg_command(cmd_line)

        print('stitching together ...')
        with open(f'{tempdir}/concat.txt', 'w') as f:
            for count in range(scene_count):
                f.write(f"file '{tempdir}/{count}.mkv'\n")
        variant = (
            'time-based '
            f'scene_length={scene_length.total_seconds()} '
            f'scene_count={scene_count}'
        )
        sample = Video(type='sample', variant=variant)
        cmd_line = (
            'ffmpeg', '-hide_banner', '-loglevel', 'warning', '-stats',
            '-f', 'concat',
            '-safe', '0',
            '-i', f'{tempdir}/concat.txt',
            '-c', 'copy',
            '-f', 'matroska',
            sample.filename
        )
        run_ffmpeg_command(cmd_line)
        store.persist(sample)
    if args.update_config:
        configure_sample(sample)
    print('Done!')
