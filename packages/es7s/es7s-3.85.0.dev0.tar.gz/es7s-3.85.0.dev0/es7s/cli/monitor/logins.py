# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from ._base import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.shared import SocketMessage, LoginsInfo
from es7s.shared import Styles

OUTPUT_WIDTH = 3


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="active OS-level user sessions",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    LoginsMonitor(ctx, demo, **kwargs)


class LoginsMonitor(CoreMonitor[LoginsInfo, CoreMonitorConfig]):
    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="logins",
            config=CoreMonitorConfig("monitor.logins", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[LoginsInfo]) -> pt.Text:
        val = len(msg.data.parsed)

        val_st = Styles.TEXT_DISABLED
        label_st = Styles.TEXT_DISABLED
        if val > 1:
            val_st = Styles.TEXT_UPDATED
            label_st = Styles.VALUE_LBL_5

        label_pfx = '('
        label_sfx = ')'
        val_str = str(val)
        if len(val_str) > 1:
            val_str = 'ô'

        return pt.Text(
            pt.Fragment(label_pfx, label_st),
            pt.Fragment(val_str.rjust(1), val_st),
            pt.Fragment(label_sfx, label_st),
        )
