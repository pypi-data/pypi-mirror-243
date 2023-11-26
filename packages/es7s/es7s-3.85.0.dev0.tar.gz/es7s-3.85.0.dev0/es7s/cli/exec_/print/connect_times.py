# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from collections import OrderedDict, deque
from subprocess import CalledProcessError, CompletedProcess
from collections.abc import Iterable
import pytermor as pt
import click
from datetime import datetime, timedelta
from es7s.cli._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_X11, IntRange, CMDTRAIT_ADAPTIVE
from es7s.cli._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit
from es7s_commons import Scale, Gradient, GradientSegment
from es7s.shared import run_subprocess, get_stdout, get_logger, Styles


TIMINGS: OrderedDict[str, tuple] = OrderedDict(
    {
        "time_namelookup": ("DNS lookup", pt.cvr.AIR_SUPERIORITY_BLUE),
        "time_connect": ("Connect", pt.cvr.EMERALD_GREEN),
        "time_appconnect": ("App connect", pt.cvr.EMERALD),
        "time_pretransfer": ("Pre-transfer", pt.cvr.SAFETY_ORANGE),
        "time_redirect": ("Redirectons", pt.cvr.SAFETY_YELLOW),
        "time_starttransfer": ("Start transfer", pt.cvr.PACIFIC_BLUE),
        "time_total": ("Total", pt.cvr.FULL_WHITE),
    }
)


class CurlError(RuntimeError):
    ...


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="measure connection timings (lookups, redirects)",
)
@cli_argument(
    "url",
    type=click.STRING,
    required=True,
    nargs=-1,
)
@cli_option(
    "-p",
    "--proxy",
    metavar='[protocol://]host[:port]',
    default=None,
    help='Use the specified proxy. \'protocol\' is one of: `http` [is a default], '
         '`https`, `socks4`, `socks4a`, `socks5`, `socks5h`. If not specified, the \'port\' is '
         '1080. Proxy auth should work as well, to use it provide credentials in the form of '
         '""username:password@host"" instead of just ""host"" alone.'
)
@cli_option(
    "-x",
    "--extend",
    count=True,
    help="Increase the amount of details. Can be used multiple times ('-xx', "
         "'-xxx'). First level enables detailed event log output, second one also "
         "traces requests and responses in text form, third one -- in hexadecimal form."
)
@cli_option(
    "-w",
    "--width",
    default=40,
    show_default=True,
    type=IntRange(_min=10, max_open=True),
    help="Output scale width, in characters."
)
@catch_and_log_and_exit
class invoker:
    """
    @TODO

    Requires ++curl++.
    """

    SHARED_SCALE_CHAR = "━"  # "━▁"
    SHARED_SCALE_CHAR_START = "╺"

    def __init__(self, url: tuple[str], width: int , **kwargs):
        self.run(urls=url, scale_width=width, **kwargs)

    def run(self, urls: tuple[str], scale_width: int, extend: int, proxy: str = None):
        stdout = get_stdout()
        url_width = min(pt.get_terminal_width(), max(map(len, urls)))
        curl = CurlInvoker()

        def _print_failure(msg: str, fmt: pt.FT):
            url_str = pt.cut(url, url_width)
            if len(url_str) + len(msg) + 2 < pt.get_terminal_width():
                stdout.echo(url_str, nl=False)
                stdout.echo_rendered("  " + str(e), fmt)
            else:
                stdout.echo(url_str)
                stdout.echo_rendered("\t" + str(e), fmt)

        for url in urls:
            try:
                result = curl.invoke(url, extend, proxy)
                journal = Journal(url, result.stderr, result.stdout)
            except (CurlError, ValueError) as e:
                get_logger().non_fatal_exception(e)
                _print_failure(str(e), Styles.ERROR)
                continue

            if extend > 0:
                journal.print_event_log()
            journal.print_summary(scale_width)


class CurlInvoker:
    CURL_EXIT_CODES: dict[int, str] = {
        1: "Unsupported protocol",
        5: "Could not resolve proxy",
        6: "Could not resolve host",
        7: "Failed to connect to host",
        28: "Operation timeout",
    }
    STDOUT_SEP: str = '\t'
    FMT: str = "%{stdout}" + STDOUT_SEP.join("%{" + t + "}" for t in TIMINGS.keys()) + "\n" + "%{size_download}"

    def invoke(self, url: str, extend: int = 0, proxy: str = None) -> CompletedProcess:
        trace_args = ['-v', '--trace-time']
        if extend == 2:
            trace_args += ["--trace-ascii", "%"]
        elif extend == 3:
            trace_args += ["--trace", "%"]

        proxy_args = ("--proxy", proxy) if proxy else []

        args = [
            "curl",
            "-w",
            self.FMT,
            *("-o", "/dev/null"),
            "-Lks",
            *("--max-time", "10"),
            *trace_args,
            *proxy_args,
            url,
        ]
        try:
            return run_subprocess(*args, check=False)
        except CalledProcessError as e:
            if error_desc := self.CURL_EXIT_CODES.get(e.returncode, None):
                raise CurlError(error_desc) from e
            raise CurlError(f"Exit code {e.returncode}")


class Record:
    def __init__(self, msg: str):
        self._msg = msg

    def render(self, *args) -> str:
        return get_stdout().render(pt.Text(*self._compose(*args)))

    def _compose(self, *args) -> Iterable:
        yield pt.pad(10)
        yield self._msg, pt.cv.GRAY


class DatedRecord(Record):
    def __init__(self, dt: datetime, mode: str, msg: str):
        super().__init__(msg)
        self._dt = dt
        self._mode = mode
        self._msg = msg

    @property
    def dt(self) -> datetime:
        return self._dt

    def delta_td(self, start: datetime) -> timedelta:
        return self.dt - start

    def delta_sec(self, start: datetime) -> float:
        return self.delta_td(start).total_seconds()

    def delta_ratio(self, start: datetime, end: datetime) -> float:
        return self.delta_sec(start) / (end - start).total_seconds()

    def _compose(self, start: datetime, fmt_time: pt.Style) -> Iterable:
        match self._mode:
            case "*"|"==":
                fmt = pt.Style(fg="white")
                mode = "·"
            case ">"|"=>":
                fmt = pt.Style(fg="magenta")
                mode = ">"
            case "}":
                fmt = pt.Style(fg="magenta", dim=True)
                mode = "»"
            case "<"|"<=":
                fmt = pt.Style(fg="cyan")
                mode = "<"
            case "{":
                fmt = pt.Style(fg="cyan", dim=True)
                mode = "«"
            case _:
                fmt = pt.Style()
                mode = self._mode

        yield pt.Fragment(("+"+pt.format_time_delta(self.delta_sec(start), 6).strip()).rjust(7), fmt_time)
        yield f" "
        yield pt.Fragment(mode, pt.Style(fmt, bold=True))
        yield " "
        yield pt.Fragment(self._msg, fmt)


class CurlOutputProcessor:
    @classmethod
    def process_log(cls, raw_log: str) -> Iterable[Record]:
        for line in raw_log.splitlines():
            try:
                ts, mode, msg = line.split(" ", 2)
                dt = datetime.strptime(ts, "%H:%M:%S.%f")
                yield DatedRecord(dt, mode, msg)
            except ValueError:
                yield Record(line)


class Journal(deque[Record]):
    def __init__(self, url: str, curl_verbose_output: str, curl_customized_output: str):
        super().__init__()
        self._url = url
        self._start_dt: datetime|None = None
        self._end_dt: datetime|None = None

        lines = curl_customized_output.splitlines()
        if len(parts := lines[0].split(CurlInvoker.STDOUT_SEP)) != len(TIMINGS):
            raise ValueError(f"Malformed curl output: {curl_customized_output!r}")
        self._summary = parts
        self._size = int(lines[1])

        for record in CurlOutputProcessor.process_log(curl_verbose_output):
            if not isinstance(record, DatedRecord):
                self.append(record)
                continue
            if self._start_dt is None:
                self._start_dt = record.dt
            self._end_dt = record.dt
            self.append(record)

    def print_event_log(self):
        fmt_time_grad: Gradient = Gradient([
            GradientSegment([0.0, 0.5, 1.0], pt.RGB(0x808080), pt.RGB(0xFFFFFF))
        ])
        for record in self:
            if isinstance(record, DatedRecord):
                fmt_time = pt.Style(fg=fmt_time_grad.interpolate(record.delta_ratio(self._start_dt, self._end_dt) or 0).int)
                rendered = record.render(self._start_dt, fmt_time)
            else:
                rendered = record.render()
            get_stdout().echo(rendered)

    def print_summary(self, scale_width: int):
        stdout = get_stdout()
        stdout.echo(self._url)
        stdout.echo()

        kvs = OrderedDict({1e3 * float(v): k for k, v in zip(TIMINGS.keys(), self._summary)})

        cursor = 0
        char_shift = 0
        max_name_len = max(map(lambda kv: len(kv[0]), TIMINGS.values()))
        total_ms = [*kvs.keys()][-1]

        skvs = [*sorted(kvs.keys())]
        while len(skvs):
            val_ms = skvs.pop(0)
            if not len(skvs):
                print()
            val_str = pt.format_time_ms(val_ms)
            if val_ms > 1000:
                val_str = f"{1e-3*val_ms:4.2f}s"
            name, scale_st = TIMINGS.get(kvs.get(val_ms))
            pre_scale = Scale(
                (cursor) / total_ms,
                pt.NOOP_STYLE,
                pt.Style(fg=pt.cvr.GRAY_KALM, overlined=True),
                scale_width,
                full_block_char="░" if len(skvs) else "'",
                allow_partials=False,
                ).blocks

            scale = ""
            if len(skvs):
                scale = Scale(
                    (val_ms - cursor) / total_ms,
                    pt.NOOP_STYLE,
                    scale_st,
                    scale_width,
                    full_block_char='▇',
                    allow_partials=False,
                    require_not_empty=True,
                    ).blocks

            stdout.echo(f"{name:>{2+max_name_len}s}  {val_str:>6s}  {pre_scale}{scale}")
            cursor = val_ms
            char_shift += len(scale)

        stdout.echo(f"{'Downloaded':>{2+max_name_len}s} {pt.format_bytes_human(self._size):>6s}b")
        stdout.echo()
