# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from typing import Iterable

from pytermor import fit

from es7s.shared import SocketMessage
from es7s.shared import TemperatureInfo
from ._base import _BaseIndicator, IValue
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, RadioMenuItemConfig


class ValueTemperature(IValue):
    WARN_LEVEL_C = 80

    def __init__(self):
        super().__init__()
        self._values_sorted: list[tuple[str, float]]|None = None
        self._values_str: list[str]|None = None
        self._value_max_c: float|None = None

        self._state_none = _BoolState(
            config_var=("indicator.temperature", "label"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No label", sep_before=True, group="indicator.temperature"),
        )
        self._state_one = _BoolState(
            config_var=("indicator.temperature", "label"),
            config_var_value="one",
            gconfig=RadioMenuItemConfig("Show 1 sensor (°C)", group="indicator.temperature"),
        )
        self._state_three = _BoolState(
            config_var=("indicator.temperature", "label"),
            config_var_value="three",
            gconfig=RadioMenuItemConfig("Show 3 sensors (°C)", group="indicator.temperature"),
        )
        self.states = [
            self._state_none,
            self._state_one,
            self._state_three,
        ]

    @property
    def warn_level_exceeded(self) -> bool:
        if self._value_max_c is None:
            return False
        return self._value_max_c >= self.WARN_LEVEL_C

    @property
    def value_max_c(self) -> float|None:
        return self._value_max_c

    def set(self, dto: TemperatureInfo):
        self._values_sorted = sorted(dto.values_c, key=lambda v: v[1], reverse=True)

        self._value_max_c = 0
        if len(self._values_sorted) > 0:
            self._value_max_c = self._values_sorted[0][1]

        top_values_origin_indexes = []
        for (k, v) in self._values_sorted[:6]:
            top_values_origin_indexes.append(dto.values_c.index((k, v)))

        self._values_str = []
        for oindex in sorted(top_values_origin_indexes):
            _, val = dto.values_c[oindex]
            self._values_str.append(str(round(val)).rjust(2))

        super().set()

    def _format(self, amount: int) -> str|None:
        if self._values_str is None:
            return None
        parts = self._values_str[:amount]
        return " ".join(parts) + ("", "°")[len(parts) > 0]

    def format_label(self) -> str | Iterable[str] | None:
        if self._state_three:
            return self._format(3)
        elif self._state_one or self.attention:
            return self._format(1)
        return ""

    def format_details(self) -> str | Iterable[str] | None:
        if self._values_sorted is None:
            return None
        return "\n".join(
            [*(f"{fit(v[0], 15)}\t{v[1]:.0f}°C" for v in self._values_sorted[:10])]
            + [f"(+{len(self._values_sorted[10:])} more)" if len(self._values_sorted) > 10 else ""]
        )


class IndicatorTemperature(_BaseIndicator[TemperatureInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.temperature"
        self._value = ValueTemperature()

        super().__init__(
            indicator_name="temperature",
            socket_topic="temperature",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(*range(100, -80, -10), -273),
                subpath="temperature",
                path_dynamic_tpl="%s.svg",
            ),
            title="Thermal sensors",
            states=[*self._value.states],
        )

    def _render(self, msg: SocketMessage[TemperatureInfo]):
        self._value.set(msg.data)

        self._update_title_attention(self._value.attention)
        self._update_details(self._value.format_details())
        self._render_result(
            self._value.format_label(),
            icon=self._icon_selector.select(self._value.value_max_c),
        )
