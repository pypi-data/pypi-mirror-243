# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import importlib.resources
import os
import shutil
import stat
import tempfile
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from datetime import datetime
from functools import partial
from importlib.abc import Traversable
from os.path import basename, splitext
from pathlib import Path
from time import sleep
from typing import ClassVar, cast
import typing as t

import pytermor as pt
from click import pass_context

from es7s.shared import get_user_data_dir, ProxiedTerminalState, is_command_file
from es7s_commons import ProgressBar
from es7s.shared import RESOURCE_PACKAGE, USER_ES7S_BIN_DIR
from es7s.shared import (
    Styles,
    get_logger,
    get_stdout,
    run_detached,
    with_progress_bar,
)
from es7s_commons import format_attrs
from es7s.shared import SubprocessExitCodeError
from ..exec_.switch_wspace import invoker as invoke_switch_wspace
from .rebuild import invoker as invoke_rebuild
from .._base import Context, InvokerT
from .._decorators import catch_and_log_and_exit, cli_command, cli_option
from ... import APP_NAME


@cli_command(__file__)
@cli_option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Don't actually do anything, just pretend to.",
)
@cli_option(
    "-s",
    "--symlinks",
    is_flag=True,
    default=False,
    help="Make symlinks to core files instead of copying them. "
    "Useful for es7s development, otherwise unnecessary.",
)
@pass_context
@catch_and_log_and_exit
@with_progress_bar
class invoker:
    """Install es7s system."""

    pbar: ClassVar[ProgressBar]

    def __init__(
        self,
        pbar: ProgressBar,
        ctx: Context,
        dry_run: bool,
        symlinks: bool,
        **kwargs,
    ):
        self._stages: OrderedDict[t.Callable[[Context], str | None], str] = OrderedDict(
            {
                self._run_prepare: "Preparing",
                self._run_copy_core: "Copying core files",
                self._run_inject_bashrc: "Injecting into shell",
                self._run_inject_gitconfig: "Injecting git config",
                CopyDataRunner(dry_run, symlinks).run: "Copying data",
                CopyBinariesRunner(dry_run, symlinks).run: "Copying executables",
                self._run_install_with_apt: "Installing apt packages",
                self._run_install_with_pip: "Installing pip packages",
                self._run_install_x11: "Installing X11 packages",
                self._run_dload_install: "Downloading packages directly",
                # TmuxBuildInstallRunner(dry_run, symlinks)._run: "Building tmux",
                self._run_build_install_less: "Building less",
                self._run_build_install_htop: "Building htop",
                self._run_build_install_bat: "Building bat",
                self._run_install_es7s_exts: "Installing es7s extensions",
                self._run_install_daemon: "Installing es7s/daemon",
                self._run_install_shocks_service: "Installing es7s/shocks",
                self._run_setup_cron: "Setting up cron",
                partial(self._run_es7s_command, invoke_switch_wspace): "Installing switch-wspace",
                partial(self._run_es7s_command, invoke_rebuild): "Reconstructing resources",
            }
        )
        self._stages_results: OrderedDict[callable, tuple[bool, str]] = OrderedDict()
        self._current_stage: str | None = None
        invoker.pbar = pbar
        self._dry_run = dry_run
        self._symlinks = symlinks
        self._run(ctx)

    def _run(self, ctx: Context):
        invoker.pbar.init_tasks(len(self._stages))
        for stage_fn, stage_desc in self._stages.items():
            if fn := getattr(stage_fn, "func", None):
                current_stage = fn.__qualname__
            else:
                current_stage = stage_fn.__qualname__
            self._current_stage = current_stage.split(".")[1].lstrip("_")
            self._log(f"Starting stage: {self._current_stage}")
            invoker.pbar.next_task(stage_desc)
            try:
                result_msg = stage_fn(ctx)
            except StageFailedError as e:
                self._echo_failure(stage_desc, str(e))
                self._stages_results.update({stage_fn: (False, str(e))})
                continue
            except Exception as e:
                raise RuntimeError(self._current_stage + " failed") from e
            else:
                self._echo_success(stage_desc, result_msg)
                self._stages_results.update({stage_fn: (True, result_msg)})

    def _run_prepare(self, ctx: Context):
        # install docker
        # sudo xargs -n1 <<< "docker syslog adm sudo" adduser $(id -nu)
        # ln -s /usr/bin/python3 ~/.local/bin/python
        pass

    def _run_copy_core(self, ctx: Context):
        # install i -cp -v
        # git+ssh://git@github.com/delameter/pytermor@2.1.0-dev9
        pass

    def _run_inject_bashrc(self, ctx: Context):
        pass

    def _run_inject_gitconfig(self, ctx: Context):
        pass

    def _run_install_with_apt(self, ctx: Context):
        pass

    def _run_install_with_pip(self, ctx: Context):
        pass

    def _run_install_x11(self, ctx: Context):
        pass

    def _run_dload_install(self, ctx: Context):
        # ginstall exa
        # ginstall bat
        pass

    def _run_build_install_less(self, ctx: Context):
        # install less deps
        # build_less
        pass

    def _run_build_install_htop(self, ctx: Context):
        pass

    def _run_build_install_bat(self, ctx: Context):
        pass

    def _run_build_install_qcachegrind(self, ctx: Context):
        ...  # @temp on demand?

    def _run_build_install_bashdb(self, ctx: Context):
        ...  # @temp on demand?

    def _run_install_es7s_exts(self, ctx: Context):
        # install i -i -v

        # colors
        # fonts?
        # > pipx install kolombos
        # leo
        # > pipx install macedon
        # watson
        # nalog
        pass

    def _run_install_daemon(self, ctx: Context):
        # copy es7s.service to /etc/systemd/system
        # replace USER placeholders
        # enable es7s, reload systemd
        pass

    def _run_install_shocks_service(self, ctx: Context):
        # copy es7s-shocks.service to /etc/systemd/system
        # replace USER placeholders
        # enable shocks, reload systemd
        pass

    def _run_setup_cron(self, ctx: Context):
        pass

    def _run_es7s_command(self, invoker_: type[InvokerT], ctx: Context):
        if self._dry_run:
            self._log(f"Invoking `{invoker_}`")
            return
        ctx.invoke(invoker_, shell=True)

    def _log(self, msg: str):
        prefix = ""
        if self._dry_run:
            prefix += "DRY-RUN|"
        prefix += self._current_stage
        get_logger().info(f"[{prefix}] {msg}")

    def _echo_failure(self, stage_desc: str, msg: str):
        self._log(msg)

        stdout = get_stdout()
        text = pt.Text(
            pt.Fragment(" × ", Styles.MSG_FAILURE_LABEL),
            pt.Fragment(" " + stage_desc, Styles.MSG_FAILURE),
        )
        if msg:
            text += pt.Fragment(f": {msg}", Styles.MSG_FAILURE_DETAILS)
        stdout.echo_rendered(text)

    def _echo_success(self, stage_desc: str, msg: str = None):
        if msg:
            if self._dry_run:
                msg += " [NOT REALLY]"
            self._log(msg)

        stdout = get_stdout()
        text = pt.Text(
            pt.Fragment(" ⏺ ", Styles.MSG_SUCCESS_LABEL) + " " + stage_desc + "...",
        )
        if not msg:
            msg = "done"
        if msg:
            text += stdout.render(" " + msg.strip(), Styles.MSG_SUCCESS)

        stdout.echo_rendered(text)


class AbstractRunner(metaclass=ABCMeta):
    def __init__(self, dry_run: bool, symlinks: bool):
        self._dry_run = dry_run
        self._symlinks = symlinks

    @abstractmethod
    def run(self, ctx: Context):
        ...

    # -------------------------------------------------
    # Execution

    def _run_assert_zero_code(self, args: any, cwd: str = None):
        self._log_io("Running", format_attrs(args))
        if self._dry_run:
            return True

        exit_code = run_detached(args, cwd=cwd)
        if exit_code != 0:
            raise SubprocessExitCodeError(exit_code, args)

    # -------------------------------------------------
    # Git

    def _clone_git_repo(self, remote_url: str, path: str) -> bool:
        self._log_io("Cloning", path, remote_url)
        if self._dry_run:
            return True

        run_detached(["git", "clone", remote_url, "--progress"], cwd=path)
        return True

    # -------------------------------------------------
    # Filesystem

    def _make_dir(self, user_path: str | Path) -> bool:
        self._log_io("Creating", user_path)
        if self._dry_run:
            return True

        try:
            os.makedirs(user_path)
            self._log_io("Created", user_path)
        except Exception as e:
            get_logger().exception(e)
            get_logger().error(f"Failed to create dir: %s", user_path)
            return False

        return os.path.exists(user_path)

    def _remake_dir(self, user_path: Path) -> bool:
        if user_path.is_dir():
            self._remove_file_or_dir(user_path)
        return self._make_dir(user_path)

    def _make_temp_dir(self, name: str) -> str:
        now = datetime.now().timestamp()
        return tempfile.mkdtemp(str(now), f"es7s-core.install.{name}")

    def _remove_file_or_dir(self, user_path: str | Path) -> bool:
        self._log_io("Removing", user_path)
        if self._dry_run:
            return True

        try:
            if user_path.is_file() or user_path.is_symlink():
                os.unlink(user_path)
                self._log_io("Removed", user_path)

            elif os.path.isdir(user_path):
                shutil.rmtree(user_path)
                self._log_io("Removed", user_path)

            else:
                self._log_io("Not found", user_path)

        except Exception as e:
            get_logger().exception(e)
            get_logger().error(f"Failed to remove dir: %s", user_path)
            return False

        return not user_path.exists()

    def _write_file(self, user_path: Path, data: str | bytes, executable=True) -> bool:
        self._log_io("Writing", user_path, size=len(data))
        if self._dry_run:
           return True

        try:
            with open(user_path, "wt") as f:
                f.write(data)
            os.chmod(user_path, 0o777)
        except Exception as e:
            get_logger().exception(e)
            get_logger().error(f"Failed to write file: %s", user_path)
            return False

        return True

    def _copy_or_symlink(self, dist_path: Path, user_path: Path, overwrite=True) -> bool:
        action = "Linking" if self._symlinks else "Copying"

        if dist_path.is_dir():
            self._remake_dir(user_path)
            results = [
                self._copy_or_symlink(item.absolute(), user_path / item.name, overwrite)
                for item in dist_path.iterdir()
            ]
            return all(results)

        self._log_io(action, user_path, dist_path)
        if self._dry_run:
            return True

        if user_path.exists() or user_path.is_symlink():  # may be broken link
            if not overwrite:
                raise FileExistsError(user_path)
            self._remove_file_or_dir(user_path)

        try:
            if self._symlinks:
                os.symlink(dist_path, user_path)
                self._log_io("Linked", user_path, dist_path)
            else:
                shutil.copy(dist_path, user_path)
                self._log_io("Copied", user_path, dist_path)

        except Exception as e:
            get_logger().exception(e)
            get_logger().error(f"Failed to copy file: %s -> %s", dist_path, user_path)
            return False

        return True

    # -------------------------------------------------
    # Output

    def _log(self, msg: str):
        prefix = ""
        if self._dry_run:
            prefix += "DRY-RUN|"
        get_logger().info(f"[{prefix}] {msg}")

    def _log_io(self, action: str, target: str | Path, source: str | Path = None, size: int = None):
        prefix = ""
        path = f"{str(target)!r}"

        if source:
            path += f" <= {str(source)}"
            if not size and os.path.isfile(source):
                size = os.stat(source).st_size

        if size:
            path += " (" + pt.format_bytes_human(size) + "b)"

        self._log(f"{prefix}{action+':':<9s} {path}")


class CopyDataRunner(AbstractRunner):
    def run(self, ctx: Context) -> str:
        count = 0

        if not self._remake_dir(get_user_data_dir()):
            raise StageFailedError("Unable to start")

        dist_dir = importlib.resources.files(RESOURCE_PACKAGE)

        for dist_relpath in [
            *(f for f in dist_dir.iterdir() if f.is_file()),
            dist_dir / "conf.d",
            dist_dir / "xdotool",
        ]:
            dist_abspath = dist_relpath.absolute()

            user_relpath = dist_relpath
            if user_relpath.is_dir():  # to keep es7s.conf.d
                user_relpath = str(user_relpath).removesuffix(".d")
            user_abspath = get_user_data_dir() / os.path.basename(user_relpath)

            if self._copy_or_symlink(dist_abspath, user_abspath):
                count += 1

        return f"({count} files)"


class CopyBinariesRunner(AbstractRunner):
    def run(self, ctx: Context):
        count = 0

        if not self._remake_dir(USER_ES7S_BIN_DIR):
            raise StageFailedError("Unable to start")

        dist_roots: list[Path | Traversable] = [
            importlib.resources.files(f"{APP_NAME}.cli.exec_"),
            importlib.resources.files(f"{APP_NAME}.data") / "internal",
        ]

        while dist_roots and (dist_root := dist_roots.pop(0)):
            dist_dirs = [Path(".")]
            while dist_dirs and (d := dist_dirs.pop(0)):
                dist_dir = dist_root / d
                for f in dist_dir.iterdir():
                    if f.is_dir():
                        dist_dirs.append(d / f)
                    elif f.is_file():
                        name, ext = splitext(basename(f))
                        if not is_command_file(name, ext):
                            continue
                        dist_relpath = os.path.relpath(f, dist_root)
                        user_relpath = str(dist_relpath).replace("/", "-")
                        user_abspath = USER_ES7S_BIN_DIR / user_relpath.removesuffix(ext)

                        match ext:
                            case ".sh":
                                if self._copy_or_symlink(f, user_abspath):
                                    count += 1
                            case ".py" | ".txt":
                                self._write_launcher(user_abspath, dist_relpath.removesuffix(ext))
                                count += 1
                            case _:
                                get_logger().warning(f"Unknown file type %s: %s", ext, f)

        return f"({count} files)"

    def _write_launcher(self, user_abspath: Path, dist_relpath: str):
        data = "\n".join(
            [
                "#!/bin/sh",
                "es7s exec " + dist_relpath.replace("/", " ") + ' "$@"',
            ]
        )
        self._write_file(user_abspath, data)


class TmuxBuildInstallRunner(AbstractRunner):
    def run(self, ctx: Context) -> str:
        # sudo apt install automake autotools-dev bison build-essential byacc gcc iproute2 iputils-ping libevent-dev ncurses-dev pkg-config -y
        logger = get_logger()
        idx, total = 0, 5
        invoker.pbar.init_steps(steps_amount=total)

        try:
            temp_dir_path = self._make_temp_dir("tmux")

            invoker.pbar.next_step(step_label="Cloning primary repo")
            self._clone_git_repo("ssh://git@github.com/dl-forks/tmux", temp_dir_path)

            invoker.pbar.next_step(step_label="Building from sources")
            self._run_assert_zero_code(["sh", "autogen.sh"], cwd=temp_dir_path)
            self._run_assert_zero_code(["./configure && make"], cwd=temp_dir_path)
            self._run_assert_zero_code(["sudo make install"], cwd=temp_dir_path)
            self._remove_file_or_dir(temp_dir_path)

            # ln -s `pwd`/tmux ~/bin/es7s/tmux

            tpm_dir_path = os.path.expanduser("~/.tmux/plugins/tpm")
            self._make_dir(tpm_dir_path)

            invoker.pbar.next_step(step_label="Cloning tpm repo")
            self._clone_git_repo("ssh://git@github.com:tmux-plugins/tpm", tpm_dir_path)

            invoker.pbar.next_step(step_label="Installing tpm")
            self._run_assert_zero_code(
                ["tmux", "run-shell", "./bindings/install_plugins"], cwd=tpm_dir_path
            )

        except Exception as e:
            logger.exception(e)
            raise StageFailedError("Unable to continue")
        return "donee"


class StageFailedError(RuntimeError):
    pass
