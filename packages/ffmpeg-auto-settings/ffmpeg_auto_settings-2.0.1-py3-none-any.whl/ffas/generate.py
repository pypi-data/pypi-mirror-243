import sys
from pathlib import Path
from magic import Magic
import shutil
from typing import Literal
from decimal import Decimal
from dataclasses import dataclass
from prettytable import PrettyTable
from .terminal import write_terminal_line
from .encoding import create_sample_encode, calculate_vmaf
from .config import Config, get_configured_sample
from .misc import ORDERED_PRESETS, get_extension_for_mimetype, print_err
from .videostore import VideoStore, Video, NoResultFound


def export_generated_encode(encode: Video) -> Literal['hardlink', 'symlink', 'copy', 'skipped']:
    """
    Export a generated encode under an informative name

    Does nothing if encode was already exported (returns "skipped")
    :param encode: sample-encode to export
    :return: the method used to export
    """
    # create directory for each sample base
    dirname = get_configured_sample().variant
    Path(dirname).mkdir(exist_ok=True)

    # build basename
    sorting_number = f'{ORDERED_PRESETS.index(encode.preset)}'  # provides better sorting in directory view
    basename = f'{sorting_number}_{encode.preset}_{encode.crf}'

    # guess extension
    mimetype = Magic(mime=True).from_file(encode.filename)
    try:
        extension = f'.{get_extension_for_mimetype(mimetype)}'
    except KeyError:
        print_err(f'Warning: mimetype {mimetype} has no known file extension')
        extension = ''

    # make paths
    source_path = Path(encode.filename)
    target_path = Path(f'{dirname}/{basename}{extension}')

    # export file in order of most convenient methods: hardlink > symlink > copy
    if target_path.is_file():
        # should be okay
        return 'skipped'
    try:
        target_path.hardlink_to(source_path)
        return 'hardlink'
    except Exception:
        try:
            target_path.symlink_to(source_path)
            return 'symlink'
        except Exception:
            shutil.copyfile(source_path, target_path)  # may ultimately raise an error
            return 'copy'


def cmd_generate(args):
    if args.min > args.max:
        sys.exit('Error: min crf is bigger than max crf')

    # create list of presets
    if args.presets:
        # use presets from args
        requested_presets = set(args.presets.split(','))
        presets = []
        for preset in requested_presets:
            if preset in ORDERED_PRESETS:
                presets.append(preset)
            else:
                print_err(f'Invalid preset: "{preset}"')
                if not preset:
                    print_err('Did you accidentally include an excess comma?')
                sys.exit(1)
    else:
        # use presets from config
        presets = [preset for preset in ORDERED_PRESETS if preset in Config()['presets']]

    # create list of crf values
    crfs = [args.min]
    while crfs[-1] + args.step_width <= args.max:
        crfs.append(crfs[-1] + args.step_width)

    generate_encodes(presets, crfs)


def cmd_generate_single(args):
    generate_encodes([args.preset], [args.crf])


def generate_encodes(presets: list[str], crfs: list[Decimal]):
    # setup
    log_lines = []
    config = Config()
    store = VideoStore()
    sample = get_configured_sample()

    # 4 newlines to push terminal output down
    print('\n\n\n')

    n_current_encode = 1
    n_total_encodes = len(presets) * len(crfs)
    exported_by_copy_at_least_once = False
    for preset in presets:
        n_current_sample_encode = 1
        for crf in crfs:
            # check if we already encoded this combination or didn't finish vmaf calculation
            try:
                existing_encode = store.get_video(
                    type='sample-encode',
                    encoder=config['encoder'],
                    preset=preset,
                    crf=crf,
                    variant=sample.variant
                )

                if existing_encode.vmaf is None:
                    write_terminal_line(-4, 'Fixing interrupted run -- calculating stray vmaf-less sample-encode')
                    calculate_vmaf(sample, existing_encode)

                # increment progress counters; export
                n_current_sample_encode += 1
                n_current_encode += 1
                try:
                    export_method = export_generated_encode(existing_encode)
                    if export_method == 'copy':
                        exported_by_copy_at_least_once = True
                except Exception as e:
                    log_lines.append(f'Unable to export file: [{e.__class__.__name__}] {str(e)}')

                # skip to next encode
                continue
            except NoResultFound:
                # the usual case, we have to create the encode first
                pass

            write_terminal_line(
                -4,
                (
                    f'Generating encode {n_current_encode}/{n_total_encodes}'
                    f' ({n_current_sample_encode}/{len(crfs)} of preset {preset})'
                )
            )

            # encode video, calculate vmaf
            encode = create_sample_encode(encoder=config['encoder'], preset=preset, crf=crf)
            calculate_vmaf(sample, encode)

            # increment progress counters; export
            n_current_sample_encode += 1
            n_current_encode += 1
            try:
                export_method = export_generated_encode(encode)
                if export_method == 'copy':
                    exported_by_copy_at_least_once = True
            except Exception as e:
                log_lines.append(f'Unable to export file: [{e.__class__.__name__}] {str(e)}')

    if exported_by_copy_at_least_once:
        log_lines.append('Warning: Had to copy instead of link files at least once')

    # show results
    show_info(sample, presets, crfs)

    if log_lines:
        print('')  # newline
        for line in log_lines:
            print(line)


@dataclass
class VideoStub:
    preset: str
    crf: Decimal
    vmaf: str = 'n/a'
    vmaf_harmonic: str = 'n/a'


def show_info(sample: Video, presets: list[str], crfs: list[Decimal]):
    store = VideoStore()
    config = Config()

    t = PrettyTable()
    t.field_names = ['preset', 'crf', 'vmaf_harmonic', 'vmaf']
    for preset in presets:
        for crf in crfs:
            try:
                encode = store.get_video(
                    type='sample-encode',
                    encoder=config['encoder'],
                    preset=preset,
                    crf=crf,
                    variant=sample.variant
                )
            except NoResultFound:
                encode = VideoStub(preset=preset, crf=crf)

            t.add_row([
                encode.preset,
                encode.crf,
                encode.vmaf_harmonic,
                encode.vmaf
            ])

    print(f'\nSample: {sample.variant}')
    print(t)
