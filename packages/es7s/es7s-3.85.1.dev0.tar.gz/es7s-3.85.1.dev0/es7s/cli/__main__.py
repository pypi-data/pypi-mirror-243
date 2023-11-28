# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import sys

from ._entrypoint import invoker as entrypoint_fn


def main():
    entrypoint_fn()


def exec_():
    sys.argv.insert(1, 'exec')
    sys.orig_argv.insert(2, 'exec')  # autocompletion
    entrypoint_fn()


def monitors():
    sys.argv.insert(1, 'monitor')
    sys.argv.insert(2, 'combined')
    entrypoint_fn()

def edit_image():  # @why
    sys.argv.insert(1, 'exec')
    sys.argv.insert(2, 'edit-image')
    entrypoint_fn()


if __name__ == "__main__":
    main()
