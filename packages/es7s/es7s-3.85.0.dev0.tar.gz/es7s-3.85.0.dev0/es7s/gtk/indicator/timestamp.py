# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime
import itertools
from collections.abc import Iterable
from functools import cached_property

import pytermor as pt

from es7s_commons import now
from es7s.shared import SocketMessage
from es7s.shared import TimestampInfo
from ._base import (
    _BaseIndicator,
    IValue,
)
from ._icon_selector import IIconSelector, IconEnum
from ._state import _BoolState, CheckMenuItemConfig


class TimestampModeIconEnum(IconEnum):
    DEFAULT = "default%s.png"
    NODATA = "nodata%s.png"
    OUTDATED = "outdated%s.png"
    FUTURE = "future%s.png"

    def compose(self, netcom: bool = False) -> str:
        return self.value % (["", "-nc"][netcom])


class TimestampValueIconEnum(IconEnum):
    TPL_5_MINUTES = "%s5m%s.png"
    TPL_1_HOUR = "%s1h%s.png"
    TPL_3_HOURS = "%s3h%s.png"
    TPL_1_DAY = "%s1d%s.png"

    def compose(self, negative: bool, netcom: bool) -> str:
        return self.value % (["", "-"][negative], ["", "-nc"][netcom])


class TimestampIconSelector(IIconSelector):
    def __init__(self):
        super().__init__(TimestampModeIconEnum.DEFAULT.compose(), subpath="delta")

    def select(self, now: float, remote: int | None, ok: bool, network_comm: bool = None) -> str:
        if override := super().select():
            return override

        if not ok:
            return TimestampModeIconEnum.OUTDATED.compose(network_comm)
        if not remote:
            return TimestampModeIconEnum.NODATA.compose(network_comm)

        negative = now < remote
        adiff = abs(now - remote)
        if adiff < 300:  # @TODO to config
            return TimestampValueIconEnum.TPL_5_MINUTES.compose(negative, network_comm)
        if adiff < 3600:
            return TimestampValueIconEnum.TPL_1_HOUR.compose(negative, network_comm)
        if adiff < 3 * 3600:
            return TimestampValueIconEnum.TPL_3_HOURS.compose(negative, network_comm)
        if adiff < 24 * 3600:
            return TimestampValueIconEnum.TPL_1_DAY.compose(negative, network_comm)
        if now < remote:
            return TimestampModeIconEnum.FUTURE.compose(network_comm)
        return TimestampModeIconEnum.DEFAULT.compose(network_comm)

    @cached_property
    def icon_names_set(self) -> set[str]:
        def _iter() -> Iterable[str]:
            yield from [
                tpl.compose(netcom)
                for tpl, netcom in itertools.product(
                    TimestampModeIconEnum,
                    [False, True],
                )
            ]
            yield from [
                tpl.compose(negative, netcom)
                for tpl, negative, netcom in itertools.product(
                    TimestampValueIconEnum,
                    [False, True],
                    [False, True],
                )
            ]

        return set(_iter())


class ValueTimestamp(IValue):
    def __init__(self):
        super().__init__()
        self._value_ts: int | None = None
        self._value_ok: bool = True
        self._last_formatted: str | None = None

        self.state = _BoolState(
            config_var=("indicator.timestamp", "label-value"),
            gconfig=CheckMenuItemConfig("Show value", sep_before=True),
        )
        self._formatter_label = pt.dual_registry.get_shortest()
        self._formatter_details = pt.dual_registry.get_by_max_len(6)
        self._formatter_details._allow_fractional = False  # @FIXME (?) copied from monitor

    def set(self, dto: TimestampInfo):
        self._value_ts = dto.ts
        self._value_ok = dto.ok
        # super().set()

    @property
    def _attention_delay_sec(self) -> float:
        return 60

    @property
    def value_ts(self) -> int | None:
        return self._value_ts

    def _format(self, fmter: pt.DualFormatter) -> str | None:
        if self._value_ts is not None:
            return fmter.format(now() - self._value_ts)

    def format_label(self) -> str | None:
        if self._value_ts is not None and (self.state or self.attention or not self._last_formatted):
            formatted = self._format(self._formatter_label)
            if self._last_formatted != formatted:
                self._last_formatted = formatted
                self._last_warn_ts = now()
            return formatted

    def format_details(self) -> str | None:
        if self._value_ts is not None:
            return " · ".join(
                [
                    "∆ " + self._format(self._formatter_details),
                    datetime.datetime.fromtimestamp(self._value_ts).strftime("%-e %b  %R"),
                ]
            )


class IndicatorTimestamp(_BaseIndicator[TimestampInfo, TimestampIconSelector]):
    """
    ╭──────────╮                         ╭────────────╮
    │ Δ │ PAST │                         │ ∇ │ FUTURE │
    ╰──────────╯                         ╰────────────╯
              -1h  -30min   ṇọẉ   +30min  +1h
         ▁▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁
       ⠄⠢⠲░░░░│▁│░░░░│▃│░░░░│█│░░░░│▀│░░░░│▔│░⣊⠈⣁⢉⠠⠂⠄
          ▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔
             ← 0%   +50%   +100%    │      │
                           -100%  -50%    -0% →
    """

    RENDER_INTERVAL_SEC = 1.0

    def __init__(self):
        self.config_section = "indicator.timestamp"

        self._value = ValueTimestamp()

        # self._last_remote: int = 0
        # self._invalidated_remote: int = 0

        # self._reset = _StaticState(
        #     callback=self._enqueue_reset,
        #     gconfig=MenuItemConfig("Reset remote", sep_before=False),
        # )

        super().__init__(
            indicator_name="timestamp",
            socket_topic="timestamp",
            icon_selector=TimestampIconSelector(),
            title="Remote timestamp",
            states=[
                # self._reset,
                self._value.state,
            ],
        )

    # def _enqueue_reset(self, _=None):
    #     self._enqueue(self._reset_remote)

    # def _reset_remote(self):
    #     self._invalidated_remote = self._last_remote
    #     self._update_title("")
    #     ForeignInvoker().spawn("-ic", 'remote "nalog add; nalog delete"', wait=False)

    def _render(self, msg: SocketMessage[TimestampInfo]):
        self._value.set(msg.data)
        if self._value.value_ts is None:
            self._render_result(
                "N/A", "N/A", icon=self._icon_selector.select(now(), None, True, msg.network_comm), nc=msg.network_comm,
            )
            return
        # self._last_remote = remote

        # if self._invalidated_remote:
        #     if remote != self._invalidated_remote:
        #         self._invalidated_remote = 0
        #     else:
        #         self._render_result(
        #             WAIT_PLACEHOLDER,
        #             WAIT_PLACEHOLDER,
        #             icon=self._get_icon("nodata", msg.network_comm),
        #         )
        #         return

        icon = self._icon_selector.select(
            now(),
            self._value.value_ts,
            msg.data.ok,
            msg.network_comm,
        )

        self._update_title_attention(not msg.data.ok)
        self._update_details(self._value.format_details())
        self._render_result(self._value.format_label() or "", icon=icon, nc=msg.network_comm)
