# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from abc import ABCMeta
from collections.abc import Iterable

import pytermor as pt
from pytermor import format_auto_float

from es7s_commons import pt_
from es7s.shared import SocketMessage
from es7s.shared import MemoryInfo, uconfig
from es7s.shared import get_merged_uconfig
from ._base import (
    _BaseIndicator,
    IValue,
)
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig, RadioMenuItemConfig


class ValueMemory(IValue, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self._value_used_bytes: int | None = None
        self._value_total_bytes: int | None = None

    @property
    def value_used_ratio(self) -> float:
        return self._value_used_bytes / self._value_total_bytes

    @property
    def value_used_perc(self) -> float:
        return 100 * self.value_used_ratio

    def _format_used_perc(self) -> str:
        return f"{self.value_used_perc:3.0f}% "

    def _format_bytes(self, short: bool, total=False) -> str:
        value_b = [self._value_used_bytes, self._value_total_bytes][total]
        value_kb = value_b / 1024
        value_mb = value_b / 1024**2
        value_gb = value_b / 1024**3
        if short:
            return pt.format_auto_float(value_gb, 3) + "G"

        if value_kb < 1:
            return "< 1k"
        if value_kb < 1000:
            return format_auto_float(value_kb, 4, False) + "k"
        if value_mb < 10000:
            return format_auto_float(value_mb, 4, False) + "M"
        return format_auto_float(value_gb, 4, False) + "G"


class ValueMemoryPhys(ValueMemory):
    def __init__(self):
        super().__init__()
        self._warn_ratio: float | None = uconfig.get_for(self).get(
            "physical-warn-level-ratio", float
        )

        self._state_perc = _BoolState(
            config_var=("indicator.memory", "label-physical-percents"),
            gconfig=CheckMenuItemConfig("Show physical (%)", sep_before=True),
        )
        self._state_bytes_none = _BoolState(
            config_var=("indicator.memory", "label-physical-bytes"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig(
                "No physical abs. value", sep_before=True, group="indicator.memory"
            ),
        )
        self._state_bytes_dynamic = _BoolState(
            config_var=("indicator.memory", "label-physical-bytes"),
            config_var_value="dynamic",
            gconfig=RadioMenuItemConfig("Show physical (kB/MB/GB)", group="indicator.memory"),
        )
        self._state_bytes_short = _BoolState(
            config_var=("indicator.memory", "label-physical-bytes"),
            config_var_value="short",
            gconfig=RadioMenuItemConfig("Show physical (GB)", group="indicator.memory"),
        )
        self.states = [
            self._state_perc,
            self._state_bytes_none,
            self._state_bytes_dynamic,
            self._state_bytes_short,
        ]

    @property
    def warn_level_exceeded(self) -> bool:
        if self._warn_ratio is None:
            return False
        return self.value_used_ratio >= self._warn_ratio

    def set(self, dto: MemoryInfo):
        self._value_used_bytes = dto.phys_used
        self._value_total_bytes = dto.phys_total
        super().set()

    def format_label(self) -> Iterable[str]:
        if self._value_used_bytes is None or self._value_total_bytes is None:
            return
        if self._state_perc or self.attention:
            yield self._format_used_perc()

        if self._state_bytes_short:
            yield self._format_bytes(short=True)
        elif self._state_bytes_dynamic:
            yield self._format_bytes(short=False)

    def format_details(self) -> Iterable[str]:
        yield "Phys."
        if self._value_used_bytes is None or self._value_total_bytes is None:
            yield "---"
            return
        yield self._format_used_perc()
        yield self._format_bytes(short=False) + " / " + self._format_bytes(short=False, total=True)


class ValueMemorySwap(ValueMemory):
    def __init__(self):
        super().__init__()
        self._warn_ratio: float | None = uconfig.get_for(self).get("swap-warn-level-ratio", float)
        self._state_perc = _BoolState(
            config_var=("indicator.memory", "label-swap-percents"),
            gconfig=CheckMenuItemConfig("Show swap (%)", sep_before=True),
        )
        self._state_bytes = _BoolState(
            config_var=("indicator.memory", "label-swap-bytes"),
            gconfig=CheckMenuItemConfig("Show swap (kB/MB/GB)"),
        )
        self.states = [self._state_perc, self._state_bytes]

    @property
    def warn_level_exceeded(self) -> bool:
        if self._warn_ratio is None:
            return False
        return self.value_used_ratio >= self._warn_ratio

    def set(self, dto: MemoryInfo):
        self._value_used_bytes = dto.swap_used
        self._value_total_bytes = dto.swap_total
        super().set()

    def format_label(self) -> Iterable[str]:
        if self._value_used_bytes is None or self._value_total_bytes is None:
            return
        if self._state_perc or self.attention:
            yield self._format_used_perc()
        if self._state_bytes:
            yield self._format_bytes(short=False)

    def format_details(self) -> Iterable[str]:
        yield "Swap"
        if self._value_used_bytes is None or self._value_total_bytes is None:
            yield "---"
            return
        yield self._format_used_perc()
        yield self._format_bytes(short=False) + " / " + self._format_bytes(short=False, total=True)


class IndicatorMemory(_BaseIndicator[MemoryInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.memory"

        self._value_phys = ValueMemoryPhys()
        self._value_swap = ValueMemorySwap()

        super().__init__(
            indicator_name="memory",
            socket_topic="memory",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(100, 95, *range(90, -10, -10)),
                subpath="memory",
                path_dynamic_tpl="%s.svg",
            ),
            title="RAM",
            states=[*self._value_phys.states, *self._value_swap.states],
        )

    def _render(self, msg: SocketMessage[MemoryInfo]):
        self._value_phys.set(msg.data)
        self._value_swap.set(msg.data)

        self._update_details(self._format_details())

        self._render_result(
            self._format_label(),
            icon=self._icon_selector.select(self._value_phys.value_used_perc),
        )

    def _format_label(self):
        parts = pt.filtern(
            [
                *self._value_phys.format_label(),
                *self._value_swap.format_label(),
            ]
        )
        return " ".join(parts).rstrip()

    def _format_details(self) -> str:
        parts = pt_.filtere(
            [
                "\t".join(self._value_phys.format_details()),
                "\t".join(self._value_swap.format_details()),
            ]
        )
        return "\n".join(parts).rstrip()
