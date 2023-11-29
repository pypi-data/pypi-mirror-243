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

import argparse
from pathlib import Path
from decimal import Decimal
import sys
from . import basic, sample, find_pairs, show_pairs, generate
from .misc import print_err, ORDERED_PRESETS


parser = argparse.ArgumentParser(
    prog='ffas',
    description='ffmpeg-auto-settings - various ffmpeg video encoding helpers'
)
subparsers = parser.add_subparsers(required=True, dest='subcommand', metavar='subcommand')

# command: init
p_init = subparsers.add_parser(
    'init',
    help='initialize the current directory for use with ffas'
)
p_init.add_argument('video_file', type=Path, nargs='?', help='path to source video (as in `ffas import`)')
p_init_group = p_init.add_mutually_exclusive_group()
p_init_group.add_argument('-c', '--copy', action='store_true', help='copy instead of hardlink (as in `ffas import`)')
p_init_group.add_argument('-s', '--symlink', action='store_true', help='symlink instead of hardlink (as in `ffas import`)')

# command: config
p_config = subparsers.add_parser(
    'config',
    help='configure (default) encoding parameters'
)
p_config_group = p_config.add_mutually_exclusive_group()
p_config_group.add_argument('-i', '--interactive', action='store_true', help='run interactive configuration (default)')
p_config_group.add_argument('-f', '--template-file', type=argparse.FileType('r'), help='apply options from toml TEMPLATE_FILE to current configuration')

# command: import
p_import = subparsers.add_parser(
    'import',
    help='Import a video file as source'
)
p_import.add_argument('video_file', type=Path, help='path to source video')
p_import_group = p_import.add_mutually_exclusive_group()
p_import_group.add_argument('-c', '--copy', action='store_true', help='copy instead of hardlink')
p_import_group.add_argument('-s', '--symlink', action='store_true', help='symlink instead of hardlink')

# command: time-based-sample, tbs
long_help = 'Creates a sample from multiple scenes determined by (approx.) evenly distributed timespans'
for p_command, p_help in [('time-based-sample', long_help), ('tbs', 'alias for time-based-sample')]:
    p_time_based_sample = subparsers.add_parser(
        p_command,
        help=p_help,
        description='You need to supply exactly two arguments out of `length`, `scene-length` and `scene-count`.'
    )
    p_time_based_sample.add_argument('-l', '--length', help='target length of full sample')
    p_time_based_sample.add_argument('-t', '--scene-length', help='length of each scene')
    p_time_based_sample.add_argument('-c', '--scene-count', type=int, help='how many scenes to extract')
    p_time_based_sample.add_argument(
        '-n', '--no-update-config', dest='update_config', action='store_false',
        help="don't update 'sample_variant' config afterwards"
    )

# command: export
p_export = subparsers.add_parser('export', help='make internally stored encode available under custom name')
p_export.add_argument('-n', '--no-guess-ext', action='store_true',
                      help="don't attempt to guess an appropriate file extension")
p_export.add_argument('-c', '--copy', action='store_true', help='copy instead of hardlink')
p_export.add_argument('id_or_tag', help='encode id or tag name')
p_export.add_argument('file_name', nargs='?', help='filename to export encode to')

# command: list
p_list = subparsers.add_parser('list', help='list all known encodes')
p_list.add_argument('filter', nargs='*', help='metadata filter(s) in the form `key=value`')

# command: find-pairs
p_find_pairs = subparsers.add_parser(
    'find-pairs',
    help='find crf/preset pairs resulting in roughly the same VMAF score'
)
p_find_pairs.add_argument(
    '-t', '--crf-hints', action='store_true',
    help='use results to preseed crf hints for next run, possibly with a longer sample'
)

# command: show-pairs, show
long_help = 'show crf/preset pairs discovered in `find-pairs`'
for p_command, p_help in [('show-pairs', long_help), ('show', 'alias for show-pairs')]:
    subparsers.add_parser(p_command, help=p_help)

# command: generate
p_generate = subparsers.add_parser(
    'generate',
    help='generate multiple sample-encodes',
    description='Encodes are generated for the currently configured presets, unless you specify --presets explicitly.'
)
p_generate.add_argument('-n', '--min', required=True, type=Decimal, help='minimum crf')
p_generate.add_argument('-x', '--max', required=True, type=Decimal, help='maximum crf')
p_generate.add_argument('-s', '--step-width',
                        required=True,
                        type=Decimal,
                        help='generate one encode every <step-width> crf'
                        )
p_generate.add_argument('-p', '--presets', help='(optional) comma-separated list of presets')

# command: generate-single
p_generate_single = subparsers.add_parser(
    'generate-single',
    help='generate a single sample-encode'
)
p_generate_single.add_argument('-p', '--preset',
                               required=True,
                               type=lambda s: s.lower(),
                               choices=ORDERED_PRESETS,
                               help='preset'
                               )
p_generate_single.add_argument('-c', '--crf', required=True, type=Decimal, help='crf')

# command: version
p_version = subparsers.add_parser('version', help='show version and license info')

# parse arguments and run
args = parser.parse_args()
command_map = {
    'init': basic.cmd_init,
    'import': basic.cmd_import,
    'config': basic.cmd_config,
    'time-based-sample': sample.cmd_time_based_sample,
    'tbs': sample.cmd_time_based_sample,
    'export': basic.cmd_export,
    'list': basic.cmd_list,
    'find-pairs': find_pairs.cmd_find_pairs,
    'show-pairs': show_pairs.cmd_show_pairs,
    'show': show_pairs.cmd_show_pairs,
    'generate': generate.cmd_generate,
    'generate-single': generate.cmd_generate_single,
    'version': basic.cmd_version
}
if args.subcommand not in ('init', 'version'):
    if not Path('.ffas').is_dir():
        print_err('Not inside a ffas project (.ffas directory was not found).')
        print_err('To start a new project, create an empty directory, `cd` into it and run `ffas init [<file>]`')
        sys.exit(1)

sys.exit(command_map[args.subcommand](args))
