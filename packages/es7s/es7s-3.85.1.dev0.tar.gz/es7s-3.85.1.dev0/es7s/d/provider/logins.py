# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
from collections.abc import Iterable

from ._base import DataProvider
from es7s.shared import LoginInfo, LoginsInfo, run_subprocess


class LoginsProvider(DataProvider[LoginsInfo]):
    def __init__(self):
        super().__init__("logins", "logins")

    def _collect(self) -> LoginsInfo:
        p = run_subprocess('last', '-wi', '--present=now', '--time-format=iso')  # @TODO -> `who`
        parsed = []
        raw = []
        for r in self._parse(p.stdout):
            if isinstance(r, LoginInfo):
                parsed.append(r)
            else:
                raw.append(r)
        return LoginsInfo(parsed, raw)

    def _parse(self, output: str) -> Iterable[LoginInfo|str]:
        for line in output.splitlines():
            if not ("logged in" in line or "no logout" in line):
                continue
            try:
                user, tty, ip, dt, _ = re.split(R'\s+', line, 4)
                yield LoginInfo(user, ip, dt)
            except Exception:
                yield line
