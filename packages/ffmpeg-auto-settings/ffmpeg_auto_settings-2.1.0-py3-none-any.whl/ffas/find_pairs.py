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

import time
import sys
from blessings import Terminal
from decimal import Decimal
from typing import Literal
from .config import Config, get_configured_sample, ensure_configured_sample
from .encoding import create_sample_encode, calculate_vmaf, crf_is_valid
from .terminal import write_terminal_line
from .videostore import VideoStore
from .misc import ORDERED_PRESETS, ensure_acceptable_ffmpeg
from .show_pairs import show_pairs


def ensure_configured_target_vmaf() -> None:
    if 'target_vmaf' not in Config():
        sys.exit('You need to set a target_vmaf first! (`ffas config`)')


class NoCRFCandidateInLimits(Exception):
    pass


def get_configured_limit(encoder, side):
    try:
        configured_limit = Config()['crf_limits'][encoder][side]
        if not crf_is_valid(encoder, configured_limit):
            raise RuntimeError(
                f'Configured {side} limit for {encoder} is out of bounds or invalid: {configured_limit:.2f}'
            )
        return configured_limit
    except KeyError:
        # no limit configured
        return 0.0 if side == 'lower' else 51.0


def guess_next_crf(encoder, current_crf, direction: Literal['lower', 'higher'], step_width) -> Decimal:
    if direction == 'lower':
        limit = get_configured_limit(encoder, 'lower')
        next_crf = max(limit, current_crf - step_width)
        if next_crf >= current_crf:
            raise NoCRFCandidateInLimits
    elif direction == 'higher':
        limit = get_configured_limit(encoder, 'upper')
        next_crf = min(limit, current_crf + step_width)
        if next_crf <= current_crf:
            raise NoCRFCandidateInLimits
    else:
        raise NotImplementedError('unknown direction')

    return Decimal(next_crf)


def cmd_find_pairs(args):
    log_lines = []  # contains useful info that should not disappear while searching

    # ensure we are prepared (have usable ffmpeg, configured target vmaf, generated sample)
    ensure_acceptable_ffmpeg()
    ensure_configured_target_vmaf()
    ensure_configured_sample()
    sample = get_configured_sample()

    config = Config()
    store = VideoStore()
    encoder = config['encoder']
    configured_metric = 'vmaf_harmonic' if config['use_harmonic_mean'] else 'vmaf'
    # read enabled presets and sort them - fastest to slowest
    presets = []
    for preset in ORDERED_PRESETS:
        if preset in config['presets']:
            presets.append(preset)
    print('\n\n\n')  # print 4 newlines to make room for stats
    for preset_count, preset in enumerate(presets):
        write_terminal_line(-5, f'Analyzing preset {preset} ({preset_count + 1}/{len(presets)})')

        # recover from interrupted run: look for encodes without vmaf score
        unrated_encodes = store.get_videos(
            type='sample-encode',
            encoder=encoder,
            preset=preset,
            variant=sample.variant,
            vmaf=None
        )
        for unrated_encode in unrated_encodes:
            write_terminal_line(-4, 'Fixing interrupted run -- calculating stray vmaf-less sample-encode')
            calculate_vmaf(get_configured_sample(), unrated_encode)

        # decrease step width if we can work with hints
        try:
            use_hints = preset in config['crf_hints']
        except KeyError:
            # crf_hints key may not exist
            use_hints = False
        if use_hints:
            step_width = 0.5
        else:
            step_width = 2

        encodes = store.get_videos(type='sample-encode', encoder=encoder, preset=preset, variant=sample.variant)
        if len(encodes) == 0:
            # no known encodes for this preset
            if use_hints:
                # round crf from config to two decimal places. tomlkit does weird stuff otherwise
                crf = Decimal(config['crf_hints'][preset]).quantize(Decimal('1.00'))
                write_terminal_line(-4, f'No known pairs for this preset, starting with hint crf={crf}')
            else:
                crf = Decimal(23) if encoder == 'libx264' else Decimal(28)
                write_terminal_line(-4, f'No known pairs for this preset, starting to guess at crf={crf}')

            if not get_configured_limit(encoder, 'lower') < crf < get_configured_limit(encoder, 'upper'):
                # We could try to find some sensible starting point by picking something inside limits, but considering
                # the default crf is somewhat sensible and the crf hints should be a good approximation already,
                # it's more likely that the limits are misconfigured.
                # crf limits are mainly used as runaway protection anyway
                log_lines.append(f'Initial guess of crf={crf} for {preset} is outside configured limits!')
                log_lines.append("Make sure your encoder's default crf (or your crf hints) are within limits.")
                continue
            new_encode = create_sample_encode(encoder=encoder, preset=preset, crf=crf)
            calculate_vmaf(get_configured_sample(), new_encode)
            encodes.append(new_encode)

        target_vmaf = config['target_vmaf']
        vmaf_delta = config['vmaf_delta']
        encodes = sorted(encodes, key=lambda encode: encode.vmaf)
        i = 0
        immediate_find = True
        while True:
            try:
                encode = encodes[i]
            except IndexError:
                # search exhausted list without finding an encode with vmaf >= target_vmaf
                immediate_find = False
                try:
                    # guess next crf decreasing from previous, which is not good enough
                    crf = guess_next_crf(encoder, encodes[i-1].crf, 'lower', step_width)
                except NoCRFCandidateInLimits:
                    log_lines.append(f'Cannot find low enough crf for {preset} within valid or configured bounds!')
                    break
                write_terminal_line(
                    -4,
                    (
                        'Increasing quality ('
                        f'crf={encodes[i - 1].crf:.2f}'
                        f' --> vmaf={getattr(encodes[i - 1], configured_metric):.2f}'
                        f' < {target_vmaf:.2f}'
                        ')'
                    )
                )
                new_encode = create_sample_encode(encoder=encoder, preset=preset, crf=crf)
                calculate_vmaf(get_configured_sample(), new_encode)
                encodes.append(new_encode)
                continue

            if target_vmaf <= getattr(encode, configured_metric) <= target_vmaf + vmaf_delta:
                # found proper candidate
                write_terminal_line(-4, f'Found encode in range {target_vmaf:.2f} +{vmaf_delta:.2f}')
                write_terminal_line(-3, f'crf: {encode.crf}')
                write_terminal_line(-2, '')
                if not immediate_find:
                    time.sleep(1)

                # write crf hint if requested
                if args.crf_hints:
                    if 'crf_hints' not in config:
                        config['crf_hints'] = dict()
                    config['crf_hints'][preset] = float(encode.crf)
                    config.write_config()
                break

            if getattr(encode, configured_metric) < target_vmaf:
                # search through list, pick next encode if found vmaf not high enough
                i += 1
            else:
                # searched through list, found vmaf is high enough, but too high (otherwise we had a proper
                # candidate, see above)
                if i == 0:
                    # usually, we'd try to bisect the next crf value. if i=0, there is no smaller crf neighbor to work
                    # with, so we need to create a smaller neighbor
                    immediate_find = False
                    write_terminal_line(
                        -4,
                        (
                            'Decreasing quality ('
                            f'crf={encodes[i - 1].crf:.2f}'
                            f' ↦ vmaf={getattr(encodes[i - 1], configured_metric):.2f}'
                            f' > {target_vmaf:.2f}'
                            ')'
                        )
                    )
                    try:
                        # guess next crf decreasing from current, which is too good
                        crf = guess_next_crf(encoder, encodes[i].crf, 'higher', step_width)
                    except NoCRFCandidateInLimits:
                        log_lines.append(f'Cannot find high enough crf for {preset} within valid or configured bounds!')
                        break
                else:
                    immediate_find = False
                    write_terminal_line(
                        -4,
                        (
                            'Bisecting quality ('
                            f'crf {encodes[i-1].crf:.2f} ↦ {getattr(encodes[i-1], configured_metric):.4f}'
                            f' < {target_vmaf:.4f}'
                            f' < crf {encode.crf:.2f} ↦ {getattr(encode, configured_metric):.4f}'
                            ')'
                        )
                    )
                    crf = encodes[i-1].crf + ((encode.crf - encodes[i-1].crf) / 2)  # guess crf through bisection
                    crf = round(crf, 2)  # round to two decimal places
                    if not (get_configured_limit(encoder, 'lower') <= crf <= get_configured_limit(encoder, 'upper')):
                        # a bisected crf out of configured bounds should only occur if you work on existing find-pairs
                        # searches and change the limits afterwards
                        log_lines.append(f'crf solution for {preset} is inside valid, but outside configured limits!')
                    if crf in (encodes[i-1].crf, encodes[i].crf):
                        # Bisected crf value was already calculated, so we're not working precise enough (bug) or
                        # user searches an unsensibly specific vmaf value
                        log_lines.append(f"Cannot pinpoint crf for {preset}! Is the vmaf_delta set too tight?")
                        break
                new_encode = create_sample_encode(encoder=encoder, preset=preset, crf=crf)
                calculate_vmaf(get_configured_sample(), new_encode)
                encodes.insert(i, new_encode)

    # move terminal cursor to bottom, then add newlines to not overwrite things
    term = Terminal()
    term.location(0, term.height)
    print('\n\n')  # newlines

    # flush log lines
    for line in log_lines:
        print(line)

    # show results
    show_pairs()
