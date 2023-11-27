from typing import Optional, List, Union
from dataclasses import dataclass
from cmdi import CmdResult

from mewo_git import cmd as git_cmd
from mewo_git import prompt


@dataclass
class SeqSettings:
    version: Optional[str]
    new_release: bool
    check_status: bool
    check_diff: bool
    add_all: Optional[bool]
    commit: bool
    commit_msg: Optional[str]
    apply_tag: Optional[bool]
    push: Optional[bool]
    branch: str = "master"
    run_any: bool = True


def bump_git(
    version: str,
    new_release: bool = True,
    check_status: bool = True,
    check_diff: bool = True,
    add_all: Optional[bool] = None,
    apply_tag: Optional[bool] = None,
    push: Optional[bool] = None,
    commit: Optional[bool] = None,
    commit_msg: Optional[str] = None,
):
    """
    If arg is True -> Run command.
    If arg is False -> Do not run command.
    If arg is None -> Ask user what to do.
    """

    # Get Values
    # ----------

    s = SeqSettings(**locals())

    # Ask user to check status.
    if s.check_status and not prompt.confirm_status("y"):
        s.run_any = False

    # Ask user to check diff.
    if s.check_diff and not prompt.confirm_diff("y"):
        s.run_any = False

    # Ask user to run 'git add -A.
    if s.add_all is None:
        s.add_all = prompt.should_add_all(default="y")

    # Ask user to run commit.
    if commit is None:
        s.commit = prompt.should_commit(default="y")

    # Get commit msg from user.
    if s.commit and not s.commit_msg:
        s.commit_msg = prompt.commit_msg()

    # Ask user to run 'tag'.
    if s.apply_tag is None:
        s.apply_tag = prompt.should_tag(default="y" if s.new_release is True else "n")

    # Ask user to push.
    if s.push is None:
        s.push = prompt.should_push(default="y")

    # Ask user for branch.
    if any([s.apply_tag, s.push]):
        s.branch = prompt.branch()

    # Run Commands
    # ------------

    results: List[CmdResult] = []

    # If any git commands should be run.
    if not s.run_any:
        return results

    # Run 'add -A'
    if s.add_all:
        results.append(git_cmd.add_all())

    # Run 'commit'
    if s.commit:
        results.append(git_cmd.commit(msg=s.commit_msg))

    # Run 'tag'
    if s.apply_tag:
        results.append(git_cmd.tag(s.version, s.branch))

    # Run 'push'
    if s.push:
        results.append(git_cmd.push(s.branch))

    return results
