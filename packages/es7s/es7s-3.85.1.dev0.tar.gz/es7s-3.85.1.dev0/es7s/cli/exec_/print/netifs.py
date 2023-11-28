# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import functools

import psutil
import typing as t
import pytermor as pt

from es7s.cli._decorators import cli_option
from es7s.cli._decorators import cli_command


@cli_command(__file__, short_help="network interface list")
@cli_option('-H', '--no-header', is_flag=True, help='Omit header from the output.')
class invoker:
    """
    .
    """
    def __init__(self, **kwargs):
        self._run(**kwargs)

    def _run(self, no_header: bool):
        header = not no_header

        def row(val: t.Iterable, pad=0, align=pt.Align.LEFT, transfn=lambda s: s or '-') -> str:
            fit = functools.partial(pt.fit, align=align, overflow='')

            def make(tval):
                tval = [*tval]
                if header:
                    yield ' '*pad
                yield fit(tval.pop(0), 18-pad)
                yield from [fit(cc, 16) for cc in tval[:-1]]
                yield fit(tval[-1], 12)
            return ' '.join(make(transfn(v) for v in val))

        cols = ['network interface', 'address', 'net mask', 'broadcast', 'ptp', 'family']
        if header:
            print(row(cols, 0, pt.Align.CENTER, str.upper))
            print(row(len(cols)*['='*17], 0))
        for k in (ifs := psutil.net_if_addrs()):
            for c in ifs[k]:
                if ':' in c.address:  # filter out ipv6
                    continue
                print(row([k, *[*c][1:], c.family.name], pad=1))
