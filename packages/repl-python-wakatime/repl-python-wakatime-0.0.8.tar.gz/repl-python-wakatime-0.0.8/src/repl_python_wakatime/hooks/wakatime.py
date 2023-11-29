"""Wakatime
===========

Refer `create-plugin <https://wakatime.com/help/creating-plugin>`_.
"""
import os
from subprocess import run  # nosec: B404
from threading import Thread
from typing import Any, Callable


def send_wakatime_heartbeat(
    project: str = "",
    category: str = "coding",
    plugin: str = "repl-python-wakatime",
    filenames: list[str] = [".git"],
    detect_func: Callable[[str], bool] = os.path.isdir,
    *args: Any,
    **kwargs: Any,
) -> None:
    """Send wakatime heartbeat.

    If ``project == ""``, detect automatically.

    ``plugin`` must be the format of ``repl-REPL_NAME-wakatime`` to let
    wakatime detect correctly.

    :param project:
    :type project: str
    :param category:
    :type category: str
    :param plugin:
    :type plugin: str
    :param filenames:
    :type filenames: list[str]
    :param detect_func:
    :type detect_func: Callable[[str], bool]
    :rtype: None
    """
    if project == "":
        from ..utils.project import get_project

        project = get_project(filenames, detect_func)
    run(  # nosec: B603 B607
        [
            "wakatime-cli",
            "--write",
            f"--category={category}",
            f"--plugin={plugin}",
            "--entity-type=app",
            "--entity=python",
            "--alternate-language=python",
            f"--project={project}",
        ],
        stdout=open(os.devnull, "w"),
    )


def wakatime_hook(*args: Any, **kwargs: Any) -> None:
    """Wakatime hook.

    :param args:
    :type args: Any
    :param kwargs:
    :type kwargs: Any
    :rtype: None
    """
    task = Thread(target=send_wakatime_heartbeat, args=args, kwargs=kwargs)
    task.daemon = True
    task.start()
