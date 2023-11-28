# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import importlib.resources
import typing as t
from collections.abc import Iterator
from importlib.abc import Traversable
from pathlib import Path

from es7s.shared.path import RESOURCE_PACKAGE


def get_res_dir(subpath: str|Path = None) -> Traversable:
    result = importlib.resources.files(RESOURCE_PACKAGE)
    if subpath:
        return result.joinpath(subpath)
    return result


def get_demo_highlight_num_text() -> Traversable:
    return get_res_dir(Path('demo', "demo-text.txt"))


class DemoGradients:
    @classmethod
    def iter(cls) -> Iterator[Traversable]:
        for file in get_res_dir('demo').iterdir():
            if file.name.startswith('demo-gradient'):
                yield file
