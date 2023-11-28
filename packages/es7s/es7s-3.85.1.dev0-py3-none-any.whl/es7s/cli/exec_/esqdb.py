# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum
import io
import math
import os.path
import re
import sys
import time
from collections import deque, OrderedDict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property

import click
import pytermor as pt
from pytermor import get_terminal_width
from typing import BinaryIO

from es7s_commons import Regex
from es7s.shared import ESQDB_DATA_PIPE
from es7s.shared import FrozenStyle, Styles as BaseStyles, get_logger, get_stderr, get_stdout, with_terminal_state
from es7s.shared import ProxiedTerminalState
from .._base_opts_params import CMDTYPE_BUILTIN, EnumChoice, FloatRange
from .._decorators import cli_argument, cli_command, cli_option


@dataclass(frozen=True)
class SeqStyle:
    _primary: pt.RenderColor
    _secondary: pt.RenderColor
    _auxiliary: pt.RenderColor = pt.NOOP_COLOR
    _bg: pt.RenderColor = pt.NOOP_COLOR

    @cached_property
    def escape_byte(self) -> FrozenStyle:
        return FrozenStyle(fg=pt.cv.HI_WHITE, bg=self.bg, bold=True)

    @cached_property
    def classifier(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg)

    @cached_property
    def final(self) -> FrozenStyle:
        return FrozenStyle(fg=self._primary, bg=self.bg, bold=True)

    @cached_property
    def interm(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg, bold=True)

    @cached_property
    def param(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg)

    @cached_property
    def param_sep(self) -> FrozenStyle:
        return FrozenStyle(fg=self._secondary, bg=self.bg, dim=True)

    @cached_property
    def bg(self) -> pt.RenderColor:
        return self._bg

    @cached_property
    def legend(self) -> FrozenStyle:
        return FrozenStyle(fg=self.bg or self._secondary)


class _Styles(BaseStyles):
    def __init__(self):
        self.QUEUE = FrozenStyle(bg=pt.cvr.MIDNIGHT_BLUE)
        self.STATUSBAR_SEP_BG = pt.cvr.SPACE_CADET
        self.STATUSBAR_BG = pt.cvr.DARK_MIDNIGHT_BLUE

        self.STATUSBAR_SEP_BASE = FrozenStyle(fg=pt.cv.GRAY_0, bg=self.STATUSBAR_SEP_BG)
        self.STATUSBAR_BASE = FrozenStyle(fg=pt.cv.GRAY_0, bg=self.STATUSBAR_BG)

        self.CUR_PART_FMT = FrozenStyle(self.STATUSBAR_BASE, fg=pt.cv.HI_BLUE, bold=True)
        self.TOTAL_PARTS_FMT = FrozenStyle(self.STATUSBAR_BASE, fg=pt.cv.BLUE)
        self.LETTERS_FMT = FrozenStyle(self.STATUSBAR_BASE, fg=pt.cv.BLUE, bold=True)

        self.SEQ_NOOP = SeqStyle(pt.DEFAULT_COLOR, pt.DEFAULT_COLOR)
        self.SEQ_SGR = SeqStyle(pt.cv.YELLOW, pt.DEFAULT_COLOR)
        self.SEQ_SGR_RESET = SeqStyle(pt.cv.GRAY_0, pt.cv.GRAY_0, _bg=pt.cv.YELLOW)
        self.SEQ_UNKNOWN = SeqStyle(pt.cv.MAGENTA, pt.cv.MAGENTA, pt.cv.DEEP_PINK_8)
        self.SEQ_CURSOR = SeqStyle(pt.cv.BLUE, pt.cv.BLUE, pt.cv.NAVY_BLUE)
        self.SEQ_ERASE = SeqStyle(pt.cv.RED, pt.cv.RED, pt.cv.DARK_RED_2)
        self.SEQ_PRIVATE = SeqStyle(pt.cv.GREEN, pt.cv.GREEN, pt.cvr.DARK_GREEN)
        self.SEQ_CURSOR_FP = SeqStyle(pt.cv.CYAN, pt.cv.CYAN, pt.cvr.DARK_CYAN)

        self.PART_NUMBER = FrozenStyle(bg=pt.cv.GRAY_27, fg=pt.cv.GRAY_62, bold=True)
        self.PART_NEXT = FrozenStyle(fg=pt.cv.BLUE, bold=True)
        self.PART_PLAIN = FrozenStyle(fg=pt.cv.GRAY)
        self.PART_NEWLINE = FrozenStyle(fg=self.SEQ_CURSOR_FP.final.fg)
        self.PART_CARR_RET = self.PART_NEWLINE


class SequenceLegend:
    MAP = {
        Regex(R"\x1b\[0?m"): "reset SGR",
        Regex(R"\x1b\[([\d):;]+)m"): "regular SGR",
        Regex(R"\x1b\[(\d+)G"): "set cursor col.=%s",
        Regex(R"\x1b\[(\d+)d"): "set cursor line=%s",
        Regex(R"\x1b\[(\d+)F"): "cursor col.=1 ▼%s",
        Regex(R"\x1b\[(\d+)E"): "cursor col.=1 ▲%s",
        Regex(R"\x1b\[(\d+)C"): "mov cursor ▶%s",
        Regex(R"\x1b\[(\d+)D"): "mov cursor ◀%s",
        Regex(R"\x1b\[(\d+)B"): "mov cursor ▼%s",
        Regex(R"\x1b\[(\d+)A"): "mov cursor ▲%s",
        Regex(R"\x1b\[H"): "reset cursor",
        Regex(R"\x1b\[(\d*);?(\d*)H"): "set cursor %s,%s",
        Regex(R"\x1b7"): "save cursor pos",
        Regex(R"\x1b8"): "restore cursor pos",
        Regex(R"\x1b\[\?25l"): "hide cursor",
        Regex(R"\x1b\[\?25h"): "show cursor",
        Regex(R"\x1b\[0?J"): "clrscrn after cur",
        Regex(R"\x1b\[1J"): "clrscrn before cur",
        Regex(R"\x1b\[2J"): "clrscrn entirely",
        Regex(R"\x1b\[3J"): "clrscrn history",
        Regex(R"\x1b\[0?K"): "clrline after cur",
        Regex(R"\x1b\[1K"): "clrline before cur",
        Regex(R"\x1b\[2K"): "clrline entirely",
    }


class Mode(str, enum.Enum):
    SEND = "send"
    RECV = "recv"

    def __str__(self):
        return self.value


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    short_help="&escape &se&q &de&bugger, interactive step-by-step stream inspector",
    command_examples=[
        "1. read the output of a command through pipe broken down by escape seqs (no control terminal):",
        "",
        "     <<...>> | %s send - /dev/null",
        "",
        "2. stream breakdown+assembly (two terminals, 2nd is control one) communicating over a named pipe,",
        "   (which is set up by the application in the background if no arguments specified):",
        "",
        "     <<...>> | %s send",
        "     %s recv",
        "",
        "3. stream breakdown+assembly communicating over a file, which keeps the transmitted data:",
        "",
        "     <<...>> | %s send - /tmp/esq",
        "     tail -f /tmp/esq | %s recv",
        "",
        "4. step-by-step (manual control) breakdown+assembly from a file:",
        "",
        "     %s send /tmp/esq",
        "     %s recv",
        "",
        "5. similar to (4), but the same terminal is used for code display and as a control one (results may vary):",
        "",
        "     %s send /tmp/esq -",
    ],
)
@cli_argument("mode", type=EnumChoice(Mode), required=True)
@cli_argument("infile", type=click.File(mode="rb"), required=False)
@cli_argument("outfile", type=click.File(mode="wb"), required=False)
@cli_option(
    "-m",
    "--merge",
    is_flag=True,
    help="Merge subsequent SGRs into single pieces instead of processing the one-by-one. "
    "Useful when there is a necessity to inspect any other types of sequences, such "
    "as cursor controlling or display erasing ones.",
)
@cli_option(
    "-d",
    "--delay",
    type=FloatRange(_min=1e-9, max_open=True),
    default=0.4,
    show_default=True,
    metavar="SECONDS",
    help="Floating-point value determining the interval between processing each of split "
    "data chunks. This option takes effect only in automatic mode and is silently "
    "ignored in manual mode.",
)
@with_terminal_state  # @TODO send to stderr?
class invoker:
    """
    ¯Send mode¯

    Open specified INFILE in binary mode and start reading the content to the buffer.
    If omitted or specified as ''-'', the stdin will be used as data input instead.
    Split the data by ESC control bytes (`0x1b`) and feed the parts one-by-one to
    OUTFILE, or to a <<prepared named pipe>> in a system temporary directory, if no
    OUTFILE is specified.\n\n

    Manual control is available only if stdin of the process is a terminal, otherwise
    the automatic data writing is performed.\n\n

    ¯Receive mode¯

    Open specified INFILE in binary mode, start reading the content and immediately
    write the results to stdout. If INFILE is omitted, read from the same named pipe
    as in send mode instead (the filename is always the same). OUTFILE argument is
    ignored. No stream control is implemented. Terminate on EOF.

    ¯Statusbar¯

    Status example:

    ` <stdin> → /tmp/es7s-esqdb-pipe   F P A M                 4+37     12/32440`
    """

    MANUAL_CONTROL_HINT = "Press any key to send next part of the data, or Ctrl+C to exit. "
    AUTO_CONTROL_HINT = "Press Ctrl+C to exit. "

    LEGEND_WIDTH = 24

    def __init__(
        self,
        termstate: ProxiedTerminalState,
        mode: Mode,
        infile: io.RawIOBase | None,
        outfile: io.IOBase,
        merge: bool,
        delay: float,
        **kwargs,
    ):
        self._mode_manual_control = sys.stdin.isatty()
        self._mode_stats_display = sys.stdout.isatty()
        self._mode_merge_sgr = merge
        self._delay = delay
        self._styles = _Styles()

        if self._mode_manual_control:
            if mode is Mode.SEND:
                termstate.hide_cursor()
            termstate.disable_input()
        if self._mode_stats_display:
            termstate.assign_proxy(get_stderr())
            termstate.enable_alt_screen_buffer()
            get_stderr().echo(pt.make_reset_cursor())

        logger = get_logger()
        self._stream_types = {"out": "F", "in": "F"}

        self._last_seq_and_st = []

        try:
            if mode is Mode.SEND:
                logger.debug(f"Input is set to {infile}")
                self._run_send(
                    outfile or self._get_default_fifo(read=False),
                    infile or sys.stdin.buffer,
                )
            elif mode is Mode.RECV:
                self._run_rcv(
                    infile or self._get_default_fifo(read=True),
                )
            else:
                raise RuntimeError(f"Invalid mode: {mode}")
        finally:
            if infile and not infile.closed:
                infile.close()
            if outfile and not outfile.closed:
                outfile.close()

    @cached_property
    def _split_regex(self) -> re.Pattern:
        if self._mode_merge_sgr:
            # splits by \e[0m as well
            #return re.compile(rb"(\x1b\[\??(?:[0-9;:]*[^0-9;:m]|0?m))")
            return re.compile(rb"(\x1b\[\??[0-9;:]*[^0-9;:m])")
        return re.compile(rb"(\x1b)")

    def _wrap_buffer(self, stream: io.RawIOBase) -> tuple[BinaryIO, int | None]:
        max_offset = None
        buf = stream
        if stream.seekable():
            stream.seek(0, os.SEEK_END)
            max_offset = stream.tell()
            stream.seek(0)
            buf = io.BufferedReader(stream)
        if isinstance(buf, io.TextIOWrapper):
            buf = buf.buffer
        return buf, max_offset

    def _get_default_fifo(self, *, read: bool) -> BinaryIO:
        default = ESQDB_DATA_PIPE
        if not os.path.exists(default):
            get_logger().debug(f"Creating FIFO: '{default}'")
            os.mkfifo(default, 0o600)

        get_stderr().echo(f"{'Source' if read else 'Destination'} stream ", nl=False)
        get_stderr().echo(f"is a NAMED PIPE:  '{default}'")
        if read:
            get_stderr().echo("Waiting for the sender to start transmitting.")
            return open(default, "rb")
        get_stderr().echo("Waiting for the receiver to connect.")
        return open(default, "wb")

    def _run_send(self, outfile: io.IOBase = None, infile: io.RawIOBase = None):
        stderr = get_stderr()
        logger = get_logger()
        get_logger().debug(f"SEND mode, {infile} -> {outfile}")

        if self._mode_stats_display:
            stderr.echo(pt.make_clear_display())
            stderr.echo(pt.make_move_cursor_down(9999))
        else:
            stderr.echo(
                "It seems like stderr stream is not connected to a terminal, "
                "so statistics are disabled."
            )
            if self._mode_manual_control:
                stderr.echo(self.MANUAL_CONTROL_HINT)
            else:
                stderr.echo(self.AUTO_CONTROL_HINT)

        buf_offset = 0
        inbuf, max_offset = self._wrap_buffer(infile)
        infilename = getattr(infile, "name", "?")

        ps: deque[bytes] = deque()
        pll: int = 1
        offset: int = 0
        oll: int = 2 * math.ceil(len(f"{max_offset or 0:x}") / 2)

        idx = -1 if self._mode_manual_control else 0

        letters = [
            self._get_fletter("in", infile),
            self._get_fletter("out", outfile),
            ("A", " ")[self._mode_manual_control],
            (" ", "M")[self._mode_merge_sgr],
        ]
        letters_str = " ".join(["", *letters, ""])

        while not inbuf.closed or len(ps):
            if not inbuf.closed and (len(ps) < 3 or buf_offset - offset < 1024):
                psp = inbuf.readline()
                if not len(psp):
                    inbuf.close()
                buf_offset += len(psp)
                pspl = re.split(self._split_regex, psp)
                while len(pspl):
                    p = pspl.pop(0)
                    if not len(ps) or re.search(rb"[^\x1b]", ps[-1]):
                        ps.append(p)
                    else:
                        ps[-1] += p
                pll = max(pll, len(str(len(ps))))

            if self._mode_stats_display:
                stderr.echo(pt.make_set_cursor_column(1), nl=False)
                stderr.echo(pt.SeqIndex.RESET, nl=False)
                stderr.echo(pt.make_clear_line_after_cursor(), nl=False)

            twidth: int = get_terminal_width(pad=0)
            lineno = pt.Text(*self._format_part_no(idx - 1))
            olinew = twidth - len(lineno) - self.LEGEND_WIDTH

            if len(ps) and idx > 0:
                p = ps.popleft()
                pw = p
                if pw == self.hide_cursor_seq:
                    pw = b""
                offset += outfile.write(pw)
                outfile.flush()

                oline = stderr.render(self._decode(p, partnum=idx - 1, preview=False) or "")
                olines = pt.wrap_sgr(oline, olinew).splitlines()
                for Lidx, o in enumerate(olines):
                    stderr.echo_rendered(lineno, nl=False)
                    if Lidx == 0:
                        lineno = pt.Text(*self._format_part_no(idx - 1, blank=True))
                    stderr.echo(self._styles.PART_PLAIN.fg.to_sgr().assemble() + o, nl=False)
                    while Lidx == 0 and self._last_seq_and_st:
                        seq, st = self._last_seq_and_st.pop(0)
                        if not seq:
                            continue
                        stderr.echo(pt.SeqIndex.RESET, nl=False)
                        stderr.echo(
                            pt.make_set_cursor_column(twidth - self.LEGEND_WIDTH + 1), nl=False
                        )
                        stderr.echo_rendered(
                            self._format_legend(seq, st, self.LEGEND_WIDTH - 2), nl=False
                        )

                    stderr.echo()

            if self._mode_stats_display:
                stderr.echo(pt.make_move_cursor_down_to_start(1), nl=False)

                left_st = self._styles.QUEUE
                stderr.echo(left_st.bg.to_sgr(pt.ColorTarget.BG), nl=False)
                stderr.echo(pt.make_clear_line_after_cursor(), nl=False)
                if self._mode_manual_control and idx == -1:
                    stderr.echo_rendered(self.MANUAL_CONTROL_HINT, left_st, nl=False)
                    stderr.echo(pt.make_set_cursor_column(), nl=False)

                else:
                    examplestr = self._decode(ps[0] if len(ps) else b"", partnum=idx, preview=True)

                    status_right_fixed = (
                        pt.Fragment(" ", self._styles.STATUSBAR_SEP_BASE)
                        + pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                        + pt.Fragment(str(idx).rjust(pll), self._styles.CUR_PART_FMT)
                        + pt.Fragment("+" + str(len(ps)).rjust(pll), self._styles.TOTAL_PARTS_FMT)
                        + pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                        + pt.Fragment(" ", self._styles.STATUSBAR_SEP_BASE)
                        + pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                        + pt.Fragment(f"{offset:{oll}d}", self._styles.CUR_PART_FMT)
                        + pt.Fragment(
                            f"/{max_offset:{oll}d}" if max_offset else "", self._styles.TOTAL_PARTS_FMT
                        )
                        + pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                    )

                    status_right_flex: pt.Text = pt.Text()
                    if max_fname_len := max(
                        0, (twidth - len(status_right_fixed) - 16) // 2
                    ):  # self._get_max_fname_len(twidth):
                        status_right_flex += (
                            pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                            + pt.Fragment(
                                pt.cut(infilename, max_fname_len, ">"), self._styles.TOTAL_PARTS_FMT
                            )
                            + pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                            + pt.Fragment("→", self._styles.CUR_PART_FMT)
                            + pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                            + pt.Fragment(
                                pt.cut(getattr(outfile, "name", "-"), max_fname_len, ">"),
                                self._styles.TOTAL_PARTS_FMT,
                            )
                        )

                    status_right_flex += (
                        pt.Fragment(" ", self._styles.STATUSBAR_BASE)
                        + pt.Fragment(" ", self._styles.STATUSBAR_SEP_BASE)
                        + pt.Fragment(letters_str, self._styles.LETTERS_FMT)
                        + pt.Fragment(" ", self._styles.STATUSBAR_SEP_BASE)
                    )

                    if twidth < len(status_right_fixed):
                        status_right_flex = pt.Text()
                        status_right_fixed.set_width(min(twidth, len(status_right_fixed)))
                    else:
                        free = twidth - len(status_right_fixed)
                        status_right_flex.set_width(max(0, free))

                    if examplestr and (twidth - self.LEGEND_WIDTH) < len(examplestr):
                        examplestr.set_width(twidth - self.LEGEND_WIDTH)

                    stderr.echo(left_st.bg.to_sgr(pt.ColorTarget.BG), nl=False)
                    stderr.echo(pt.make_clear_line_after_cursor(), nl=False)
                    examplestr.prepend(pt.Fragment("", left_st, close_this=False))
                    stderr.echo_rendered((examplestr or ""), nl=False)

                    stderr.echo(pt.make_save_cursor_position(), nl=False)
                    stderr.echo(pt.make_reset_cursor(), nl=False)
                    stderr.echo(self._styles.STATUSBAR_BG.to_sgr(pt.ColorTarget.BG), nl=False)
                    stderr.echo(pt.make_clear_line_after_cursor(), nl=False)
                    stderr.echo_rendered(status_right_flex, nl=False)
                    stderr.echo_rendered(status_right_fixed, nl=False)

                    stderr.echo(pt.make_restore_cursor_position(), nl=False)

            self._wait(infile)

            logger.debug(f"State: (idx={idx}, offset={offset}/{max_offset})")
            if max_offset and offset == max_offset:
                if not self._mode_manual_control:
                    break
                stderr.echo_rendered(
                    "Done. Press any key to exit",
                    FrozenStyle(bg=self._styles.STATUSBAR_SEP_BG),
                    nl=False,
                )
                stderr.echo(self._styles.STATUSBAR_SEP_BG.to_sgr(pt.ColorTarget.BG), nl=False)
                stderr.echo(pt.make_clear_line_after_cursor(), nl=False)
                self._wait(infile)
                break

            idx += 1

    def _run_rcv(self, infile: io.RawIOBase = None):
        get_logger().debug(f"RCV mode, {infile} -> stdout")
        if not infile:
            infile = self._get_default_fifo(read=True)
        inbuf, max_offset = self._wrap_buffer(infile)
        if self._mode_stats_display:
            get_stdout().echo(pt.make_clear_display(), nl=False)
            get_stdout().echo(pt.make_reset_cursor(), nl=False)

        while i := inbuf.readline(1):
            get_stdout().io.buffer.write(i)  # noqa
            get_stdout().io.flush()

    hide_cursor_seq = pt.make_hide_cursor().assemble().encode()

    def _format_part_no(self, partnum: int, blank=False) -> Iterable[pt.RT]:
        yield pt.Fragment(f" {(str(partnum) if not blank else ''):4s} ", self._styles.PART_NUMBER)
        yield pt.Fragment("▏", FrozenStyle(self._styles.PART_NUMBER, bg=pt.DEFAULT_COLOR))

    def _format_legend(self, seq: pt.ISequence, st: SeqStyle, maxlen: int) -> pt.Fragment:
        seqass = seq.assemble()
        msg = repr(seq)
        for regex, desc in SequenceLegend.MAP.items():
            if m := regex.match(seqass):
                msg = desc
                if "%" in msg:
                    try:
                        msg %= m.groups()
                    except ValueError as e:
                        pass
                break
        return pt.Fragment(pt.fit(msg, maxlen, ">"), st.legend)

    def _decode(self, b: bytes, partnum: int, preview: bool) -> pt.Text:
        def _sanitize(s: str) -> str:
            return re.sub(
                r"(\x1b)|(\n+)|(\r+)|( +)",
                lambda m: (len(m[1] or "") * "ǝ")
                + (len(m[2] or "") * "↵\n")
                + (len(m[3] or "") * "⇤\r")
                + (len(m[4] or "") * "␣"),
                s,
            )

        result = pt.Text()
        ss = b.decode(errors="replace_with_qmark")
        for part in pt.parse(ss):
            if not result:
                if preview:
                    result.append(" NEXT ▏", self._styles.PART_NEXT)

            if not isinstance(part, pt.ISequence):
                for pline in re.split(r"(.[\n\r])", _sanitize(part)):
                    if pline.endswith("\n"):
                        result.append(pline.rstrip(), self._styles.PART_NEWLINE)
                    elif pline.endswith("\r"):
                        result.append(pline.rstrip(), self._styles.PART_CARR_RET)
                    else:
                        result.append(pline, self._styles.PART_PLAIN)
                continue

            seq = pt.ESCAPE_SEQ_REGEX.search(part.assemble())
            g = OrderedDict(
                {
                    k.rsplit("_", 1)[-1]: v
                    for k, v in seq.groupdict().items()
                    if v and re.match(r"data$|.+(_classifier|_interm|_param|_final)$", k)
                }
            )

            style = self._styles.SEQ_UNKNOWN
            if isinstance(part, pt.SequenceSGR):
                style = self._styles.SEQ_SGR
                if part == pt.SeqIndex.RESET:
                    style = self._styles.SEQ_SGR_RESET
            elif isinstance(part, pt.SequenceCSI):
                if g.get("final") in "HABDCFEdGn":
                    style = self._styles.SEQ_CURSOR
                elif g.get("final") in "JK":
                    style = self._styles.SEQ_ERASE
                elif g.get("final") in "lh" and g.get("interm") == "?":
                    style = self._styles.SEQ_PRIVATE
            elif isinstance(part, pt.SequenceFp):
                if g.get("classifier") in "78":
                    style = self._styles.SEQ_CURSOR_FP

            param = map(lambda p: (p, style.param), g.get("param", "").split(";"))
            params = pt.flatten1([*((p, (";", style.param_sep)) for p in param)])
            params.pop()
            result.append(
                "ǝ",
                style.escape_byte,
                g.get("classifier", ""),
                style.classifier,
                g.get("interm", ""),
                style.interm,
                *params,
                g.get("final"),
                style.final,
                " ",
            )
            if not preview:
                self._last_seq_and_st.append((part, style))
        return result

    def _wait(self, infile: io.IOBase):
        if self._mode_manual_control:
            pt.wait_key()
        else:
            time.sleep(self._delay)

    def _get_fletter(self, stype_key: str, file: io.IOBase) -> str:
        if file.isatty():
            return "T"
        elif getattr(file, "seekable", lambda: False)():
            return self._stream_types[stype_key]
        return "P"

    def _get_max_fname_len(self, twidth: int) -> int | None:
        if twidth < 60:
            return None
        return 10 + max(0, min((twidth - 80) // 5, 20))
