# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import typing as t

import pytermor as pt
from pytermor import get_qname

import es7s_commons
from es7s.cli._base import NWMarkup
from es7s.cli._base import CliCommand
from es7s.cli._base_opts_params import CMDTRAIT_ADAPTIVE, CMDTYPE_BUILTIN
from es7s.cli._decorators import catch_and_log_and_exit, cli_command


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="internal es7s markup syntax for command descriptions",
)
@catch_and_log_and_exit
class invoker:
    """
    Display NWML specification and examples. NWML stands for
    "Not-the-Worst-Markup-Language".\n\n
    """

    class CustomList(list):
        __hash__ = super(list).__hash__

    def __init__(self, **kwargs):
        nwml = NWMarkup()
        inspect(nwml._filters)
        inspect(pt.DualFormatterRegistry)
        inspect(pt.DualFormatter())
        inspect(pt.TemplateEngine())
        inspect(pt.SeqIndex)
        a = 1
        b = [a, 2, 3, 4]
        c = [b, 5, 6, 7, 8]
        d = [c, 9, 10]
        b.append(d)
        inspect(d)
        print(d)


def inspect(o: object):
    prev_level = 0
    for k, v, prim, level, acc in traverse(None, o):
        already_visited =( level < 0)
        if level < 0:
            level *= -1
        if prev_level > level and level < 1:
            print('')
        prev_level = level

        idstr = pt.Fragment(' '.join([''.join(c) for c in pt.chunk(f'{id(v):012x}', 4)]),
                            [pt.NOOP_STYLE, pt.Style(bg='red')][already_visited]
                            )
        if level > 0:
            pad = pt.Fragment(' ' + ('│  '*max(0, level-1)) + '├─')
        else:
            pad = ''
        #─├

        key_st = pt.Style()
        key_str = ""
        key_str_extra = ""
        if k is None and level == 0:
            key_st.fg = pt.cv.RED
            key_str = '⏺'
        else:
            if acc == property:
                key_st.fg = pt.cv.MAGENTA
            elif isinstance(k, str):
                key_st.fg = pt.cv.GREEN
            elif isinstance(k, int):
                key_st.fg = pt.cv.HI_BLUE
            key_str = str(k)
            if (key_repr := repr(k)).strip("'") != key_str:
                key_str = key_repr
            if v.__class__.__name__ == 'method':
                key_st.fg = pt.cv.HI_YELLOW
                key_str_extra = '()'
        key_frag = pt.Fragment(key_str, pt.Style(key_st, bold=False))

        type_st = pt.Style(fg=pt.cv.GRAY, italic=True)
        type_str = pt.Fragment(pt.fit(get_qname(v)+' ', 40-len(key_str+key_str_extra+pad)), type_st)
        if prim:
            val_st = pt.cv.BLUE
            if isinstance(v, bool):
                val_st = pt.cv.YELLOW
            if isinstance(v, str):
                val_st = pt.cv.GREEN
            if isinstance(v, type):
                val_st = pt.cv.RED
            val_frag = pt.Fragment(f'{v!r:.120s}', val_st)
        elif isinstance(v, t.Sized):
            val_frag = pt.Fragment(f'({len(v)})', pt.cv.BLUE)
        elif v is None:
            val_frag = pt.Fragment('None', pt.cv.GRAY)
        else:
            val_frag = repr(v)
        pt.echo(pt.Text(pad, ' '+key_frag+key_str_extra, ': '+type_str, val_frag))


def traverse(k: any, o: object, _level=0, *, _accessor=None, _descent=True):
    if not hasattr(traverse, "visited"):
        traverse.visited = set()

    if o.__class__.__name__ == 'builtin_function_or_method':
        return
    is_primitive = isinstance(o, (str, int, float, bool, type))
    yield k, o, is_primitive, _level, _accessor

    if id(o) in traverse.visited:
        return
    try:
        traverse.visited.add(id(o))
    except TypeError:
        pass

    if isinstance(o, t.Mapping):
        for kk, vv in o.items():
            yield from traverse(kk, vv, _level+1, _accessor=dict)
    elif isinstance(o, t.Sequence) and not isinstance(o, str):
        for kk, vv in enumerate(o):
            yield from traverse(kk, vv, _level+1, _accessor=list)

    if is_primitive or not _descent:
        return
    for attr in dir(o):
        if attr.startswith('__'):
            continue
        yield from traverse(attr, getattr(o, attr), _level+1, _accessor=property, _descent=False)
