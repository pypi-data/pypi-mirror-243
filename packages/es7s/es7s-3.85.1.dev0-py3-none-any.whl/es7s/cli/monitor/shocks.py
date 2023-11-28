# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from ._base import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.shared import SocketMessage
from es7s.shared import Styles
from es7s.shared import ShocksInfo

OUTPUT_WIDTH = 7


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="SSH/SOCKS proxy tunnels count",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    ShocksMonitor(ctx, demo, **kwargs)


class ShocksMonitor(CoreMonitor[ShocksInfo, CoreMonitorConfig]):
    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="shocks",
            network_comm_indic=True,
            config=CoreMonitorConfig("monitor.shocks", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[ShocksInfo]) -> pt.Text:
        val_conn = msg.data.relay_connections_amount or 0
        val_listen = msg.data.relay_listeners_amount or 0
        val_conn_st = Styles.TEXT_DISABLED
        val_listen_st = Styles.WARNING
        if val_conn > 0:
            val_conn_st = Styles.TEXT_UPDATED
        if val_listen > 0:
            val_listen_st = Styles.VALUE_PRIM_1

        val = str(msg.data.tunnel_amount)
        val_st = Styles.VALUE_PRIM_1
        if msg.data.tunnel_amount == 0:
            val_st = [Styles.WARNING, Styles.TEXT_DISABLED][bool(val_conn or val_listen)]
        if len(val) > 1:
            val = '9+'
            label = ''

        return pt.Text(
            pt.Fragment(val.rjust(1), val_st),
            pt.Fragment('T', Styles.VALUE_LBL_5),
            ' ',
            pt.Fragment(str(val_conn), val_conn_st),
            pt.Fragment('/', Styles.TEXT_DISABLED),
            pt.Fragment(str(val_listen), val_listen_st),
            pt.Fragment('R', Styles.VALUE_LBL_5),
        )
