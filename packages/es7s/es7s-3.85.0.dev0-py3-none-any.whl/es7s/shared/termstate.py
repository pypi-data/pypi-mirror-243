# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from logging import getLogger

import pytermor as pt

from .io_ import IoProxy, get_stdout
from es7s_commons import TerminalState


class ProxiedTerminalState(TerminalState):
    def __init__(self, io_proxy: IoProxy = None):
        self._io_proxy: IoProxy = io_proxy or get_stdout()
        super().__init__()
        self._io = None

    def assign_proxy(self, io_proxy: IoProxy):
        self._io_proxy = io_proxy
        getLogger(__package__).debug(f"TSC: Switched to {self._io_proxy}")

    def _echo(self, sequence: pt.ISequence):
        self._io_proxy.echo(sequence, bypass=True)  # do not allow to intercept and buffer these

    def _is_a_tty(self):
        return self._io_proxy.io.isatty()
