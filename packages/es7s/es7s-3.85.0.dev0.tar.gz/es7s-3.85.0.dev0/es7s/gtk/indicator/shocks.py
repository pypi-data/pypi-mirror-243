# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import itertools
import subprocess
from collections.abc import Iterable
from functools import cached_property
from subprocess import CalledProcessError

import pytermor as pt

from es7s.shared import SocketMessage
from es7s.shared import ShocksInfo, ShocksProxyInfo, uconfig
from es7s.shared import get_logger
from ._base import (
    _BaseIndicator, IValue,
)
from ._icon_selector import IIconSelector, IconEnum
from ._state import _StaticState, _BoolState, MenuItemConfig, CheckMenuItemConfig


class ShocksIconEnum(IconEnum):
    WAIT = "wait.svg"
    DISABLED = "disabled.svg"
    DOWN = "down.svg"


class ShocksIconPartEnum(IconEnum):
    TPL_FAILURE = "failure-%s.svg"
    TPL_SLOW = "slow-%s.svg"
    TPL_UP = "up-%s.svg"

    def compose(self, suffix: "ShocksIconSuffixEnum") -> str:
        return self.value % suffix.value


class ShocksIconSuffixEnum(str, pt.ExtendedEnum):
    VAL_1 = "1"
    VAL_2 = "2"
    VAL_3 = "3"
    VAL_4 = "4"
    VAL_NC = "nc"


class ShocksIconSelector(IIconSelector):
    def __init__(self, latency_warn_level_ms: int):
        super().__init__(ShocksIconEnum.WAIT, subpath="shocks")
        self._latency_warn_level_ms = latency_warn_level_ms

    def select(
        self,
        data: ShocksProxyInfo = None,
        tunnel_amount: int = None,
        network_comm: bool = None,
    ) -> str:
        if override := super().select():
            return override

        suffix = ShocksIconSuffixEnum.VAL_1
        if network_comm:
            suffix = ShocksIconSuffixEnum.VAL_NC
        elif tunnel_amount:
            suffix = ShocksIconSuffixEnum.resolve_by_value(str(max(1, min(tunnel_amount, 4))))

        if not data or not data.worker_up:
            return ShocksIconEnum.DISABLED

        if not data.running:
            return ShocksIconEnum.DOWN

        if not data.healthy:
            return ShocksIconPartEnum.TPL_FAILURE.compose(suffix)

        if not tunnel_amount:
            return ShocksIconEnum.WAIT

        if (data.latency_s or 0) * 1000 >= self._latency_warn_level_ms:
            return ShocksIconPartEnum.TPL_SLOW.compose(suffix)

        return ShocksIconPartEnum.TPL_UP.compose(suffix)

    @cached_property
    def icon_names_set(self) -> set[str]:
        def _iter() -> Iterable[str]:
            yield from ShocksIconEnum
            yield from [
                tpl.compose(suffix)
                for tpl, suffix in itertools.product(
                    ShocksIconPartEnum,
                    ShocksIconSuffixEnum,
                )
            ]

        return set(_iter())


class ValueShocks(IValue):
    def __init__(self):
        super().__init__()
        self._value: ShocksInfo|None = None
        self._value_prim: ShocksProxyInfo|None = None

        self.state = _BoolState(
            config_var=("indicator.shocks", "label"),
            gconfig=CheckMenuItemConfig("Show latency", sep_before=True),
        )
        self.warn_level_ms = uconfig.get_for(self).get("latency-warn-level-ms", int, fallback=1000)

    def set(self, dto: ShocksInfo):
        self._value = dto
        if self._value is None:
            return
        for proxy in self._value.proxies:
            if proxy.name == "default" or len(self._value.proxies) == 1:
                self._value_prim = proxy
                break
        super().set()

    def _format_latency(self, lat_s: float) -> str:
        if lat_s >= 1:
            return pt.format_auto_float(lat_s, 3, allow_exp_form=False) + "s"
        return pt.format_time_ms(1e3 * lat_s)

    def _format(self, proxy: ShocksProxyInfo) -> str | None:
        if not proxy.worker_up:
            return "OFF"
        if not proxy.running:
            return "DWN"
        if not proxy.healthy:
            return "ERR"
        if not proxy.latency_s:
            return "---"
        return self._format_latency(proxy.latency_s)

    def format_label(self) -> str | None:
        if self._value_prim is None:  # @FIXME do smth about all these checks... seems to be redundant
            return None
        if not (self.state or self.attention):
            return ""
        return self._format(self._value_prim)

    def format_details(self) -> Iterable[str]:
        if self._value is None:  # @FIXME
            return
        for proxy in self._value.proxies:
            parts = [
                f"[{proxy.name}]",
                self._format(proxy),
            ]
            if proxy.proxy_latency_s:
                parts.insert(1, self._format_latency(proxy.proxy_latency_s))
            yield "\t".join(parts)

    @property
    def warn_level_exceeded(self) -> bool:
        if self._value_prim is None:  # @FIXME
            return False
        if not self._value_prim.latency_s:
            return False  # True
        latency_exceeded = (1e3 * self._value_prim.latency_s >= self.warn_level_ms)
        return latency_exceeded  # or not self._value_prim.healthy


class IndicatorShocks(_BaseIndicator[ShocksInfo, ShocksIconSelector]):
    SYSTEMCTL_CALL_TIMEOUT_SEC = 60

    def __init__(self):
        self.config_section = "indicator.shocks"
        self._value = ValueShocks()

        self._restart = _StaticState(
            callback=self._enqueue_restart,
            gconfig=MenuItemConfig("Restart service", sep_before=False),
        )

        super().__init__(
            indicator_name="shocks",
            socket_topic=["shocks"],
            icon_selector=ShocksIconSelector(self._value.warn_level_ms),
            title="SSH⚡SOCKS proxy",
            states=[self._restart, self._value.state],
        )

    def _restart_service(self):
        self._state.wait_timeout = self.SYSTEMCTL_CALL_TIMEOUT_SEC

        out, err = None, None
        try:
            try:
                cp = subprocess.run(
                    ["systemctl", "restart", "es7s-shocks.target"],
                    capture_output=True,
                    timeout=self.SYSTEMCTL_CALL_TIMEOUT_SEC,
                    check=True,
                )
            except CalledProcessError as e:
                out, err = e.stdout, e.stderr
                raise
        except Exception as e:
            get_logger().exception(e)
            self._add_timeout(self.RENDER_ERROR_TIMEOUT_SEC)
            self._render_no_data()
            [scc.monitor_data_buf.clear() for scc in self._socket_client_conn.values()]
        else:
            out, err = cp.stdout, cp.stderr

        if out:
            get_logger().info(out)
        if err:
            get_logger().error(err)

    def _enqueue_restart(self, _=None):
        self._enqueue(self._restart_service)

    def _render(self, msg: SocketMessage[ShocksInfo]):
        self._value.set(msg.data)

        if self._state.is_waiting:
            if msg.data.proxies and any((p.running and p.healthy) for p in msg.data.proxies):
                self._state.cancel_wait()
            else:
                if self._value.state:
                    self._render_result("BUSY", icon=ShocksIconEnum.WAIT, nc=msg.network_comm)
                else:
                    self._render_result("", icon=ShocksIconEnum.WAIT, nc=msg.network_comm)
                return

        if not msg.data.proxies:
            self._render_no_data()
            return

        icon = self._icon_selector.select(self._value._value_prim, msg.data.tunnel_amount, msg.network_comm)
        self._render_result(self._value.format_label() or "", icon=icon, nc=msg.network_comm)
        self._update_details("\n".join(sorted(self._value.format_details())))
