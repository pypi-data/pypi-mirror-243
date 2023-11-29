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

import sys
import copy
from pathlib import Path
import tomlkit
import tomlkit.items
from prettytable import PrettyTable
from magic import Magic
import shutil
from InquirerPy import inquirer
from blessings import Terminal
from .config import Config
from .videostore import VideoStore, Video, NoResultFound
from .misc import print_err, get_extension_for_mimetype


def cmd_init(args):
    try:
        Path('.ffas').mkdir()
    except FileExistsError:
        print_err('.ffas already exists (already initialized). Aborting.')
        return 1
    # initialize videostore's database
    _ = VideoStore()
    # create config (config will write its own defaults on first call)
    config = Config()
    # also call `ffas import` if video_file is specified
    if args.video_file:
        cmd_import(args)


def float_validator(result):
    try:
        float(result)
        return True
    except ValueError:
        return False


def cmd_config(args):
    if args.template_file is not None:
        apply_config_template(args.template_file)
    else:
        interactive_config()
    return 0


def deep_update(base, updates):
    def is_mapping(d):
        return isinstance(d, (dict, tomlkit.TOMLDocument, tomlkit.items.Table))

    for key in updates.keys():
        if is_mapping(updates[key]):
            # updates is a mapping here, prepare to go deeper
            if key not in base or not is_mapping(base[key]):
                # ensure base is a dict where updates already is
                base[key] = dict()
            # descend
            deep_update(base[key], updates[key])
        else:
            # updates is something else, stop recursion
            base[key] = updates[key]


def apply_config_template(template_file):
    config = Config()

    template_data = tomlkit.load(template_file)
    template_file.close()

    # we can't simply config.update(template_data), because that would effectively delete existing options not
    # defined in template_data
    deep_update(config, template_data)
    config.write_config()


def interactive_config():
    t = Terminal()
    config = Config()
    store = VideoStore()
    legal_presets = [
        'ultrafast',
        'superfast',
        'veryfast',
        'faster',
        'fast',
        'medium',
        'slow',
        'slower',
        'veryslow',
        'placebo'
    ]

    # InquirerPy should indicate if some options are out of sight; not sure how to make it do so
    print('Note: Sometimes more options are available if you scroll down.')
    print(f'{t.bold("Cancel:")} Ctrl+C | {t.bold("Confirm:")} Enter | {t.bold("Select:")} Space')

    main_menu_last = None
    crf_hint_last = None
    crf_limit_last = None
    while True:
        # TODO: maybe refactor menu actions into functions, this is quite spaghetti
        try:
            action = inquirer.select(
                'ffmpeg-auto-settings configuration',
                choices = [
                    {'name': 'Choose sample variant', 'value': 'choose-sample'},
                    {'name': 'Choose presets', 'value': 'choose-presets'},
                    {'name': 'Set target VMAF score', 'value': 'set-vmaf'},
                    {'name': 'Set tolerated VMAF delta', 'value': 'set-vmaf-delta'},
                    {'name': 'Toggle harmonic mean', 'value': 'toggle-harmonic-mean'},
                    {'name': 'Set crf hints', 'value': 'set-crf-hints'},
                    {'name': 'Set crf limits', 'value': 'set-crf-limits'},
                    {'name': 'Choose encoder', 'value': 'choose-encoder'},
                    {'name': 'Exit', 'value': 'exit'}
                ],
                default=main_menu_last
            ).execute()
        except KeyboardInterrupt:
            break
        main_menu_last = action
        match action:
            case 'choose-sample':
                samples = store.get_videos(type='sample')
                sample_variants = [sample.variant for sample in samples]
                configured_variant = config.get('sample_variant', None)

                choices = []
                for variant in [None] + sample_variants:
                    variant_text = variant if variant is not None else '(unset)'
                    if configured_variant == variant:
                        name = f'{variant_text} [current]'
                    else:
                        name = variant_text
                    choices.append({'name': name, 'value': variant})

                try:
                    selected_variant = inquirer.select(
                        'Select which sample to use for `find-pairs`',
                        choices=choices,
                        default=configured_variant
                    ).execute()
                except KeyboardInterrupt:
                    continue

                if selected_variant is None:
                    try:
                        del config['sample_variant']
                    except KeyError:
                        pass
                else:
                    config['sample_variant'] = selected_variant
                config.write_config()
            case 'choose-presets':
                try:
                    configured_presets = config['presets']
                except KeyError:
                    configured_presets = []
                choices = []
                for preset in legal_presets:
                    choices.append({'name': preset, 'value': preset, 'enabled': (preset in configured_presets)})

                def transformer(result):
                    output_ranges = []
                    range_start = None
                    for index, preset in enumerate(legal_presets + ["(end)"]):
                        # (end) element causes open ranges at the end to close
                        if preset in result and not range_start:
                            range_start = preset
                        elif preset not in result and range_start:
                            range_end = legal_presets[index-1]
                            if range_start == range_end:
                                output_ranges.append(range_start)
                            else:
                                output_ranges.append(range_start + '..' + range_end)
                            range_start = None
                    return ', '.join(output_ranges)

                try:
                    selected_presets = inquirer.checkbox(
                        'Choose presets',
                        choices=choices,
                        validate=lambda result: len(result) >= 1,
                        invalid_message='Select at least one preset!',
                        instruction='(select at least 1)',
                        transformer=transformer
                    ).execute()
                except KeyboardInterrupt:
                    continue

                config['presets'] = selected_presets
                config.write_config()
            case 'set-vmaf':
                if 'target_vmaf' in config:
                    configured_vmaf = f"{config['target_vmaf']:.6f}".rstrip('0').rstrip('.')
                else:
                    configured_vmaf = ''

                try:
                    input_vmaf = inquirer.text(
                        'Set target VMAF score',
                        default=configured_vmaf,
                        validate=float_validator,
                        instruction='(decimal number)',
                        filter=float
                    ).execute()
                except KeyboardInterrupt:
                    continue

                config['target_vmaf'] = input_vmaf
                config.write_config()
            case 'set-vmaf-delta':
                if 'vmaf_delta' in config:
                    configured_delta = f"{config['vmaf_delta']:.6f}".rstrip('0').rstrip('.')
                else:
                    configured_delta = ''

                try:
                    input_delta = inquirer.text(
                        'Set tolerated VMAF delta',
                        default=configured_delta,
                        validate=float_validator,
                        instruction='(decimal number)',
                        filter=float
                    ).execute()
                except KeyboardInterrupt:
                    continue

                config['vmaf_delta'] = input_delta
                config.write_config()
            case 'toggle-harmonic-mean':
                if 'use_harmonic_mean' in config:
                    configured_use_hm = config['use_harmonic_mean']
                else:
                    configured_use_hm = config.default_config['use_harmonic_mean']
                try:
                    choices = [
                        {'name': 'VMAF harmonic mean', 'value': True},
                        {'name': 'VMAF mean', 'value': False}
                    ]
                    input_use_hm = inquirer.select(
                        'Which metric should be used?',
                        choices=choices,
                        default=configured_use_hm
                    ).execute()
                except KeyboardInterrupt:
                    continue

                config['use_harmonic_mean'] = input_use_hm
                config.write_config()
            case 'set-crf-hints':
                if 'presets' not in config or len(config['presets']) == 0:
                    print(t.red("Cannot configure crf hints - configure presets first!"))
                    continue

                try:
                    selected_preset = inquirer.select(
                        'Select preset for which to set crf hint',
                        choices = config['presets'],
                        default=crf_hint_last
                    ).execute()
                    crf_hint_last = selected_preset
                except KeyboardInterrupt:
                    continue

                if 'crf_hints' not in config:
                    config['crf_hints'] = {}

                if selected_preset in config['crf_hints']:
                    configured_hint = f'{config["crf_hints"][selected_preset]:.2f}'
                else:
                    configured_hint = ''

                try:
                    input_hint = inquirer.text(
                        f'crf hint for {selected_preset}',
                        default=configured_hint,
                        validate=float_validator,
                        instruction='(crf, decimal number)',
                        filter=float,
                        transformer=lambda result: f'{selected_preset}={result}'
                    ).execute()
                except KeyboardInterrupt:
                    continue

                config['crf_hints'][selected_preset] = input_hint
                config.write_config()
            case 'set-crf-limits':
                crf_limit_bounds = {
                    'libx264': {
                        # libx264 could actually go up to 63 (10-bit), but this is not used or implemented on our side
                        'lower': 0.0,
                        'upper': 51.0
                    },
                    'libx265': {
                        'lower': 0.0,
                        'upper': 51.0
                    }
                }
                limit_choices = []
                for encoder in crf_limit_bounds.keys():
                    for side in ['lower', 'upper']:
                        limit_choices.append({
                            'name': f'{encoder} {side} limit',
                            'value': (encoder, side)
                        })

                try:
                    selected_limit = inquirer.select(
                        'Select limit to configure',
                        choices=limit_choices,
                        default=crf_limit_last
                    ).execute()
                    crf_limit_last = selected_limit
                except KeyboardInterrupt:
                    continue

                selected_encoder, selected_side = selected_limit
                try:
                    configured_limit = f"{config['crf_limits'][selected_encoder][selected_side]:.2f}"
                except (KeyError, TypeError):
                    configured_limit = ''

                def crf_validator(result):
                    try:
                        result = float(result)
                    except ValueError:
                        return False

                    return (
                            crf_limit_bounds[selected_encoder]['lower']
                            <= result
                            <= crf_limit_bounds[selected_encoder]['upper']
                    )

                try:
                    input_limit = inquirer.text(
                        f'crf {selected_side} limit for {selected_encoder}',
                        default=configured_limit,
                        validate=crf_validator,
                        instruction='(crf, decimal number)',
                        filter=float,
                        transformer=lambda result: f'{selected_encoder} {selected_side} limit={result}'
                    ).execute()
                except KeyboardInterrupt:
                    continue

                if 'crf_limits' not in config:
                    config['crf_limits'] = dict()
                if selected_encoder not in config['crf_limits']:
                    config['crf_limits'][selected_encoder] = dict()
                config['crf_limits'][selected_encoder][selected_side] = input_limit
                config.write_config()
            case 'choose-encoder':
                legal_encoders = ['libx264', 'libx265']
                if 'encoder' in config:
                    configured_encoder = config['encoder']
                else:
                    configured_encoder = ''

                choices = []
                for encoder in legal_encoders:
                    if configured_encoder == encoder:
                        choices.append({'name': f'{encoder} [current]', 'value': encoder})
                    else:
                        choices.append(encoder)

                try:
                    selected_encoder = inquirer.select(
                        'Choose encoder',
                        choices=choices,
                        default=configured_encoder
                    ).execute()
                except KeyboardInterrupt:
                    continue

                config['encoder'] = selected_encoder
                config.write_config()
            case 'exit':
                break
            case _:
                raise LookupError('menu choice not implemented. this is a bug.')


def cmd_import(args):
    store = VideoStore()

    if not args.video_file.is_file():
        print_err(f'{str(args.video_file)} is not a file, aborting.')

    source = Video(type='source')
    assert not (args.copy is None and args.symlink is None)
    if args.copy:
        shutil.copyfile(args.video_file, source.filename)
    elif args.symlink:
        source.path.symlink_to(args.video_file)
    else:
        source.path.hardlink_to(args.video_file)
    store.persist(source)
    store.add_tag('source', source)


def cmd_export(args):
    store = VideoStore()
    try:
        video = store.get_video(id=args.id_or_tag)
    except NoResultFound:
        try:
            video = store.get_video_by_tag(args.id_or_tag)
        except NoResultFound:
            print_err(f'Error: no encode with id or tag "{args.id_or_tag}"')
            return 1

    if not args.no_guess_ext:
        mimetype = Magic(mime=True).from_file(video.filename)
        try:
            extension = '.' + get_extension_for_mimetype(mimetype)
        except KeyError:
            print_err(f'Warning: mimetype {mimetype} has no known file extension')
            extension = ''
    else:
        extension = ''

    if args.file_name is not None:
        filename = args.file_name
    else:
        filename = args.id_or_tag

    export_path = Path(filename + extension)
    if args.copy:
        shutil.copyfile(video.filename, export_path)
    else:
        export_path.hardlink_to(video.filename)


def cmd_list(args):
    store = VideoStore()
    metadata_filter = {}
    for filter_str in args.filter:
        try:
            key, value = tuple(filter_str.split('=', maxsplit=1))
            metadata_filter[key] = value
        except ValueError:
            print_err(f'Error: filter contains no "=": {filter_str}')
            sys.exit(1)
    if 'tag' in metadata_filter:
        if len(metadata_filter) != 1:
            print_err('Warning: discarded any filters that are not `tag=`, because tag filter is present')
        try:
            found_videos = [store.get_video_by_tag(metadata_filter['tag'])]
        except NoResultFound:
            found_videos = []
    else:
        found_videos = store.get_videos(**metadata_filter)

    t = PrettyTable()
    correct_order = ['id', 'type', 'encoder', 'preset', 'crf', 'vmaf', 'variant', 'tags']
    t.field_names = correct_order
    encode_fields = copy.deepcopy(correct_order)
    encode_fields.remove('tags')
    for video in found_videos:
        new_row = [getattr(video, field) for field in encode_fields]
        new_row.append(','.join([tag.name for tag in video.tags]))
        t.add_row(new_row)
    print(t)


def cmd_version(args):
    from importlib.metadata import version
    print(f'ffmpeg-auto-settings, version {version("ffmpeg-auto-settings")}')
    print('Copyright (C) 2023 liancea')
    print('License: GNU GPLv3 <http://gnu.org/licenses/gpl.html>')

