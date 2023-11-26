# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import shutil
from pathlib import Path
from typing import Iterable

import click
from click import pass_context

from .._base import Context
from .._base_opts_params import HelpPart
from ...cli._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_NONE
from ...cli._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_NONE],
    short_help="&pack &effeciency &test",
)
@cli_argument(
    "file",
    type=click.Path(allow_dash=True, resolve_path=True, path_type=Path),
    required=True,
    nargs=-1,
)
@catch_and_log_and_exit
@pass_context
class invoker:
    """
    @TODO display compress rate for a given file using a set of various archivers
    """
    FORMATS = ["zip", "rar", "gzip", "tar", "7z"]
    EXECUTABLES = {}

    def __init__(self, ctx: Context, file: Iterable[Path], **kwargs):
        self._files = [*file]
        self.run()

    def run(self):
        print(self._files)
        [print(self._get_archiver(fmt)) for fmt in self.FORMATS]

    def _find_executables(self):
        for fmt in self.FORMATS:
            if path := shutil.which(fmt):
                self.EXECUTABLES[fmt] = path

    def _get_archiver(self, fmt: str) -> str | None:
        if len(self.EXECUTABLES) == 0:
            self._find_executables()
        return self.EXECUTABLES.get(fmt, None)
