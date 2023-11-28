# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
import random
from collections import namedtuple
from typing import Iterable

from es7s.shared import SocketMessage
from es7s.shared import FanInfo, uconfig
from ._base import _BaseIndicator, IValue
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig


ValueRange = namedtuple("ValueRange", ["min", "max"])


class ValueFanSpeed(IValue):
    WARN_LEVEL_PERC = 96

    def __init__(self):
        super().__init__()
        self._values: list[int]|None = None
        self._value_max: int|None = None
        self._range = ValueRange(
            uconfig.get_for(self).get("value-min", int, fallback=0),
            uconfig.get_for(self).get("value-max", int, fallback=5000),
        )

        self.state = _BoolState(
            config_var=("indicator.fan-speed", "label-rpm"),
            gconfig=CheckMenuItemConfig("Show value (RPM)", sep_before=True),
        )

    def set(self, dto: FanInfo):
        self._values = dto.values_rpm
        self._value_max = dto.max()
        super().set()

    @property
    def warn_level_exceeded(self) -> bool:
        if self.value_perc is None:
            return False
        return self.value_perc >= self.WARN_LEVEL_PERC

    @property
    def value_perc(self) -> float | None:
        if self._value_max is None:
            return None
        if self._value_max == 0.0:
            return 0
        # max(1) is for displaying OFF icon only when the fans are REALLY OFF
        return max(1, 100 * (self._value_max - self._range.min) / (self._range.max - self._range.min))

    def format_label(self) -> str | None:
        if self._value_max is None:
            return None
        if self.state or self.attention:
            return str(self._value_max or "    0")

    def format_details(self) -> Iterable[str]:
        if self._values is None:
            return
        yield "\n".join(f"· {v} RPM" for v in self._values)


class IndicatorFanSpeed(_BaseIndicator[FanInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.fan-speed"
        self._value = ValueFanSpeed()

        super().__init__(
            indicator_name="fan",
            socket_topic="fan",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(96, 84, 72, 60, 48, 36, 24, 12, 1, 0),
                subpath="fan",
                path_dynamic_tpl="%s.png",
            ),
            title="Fan speed",
            states=[self._value.state],
        )

    def _render(self, msg: SocketMessage[FanInfo]):
        self._value.set(msg.data)

        self._update_title_attention(self._value.warn_level_exceeded)
        self._update_details("".join(self._value.format_details()))
        self._render_result(
            self._value.format_label() or "",
            icon=self._icon_selector.select(self._value.value_perc),
        )
