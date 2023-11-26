# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import random

import pytermor as pt
from pytermor import format_auto_float

from es7s.shared import SocketMessage
from es7s.shared import CpuInfo
from ._base import _BaseIndicator, IValue
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig, RadioMenuItemConfig


class ValueCpuLoad(IValue):
    WARN_LEVEL_PERC = 95

    def __init__(self):
        super().__init__()
        self._value_perc: float|None = None
        self.state = _BoolState(
            config_var=("indicator.cpu-load", "label-current"),
            gconfig=CheckMenuItemConfig("Show current (%)", sep_before=True),
        )

    def set(self, dto: CpuInfo):
        self._value_perc = dto.load_perc
        super().set()

    @property
    def warn_level_exceeded(self) -> bool:
        if self._value_perc is None:
            return False
        return self._value_perc >= self.WARN_LEVEL_PERC

    def _format(self) -> str:
        return f"{self._value_perc:3.0f}%"

    def format_label(self) -> str | None:
        if self._value_perc is not None and (self.state or self.attention):
            return self._format() + ' '

    def format_details(self) -> str | None:
        if self._value_perc is not None:
            return self._format() + ' '


class ValueCpuLoadAvg(IValue):
    def __init__(self):
        super().__init__()
        self._values: list[float]|None = None
        self._state_off = _BoolState(
            config_var=("indicator.cpu-load", "label-average"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No average", sep_before=True, group="indicator.cpu-load"),
        )
        self._state_one = _BoolState(
            config_var=("indicator.cpu-load", "label-average"),
            config_var_value="one",
            gconfig=RadioMenuItemConfig("Show average (1min)", group="indicator.cpu-load"),
        )
        self._state_three = _BoolState(
            config_var=("indicator.cpu-load", "label-average"),
            config_var_value="three",
            gconfig=RadioMenuItemConfig("Show average (1/5/15min)", group="indicator.cpu-load"),
        )
        self.states = [
            self._state_off,
            self._state_one,
            self._state_three,
        ]

    def set(self, dto: CpuInfo):
        self._values = [*dto.load_avg]
        super().set()

    def _format_value(self, v: float) -> str:
        return format_auto_float(v, 4)

    def format_label(self) -> str | None:
        if self._values is not None:
            if self._state_one:
                return self._format_value(self._values[0])
            if self._state_three:
                return " ".join(map(self._format_value, self._values))

    def format_details(self) -> str | None:
        if self._values is not None:
            return " ".join(map(self._format_value, self._values))


class IndicatorCpuLoad(_BaseIndicator[CpuInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.cpu-load"

        self._value_cpu_load = ValueCpuLoad()
        self._value_cpu_load_avg = ValueCpuLoadAvg()

        self._freq_formatter = pt.StaticFormatter(
            pad=True,
            allow_negative=False,
            unit_separator="",
            unit="Hz",
            prefix_refpoint_shift=+2,
        )

        super().__init__(
            indicator_name="cpu-load",
            socket_topic="cpu",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(100, 95, 87, 75, 62, 50, 37, 25, 12, 0),
                subpath="cpuload",
                path_dynamic_tpl="%s.svg",
            ),
            title="CPU",
            states=[self._value_cpu_load.state, *self._value_cpu_load_avg.states],
        )
        self._title_added_cores = False

    def _render(self, msg: SocketMessage[CpuInfo]):
        if not self._title_added_cores:
            self._title_added_cores = True
            self._title_base += f"\t{msg.data.core_count} cores / {msg.data.thread_count} threads"

        self._value_cpu_load.set(msg.data)
        self._value_cpu_load_avg.set(msg.data)

        self._update_title_attention(self._value_cpu_load.warn_level_exceeded)
        self._update_details(self._format_details(msg.data))
        self._render_result(
            self._format_result(),
            icon=self._icon_selector.select(msg.data.load_perc),
        )

    def _format_result(self) -> str:
        parts = pt.filtern([
            self._value_cpu_load.format_label(),
            self._value_cpu_load_avg.format_label(),
        ])
        return " ".join(parts).rstrip()

    def _format_details(self, data: CpuInfo) -> str:
        return " ".join(pt.filtern([
            self._value_cpu_load.format_details(),
            self._value_cpu_load_avg.format_details(),
            '  @'+self._freq_formatter.format(data.freq_mhz),
        ])).rstrip()
