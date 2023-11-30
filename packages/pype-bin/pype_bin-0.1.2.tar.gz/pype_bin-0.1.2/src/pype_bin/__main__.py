import argparse
import os
import pathlib
import shutil
import sys

import jinja2

from . import lib

env = jinja2.Environment(undefined=jinja2.StrictUndefined)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', nargs="*", help='execute a command')
    parser.add_argument('-n', default=False, action='store_true', help='-n')
    parser.add_argument('-l', default=False, action='store_true', help='-l')
    parser.add_argument('-a', default=False, action='store_true', help='-a')
    parser.add_argument('-F', type=str, help='-F')
    parser.add_argument('-p', default=False, action='store_true', help='-p')
    parser.add_argument('-0', '--zero', default=False, action='store_true', help='-0')

    parser.add_argument('-m', type=str, nargs="*", help='-m')
    parser.add_argument('-M', type=str, nargs="*", help='-M')

    parser.add_argument('-c', default=False, action='store_true', help='print source code only')

    return parser.parse_args()


def main():
    args = parse_args()
    template_str = (pathlib.Path(__file__).parent / 'template.py.jinja').read_text()

    with lib.subr.NamedTemporaryFifo() as filepath:
        dct = {
            'fifo_filepath': filepath if not args.c else 'tmp.fifo',
            'arg_e': args.e,
            'arg_n': args.n,
            'arg_l': args.l,
            'arg_a': args.a,
            'arg_F': args.F,
            'arg_p': args.p,
            'arg_zero': args.zero,
            'arg_m': args.m,
            'arg_M': args.M,
        }
        template = env.from_string(template_str)
        print(template.render(dct), flush=True)
        os.close(1)

        if not args.c:
            with open(filepath, 'w') as f:
                shutil.copyfileobj(sys.stdin, f)
