# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from functools import cached_property
from typing import Iterable

from es7s.shared import LoginsInfo, LoginInfo, SocketMessage
from ._base import _BaseIndicator, IValue
from ._icon_selector import IIconSelector, IconEnum


class LoginsIconEnum(IconEnum):
    LOGINS_2 = "2.png"
    LOGINS_3 = "3.png"
    LOGINS_4 = "4.png"
    LOGINS_5 = "5.png"
    LOGINS_6 = "6.png"
    LOGINS_7 = "7.png"
    LOGINS_8 = "8.png"
    LOGINS_9 = "9.png"
    LOGINS_9_PLUS = "9-plus.png"


class LoginsIconSelector(IIconSelector):
    def __init__(self):
        super().__init__(subpath='logins')

    def select(self, amount: int) -> IconEnum|str:
        if override := super().select():
            return override
        if amount < 2:
            return self.name_default
        if 2 <= amount <= 9:
            return LoginsIconEnum[f'LOGINS_{amount}']
        if amount > 9:
            return LoginsIconEnum.LOGINS_9_PLUS

    @cached_property
    def icon_names_set(self) -> set[str | IconEnum]:
        return set(LoginsIconEnum.list())


class ValueLogins(IValue):
    def __init__(self):
        super().__init__()
        self._value: list[LoginInfo]|None = None

    def set(self, dto: LoginsInfo):
        self._value = dto.parsed
        super().set()

    def format_label(self) -> None:
        return None

    def format_details(self) -> Iterable[str]:
        if self._value is not None:
            for login in self._value:
                yield '\t'.join([login.user, login.ip, login.dt])


class IndicatorLogins(_BaseIndicator[LoginsInfo, LoginsIconSelector]):
    def __init__(self):
        self.config_section = "indicator.logins"
        self._value = ValueLogins()

        super().__init__(
            indicator_name="logins",
            socket_topic="logins",
            icon_selector=LoginsIconSelector(),
            title="Logins",
            pseudo_hide=True,
        )

    def _render(self, msg: SocketMessage[LoginsInfo]):
        self._value.set(msg.data)
        amount = len(msg.data.parsed) + len(msg.data.raw)
        self._hidden.value = (amount == 1)
        self._update_title(self._title_base + f'\t\t{amount}', for_mgr=True)

        self._update_details(
            "\n".join([
                *self._value.format_details(),
                *msg.data.raw,
            ])
        )
        self._update_visibility()
        self._render_result("", icon=self._icon_selector.select(amount))
