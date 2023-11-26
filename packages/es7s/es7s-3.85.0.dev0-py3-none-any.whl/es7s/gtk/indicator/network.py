# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import itertools
from collections.abc import Iterable
from copy import copy
from functools import cached_property

import pytermor as pt

from es7s.shared import SocketMessage
from es7s_commons import filtere
from es7s.shared import (
    NetworkCountryInfo,
    NetworkLatencyInfo,
    NetworkUsageInfo,
    NetworkUsageInfoStats,
    uconfig,
)
from es7s.shared import NetworkInfo
from ._base import WAIT_PLACEHOLDER, _BaseIndicator, IValue, DT
from ._icon_selector import IIconSelector, IconEnum
from ._state import _BoolState, CheckMenuItemConfig


class NetworkIconEnum(IconEnum):
    DISABLED = "disabled.svg"
    DOWN = "down.svg"
    WAIT = "wait.svg"


class NetworkIconPartEnum(IconEnum):
    NETCOM = "nc"


class NetworkIconPartVpnEnum(IconEnum):
    ENABLED = "vpn"
    WARNING = "vpnw"
    FOREIGN = "vpnf"


class NetworkIconPartArrowEnum(IconEnum):
    VAL_0 = "0"  # @TODO duplicated definitions with NetworkIndicatorIconBuilder
    VAL_1 = "1"
    VAL_2 = "2"
    VAL_3 = "3"
    VAL_4 = "4"
    VAL_5 = "5"
    VAL_6 = "6"
    WARNING = "w"
    ERROR = "e"


class NetworkIconSelector(IIconSelector):
    def __init__(self, exclude_foreign_codes: set[str]):
        super().__init__(NetworkIconEnum.DISABLED, subpath="network")
        self._path_dynamic_tpl = "%s.svg"
        self._exclude_foreign_codes = exclude_foreign_codes

    def select(
        self,
        last_usage: NetworkUsageInfo = None,
        last_country: NetworkCountryInfo = None,
        last_latency: NetworkLatencyInfo = None,
        netcom=False,
    ) -> str | IconEnum:
        if override := super().select():
            return override

        if not last_usage:
            return NetworkIconEnum.WAIT
        if not last_usage.isup:
            return NetworkIconEnum.DOWN

        frames: list[str | None] = [self._get_vpn_fid_part(last_usage, last_country)]
        for uis in (last_usage.sent, last_usage.recv):
            frames.append(self._get_icon_frame(uis, last_latency))
        frames.append(NetworkIconPartEnum.NETCOM if netcom else None)

        return self._compose_path(frames)

    @cached_property
    def icon_names_set(self) -> set[str | IconEnum]:
        def _iter() -> Iterable[str]:
            yield from NetworkIconEnum.list()
            for pts in itertools.product(
                [None, *NetworkIconPartVpnEnum],
                [*NetworkIconPartArrowEnum],
                [*NetworkIconPartArrowEnum],
                [None, NetworkIconPartEnum.NETCOM],
            ):
                yield self._compose_path(pts)

        return set(_iter())

    def _compose_path(self, frames: list[str | None]) -> str:
        return self._path_dynamic_tpl % "-".join(pt.filtern(frames))

    def _get_icon_frame(
        self,
        uis: NetworkUsageInfoStats | None,
        last_latency: NetworkLatencyInfo,
    ) -> str:
        if not uis:
            return NetworkIconPartArrowEnum.VAL_0

        failed_ratio = last_latency.failed_ratio if last_latency else 0.0
        if uis.errors or failed_ratio > 0.5:
            return NetworkIconPartArrowEnum.ERROR

        if uis.drops or failed_ratio > 0.0:
            return NetworkIconPartArrowEnum.WARNING

        if uis.bps:
            if uis.bps > 4e7:  # 40 Mbps
                return NetworkIconPartArrowEnum.VAL_6
            if uis.bps > 2e7:  # 20 Mbps
                return NetworkIconPartArrowEnum.VAL_5
            if uis.bps > 1e7:  # 10 Mbps
                return NetworkIconPartArrowEnum.VAL_4
            if uis.bps > 1e6:  # 1 Mbps
                return NetworkIconPartArrowEnum.VAL_3
            if uis.bps > 1e5:  # 100 kbps
                return NetworkIconPartArrowEnum.VAL_2
            if uis.bps > 1e4:  # 10 kpbs
                return NetworkIconPartArrowEnum.VAL_1
        # if uis.ratio:
        #     if uis.ratio > 0.4:
        #         return "4"
        #     ...
        #     if uis.ratio > 0.01:
        #         return "1"
        return NetworkIconPartArrowEnum.VAL_0

    def _get_vpn_fid_part(
        self,
        last_usage: NetworkUsageInfo,
        last_country: NetworkCountryInfo,
    ) -> str | None:
        if not last_usage or not last_usage.vpn:
            return None

        if not last_country or not last_country.country:
            return NetworkIconPartVpnEnum.WARNING

        if last_country.country.lower() in self._exclude_foreign_codes:
            return NetworkIconPartVpnEnum.ENABLED

        return NetworkIconPartVpnEnum.FOREIGN


class ValueNetworkUsage(IValue):
    def __init__(self):
        super().__init__()
        self._value: NetworkUsageInfo | None = None
        self.state = _BoolState(
            config_var=("indicator.network", "label-rate"),
            gconfig=CheckMenuItemConfig("Show usage/conn. speed (bit/s, max)", sep_before=True),
        )
        self._formatter = pt.StaticFormatter(
            pt.formatter_bytes_human,
            max_value_len=4,
            auto_color=False,
            allow_negative=False,
            allow_fractional=True,
            discrete_input=False,
            unit="",
            unit_separator="",
            pad=True,
        )

    def set(self, dto: NetworkUsageInfo|None):
        self._value = dto
        super().set()

    @property
    def warn_level_exceeded(self) -> bool:
        if self._value is None:
            return False
        return any((s.errors or s.drops) for s in self._value.stats if s)

    @property
    def bps_values(self) -> Iterable[float]:
        if self._value is None:
            return
        yield from map(lambda s: s.bps, pt.filtern(self._value.stats))

    def _format_stats(self, stats: NetworkUsageInfoStats = None) -> str:
        if stats:
            if stats.errors:
                return f"{stats.errors}×ERR"
            if stats.drops:
                return f"{stats.drops}×DRP"
            if stats.bps is not None:
                return self._format_bps(stats.bps)
        return "---"

    def _format_bps(self, bps: float = None) -> str:
        if not bps:
            return " 0.0k"
        if bps < 1000:
            return "<1.0k"
        return self._formatter.format(bps)

    def format_label(self) -> str | None:
        if self._value is None:
            return None
        if not (self.state or self.attention):
            return None
        if errors := sum(s.errors for s in self._value.stats):
            return f"{errors}×ERR"
        if drops := sum(s.drops for s in self._value.stats):
            return f"{drops}×DRP"
        if any(bps := self.bps_values):
            return self._format_bps(max(bps))
        return self._format_bps()

    def format_details(self) -> str | None:
        if self._value is None:
            return None
        parts = [
            "D↓" + self._format_stats(self._value.recv),
            "U↑" + self._format_stats(self._value.sent),
        ]
        return "  ".join(parts)


class ValueLatency(IValue):
    def __init__(self):
        super().__init__()
        self._value: NetworkLatencyInfo | None = None
        self.state = _BoolState(
            config_var=("indicator.network", "label-latency"),
            gconfig=CheckMenuItemConfig("Show latency/delivery rate (OK %)"),
        )
        self.warn_level_ms = uconfig.get_for(self).get("latency-warn-level-ms", int, fallback=400)

    def set(self, dto: NetworkLatencyInfo|None):
        self._value = dto
        super().set()

    @property
    def warn_level_exceeded(self) -> bool:
        if self._value is None:
            return False
        if self._value.latency_s is not None:
            if 1e3 * self._value.latency_s >= self.warn_level_ms:
                return True
        return bool(self._value.failed_ratio)

    @property
    def _show_label(self) -> bool:
        return self.state or self.attention

    def _format(self) -> str:
        if self._value.failed_ratio:
            return f"{100*(1-self._value.failed_ratio):3.0f}%"
        val, sep, pfx, unit = pt.formatter_time_ms._format_raw(self._value.latency_s * 1000)
        return " " * max(0, 4 - len(val + pfx + unit)) + val + pfx + unit

    def format_label(self) -> str | None:
        if self._value is not None and self._show_label:
            return self._format()

    def format_details(self) -> str | None:
        if self._value is not None:
            return self._format()


class ValueCountry(IValue):
    def __init__(self):
        super().__init__()
        self._value_country_code: str|None = None
        self._value_vpn: bool = False
        self.state = _BoolState(
            config_var=("indicator.network", "label-country"),
            gconfig=CheckMenuItemConfig("Show country code"),
        )

    def set(self, dto_ci: NetworkCountryInfo|None, dto_ui: NetworkUsageInfo|None):
        self._value_country_code = dto_ci.country if dto_ci else None
        self._value_vpn = dto_ui.vpn if dto_ui else False
        super().set()

    def _format(self) -> str:
        return self._value_country_code + ["", "*"][self._value_vpn]

    def format_label(self) -> str | None:
        if self._value_country_code is not None and self.state:
            return self._format()

    def format_details(self) -> str | None:
        if self._value_country_code is not None:
            return self._format()


class IndicatorNetwork(_BaseIndicator[NetworkInfo, NetworkIconSelector]):
    RENDER_INTERVAL_SEC = 1.0
    TITLE_BASE = "Network"

    def __init__(self):
        self.config_section = "indicator.network"
        self._interface = None
        self._obsolete_dto = dict[type, NetworkInfo]()
        self._netcom = False

        self._value_usage = ValueNetworkUsage()
        self._value_latency = ValueLatency()
        self._value_country = ValueCountry()

        super().__init__(
            indicator_name="network",
            socket_topic=["network-usage", "network-latency", "network-country"],
            icon_selector=NetworkIconSelector(
                self.uconfig().get("exclude-foreign-codes", set, str),
            ),
            title=self.TITLE_BASE,
            states=[
                self._value_usage.state,
                self._value_latency.state,
                self._value_country.state,
            ],
        )

    def _update_interface(self, last_usage: NetworkUsageInfo = None):
        if not last_usage:
            return
        self._interface = last_usage.interface
        self._title_base = (
            self.TITLE_BASE + "\t" + (self._interface or "")
        )  # @REWRITE this piece of sheet

    def _update_dto(self, msg: SocketMessage[NetworkInfo]):
        pass  # actual update is in render()

    def _render(self, msg: SocketMessage[NetworkInfo]):
        if (
            self._get_last_usage()
            and hasattr(msg.data, "interface")
            and self._interface != getattr(msg.data, "interface")
        ):
            self._render_no_data()
            self._obsolete_dto = copy(self._last_dto)
            self._value_usage.set(None)
            self._value_latency.set(None)
            self._value_country.set(None, None)
            return

        self._netcom = False
        super()._update_dto(msg)

        if hasattr(msg, "network_comm") and msg.network_comm:
            self._netcom = True

        last_usage = self._get_last_usage()
        icon = self._icon_selector.select(
            last_usage,
            self._get_last_dto(NetworkCountryInfo),
            self._get_last_dto(NetworkLatencyInfo),
            self._netcom,
        )

        if not last_usage:
            self._render_no_data()
            return

        if not last_usage.isup:
            self._render_result("N/A", "N/A", icon=icon, nc=self._netcom)
            return

        self._value_usage.set(last_usage)
        self._value_latency.set(self._get_last_dto(NetworkLatencyInfo))
        self._value_country.set(self._get_last_dto(NetworkCountryInfo), last_usage)

        self._update_title_attention(self._value_usage.attention or self._value_latency.attention)
        self._update_details(self._format_details())
        self._render_result(self._format_label(), icon=icon, nc=self._netcom)

    def _render_no_data(self):
        self._render_result("", icon=self._icon_selector.select())
        self._update_details(f"..." if self._interface else "(no interfaces)")

    def _get_last_dto(self, type_: type[DT]) -> DT | None:
        dto = super()._get_last_dto(type_)
        if dto != self._obsolete_dto.get(type_, None):
            return dto
        return None

    def _get_last_usage(self) -> NetworkUsageInfo | None:
        if last_usage := self._get_last_dto(NetworkUsageInfo):
            self._update_interface(last_usage)
        return last_usage

    def _format_label(self) -> str:
        parts = filtere(
            [
                self._value_usage.format_label(),
                self._value_latency.format_label(),
                self._value_country.format_label(),
            ]
        )
        return " ".join(parts)

    def _format_details(self) -> str:
        parts = filtere(
            [
                self._value_usage.format_details(),
                self._value_latency.format_details(),
                self._value_country.format_details(),
            ]
        )
        return " · ".join(parts).strip()
