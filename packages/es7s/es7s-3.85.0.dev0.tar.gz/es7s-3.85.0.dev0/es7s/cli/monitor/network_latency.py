# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from ._base import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig, GenericDemoComposer
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.shared import SocketMessage
from es7s.shared import Styles
from es7s.shared import NetworkLatencyInfo

OUTPUT_WIDTH = 5


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="network latency",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    NetworkLatencyMonitor(ctx, demo, **kwargs)


class NetworkLatencyMonitor(CoreMonitor[NetworkLatencyInfo, CoreMonitorConfig]):
    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="network-latency",
            network_comm_indic=True,
            config=CoreMonitorConfig("monitor.network-latency", debug_mode, force_cache),
            demo_composer=NetworkLatencyDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[NetworkLatencyInfo]) -> pt.Text:
        if msg.data.failed_ratio is None:
            return pt.Text("---".center(OUTPUT_WIDTH), Styles.TEXT_DISABLED)

        if msg.data.failed_ratio > 0:
            st = Styles.WARNING
            if msg.data.failed_ratio > 0.5:
                st = Styles.ERROR
            return pt.Text(f"{100*(1-msg.data.failed_ratio):3.0f}%", st)

        val, _, pfx, unit = pt.formatter_time_ms._format_raw(msg.data.latency_s * 1000)
        sep = pt.pad(OUTPUT_WIDTH - len(val+pfx+unit))
        return pt.Text(
            pt.Fragment(val, Styles.VALUE_PRIM_2),
            pt.Fragment(sep),
            pt.Fragment(pfx + unit, Styles.VALUE_UNIT_4),
        )


class NetworkLatencyDemoComposer(GenericDemoComposer):
    def render(self):
        ROW_LEN = 5

        table_len = (OUTPUT_WIDTH + 1) * ROW_LEN - 1
        self._print_triple_header([("Network latency", table_len)])

        dtos = [
            NetworkLatencyInfo(.0, 0),
            NetworkLatencyInfo(.0, 9.5e-4),
            NetworkLatencyInfo(.0, 1e-3),
            NetworkLatencyInfo(.0, 1e-2),
            NetworkLatencyInfo(.0, 1e-1),
            NetworkLatencyInfo(.0, 1.2e0),
            NetworkLatencyInfo(.0, 1.2e1),
            NetworkLatencyInfo(.0, 1.2e2),
            NetworkLatencyInfo(.10, 1),
            NetworkLatencyInfo(.40, 1),
            NetworkLatencyInfo(.70, 1),
            NetworkLatencyInfo(1.0, 1),
        ]

        cells = []
        while dtos or len(cells) != 0:
            if len(dtos):
                msg = SocketMessage(dtos.pop(0))
                cells.append(self._render_msg(msg))
            else:
                cells.append(" " * OUTPUT_WIDTH)

            if len(cells) == ROW_LEN:
                self._print_row(*cells)
                cells.clear()
        self._print_footer(table_len)
