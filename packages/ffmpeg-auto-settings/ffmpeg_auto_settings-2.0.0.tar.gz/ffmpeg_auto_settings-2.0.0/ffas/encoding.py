import datetime
import os
import shutil
import tempfile
import xml.etree.ElementTree
from decimal import Decimal
from .config import get_configured_sample, ensure_configured_sample
from .misc import run_ffmpeg_command
from .terminal import write_terminal_line, offset_terminal_height
from .videostore import Video, VideoStore


def create_sample_encode(**metadata) -> Video:
    write_terminal_line(-3, f'encode: c:v={metadata["encoder"]} preset={metadata["preset"]} crf={metadata["crf"]}')
    ensure_configured_sample()
    sample = get_configured_sample()
    store = VideoStore()
    encode = Video(type='sample-encode', variant=sample.variant, **metadata)
    # note: some sources have subtitles that can't be used with mp4, and matroska containers don't contain the
    # individual stream bitrates we use to estimate full encode sizes.
    #  -> use mp4, don't map subtitles
    cmd_line = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-stats',
        '-i', sample.filename,
        '-map', '0:v',  # only include video stream
        '-c:v', metadata['encoder'],
        '-c:a', 'copy',
        '-preset', metadata['preset'],
        '-crf', f'{metadata["crf"]:.2f}',
        '-f', 'matroska',
        encode.filename
    ]
    if metadata['encoder'] == 'libx265':
        # libx265 needs a separate parameter to suppress verbose logging
        cmd_line.insert(-1, '-x265-params')
        cmd_line.insert(-1, 'log-level=error')

    # TODO: not clearing the line before calling ffmpeg may leave residues (ffmpeg only clears the potion of its output
    #       it has previously written)
    #       clearing the line with write_terminal_line(-1, '') will cause ffmpeg to write into the next, wrong line.
    #       needs investigation.
    # write_terminal_line(-1, '')  # clear terminal line to be used by ffmpeg
    with offset_terminal_height(-1):
        start = datetime.datetime.now()
        run_ffmpeg_command(cmd_line)
        end = datetime.datetime.now()
    encode.additional = {
        'encoding-time': (end - start).total_seconds()
    }
    store.persist(encode)
    return encode


def calculate_vmaf(reference_encode: Video, distorted_encode: Video) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
        logpath = f'{tempdir}/log_path.xml'
        cmd_line = (
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-stats',
            '-i', reference_encode.filename,
            '-i', distorted_encode.filename,
            '-lavfi', (
                '[0:v]setpts=PTS-STARTPTS[reference]; '
                '[1:v]setpts=PTS-STARTPTS[distorted]; '
                f'[distorted][reference]libvmaf=log_fmt=xml:log_path={logpath}:n_threads={os.cpu_count()}'
            ),
            '-f', 'null',
            '-'
        )
        write_terminal_line(
            -3,
            f'vmaf: c:v={distorted_encode.encoder} preset={distorted_encode.preset} crf={distorted_encode.crf}'
        )
        # TODO: not clearing the line before calling ffmpeg may leave residues (ffmpeg only clears the potion of its
        #       output it has previously written)
        #       clearing the line with write_terminal_line(-1, '') will cause ffmpeg to write into the next, wrong line.
        #       needs investigation.
        # write_terminal_line(-1, '')  # clear terminal line to be used by ffmpeg
        with offset_terminal_height(-1):
            run_ffmpeg_command(cmd_line)

        if os.environ.get('FFAS_DEBUG_VMAF', None):
            # keep detailed vmaf log for debugging
            shutil.copyfile(logpath, f'{distorted_encode.filename}.vmaf.xml')

        xml_tree = xml.etree.ElementTree.parse(logpath)
        distorted_encode.vmaf = Decimal(
            xml_tree.find("./pooled_metrics/metric[@name='vmaf']").attrib['mean']
        )
        distorted_encode.vmaf_harmonic = Decimal(
            xml_tree.find("./pooled_metrics/metric[@name='vmaf']").attrib['harmonic_mean']
        )
        VideoStore().persist(distorted_encode)


def crf_is_valid(encoder, crf):
    if encoder not in ('libx264', 'libx265'):
        raise NotImplementedError('unknown encoder')
    try:
        return 0.0 <= crf <= 51.0
    except TypeError:
        return False
