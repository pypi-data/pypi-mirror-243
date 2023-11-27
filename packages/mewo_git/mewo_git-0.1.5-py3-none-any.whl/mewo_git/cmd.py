from mewo_git import lib
from cmdi import command, CmdResult, strip_cmdargs


@command
def add_all(**cmdargs) -> CmdResult:
    return lib.add_all()


@command
def log(
    revision_range: str = "-5",
    reverse: bool = False,
    no_pager: bool = True,
    **cmdargs,
) -> CmdResult:
    return lib.log(**strip_cmdargs(locals()))


@command
def commit(
    msg: str = "",
    **cmdargs,
) -> CmdResult:
    return lib.commit(**strip_cmdargs(locals()))


@command
def tag(
    version: str,
    branch: str,
    **cmdargs,
) -> CmdResult:
    return lib.tag(**strip_cmdargs(locals()))


@command
def push(
    branch: str,
    **cmdargs,
) -> CmdResult:
    return lib.push(**strip_cmdargs(locals()))


@command
def get_default_branch(**cmdargs) -> CmdResult:
    return lib.get_default_branch()


@command
def status(
    porcelain: bool = False,
    **cmdargs,
) -> CmdResult:
    return lib.status(**strip_cmdargs(locals()))


@command
def diff(**cmdargs) -> CmdResult:
    return lib.diff()


@command
def branch(
    show_current: bool = False,
    **cmdargs,
) -> CmdResult:
    return lib.branch(**strip_cmdargs(locals()))
