from contextlib import contextmanager
from blessings import Terminal


@contextmanager
def offset_terminal_height(bottom_offset):
    # TODO: anchor to starting line, not bottom (also in write_terminal_line)
    term = Terminal()
    with term.location(0, term.height + bottom_offset):
        yield


def write_terminal_line(bottom_offset, print_str):
    # cut off print_str to terminal width, then fill it up with spaces to fully overwrite previous prints in this line
    term = Terminal()
    terminal_width = term.width
    print_str = print_str[:terminal_width]
    print_str = print_str.ljust(terminal_width)
    with offset_terminal_height(bottom_offset):
        print(print_str)
