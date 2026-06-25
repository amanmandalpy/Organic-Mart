#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from pathlib import Path


def _relaunch_with_project_venv() -> None:
    """Use the project virtual environment when beginners run plain `python`.

    On Windows it is easy to forget the virtual-environment activation command
    and accidentally use the global Python installation. That interpreter may
    have Django
    but not the rest of this project's dependencies, causing confusing import
    errors such as `No module named 'environ'`.
    """
    if os.environ.get("ORGANICMART_SKIP_VENV_REEXEC") == "1":
        return
    if sys.prefix != sys.base_prefix:
        return

    project_root = Path(__file__).resolve().parent
    if os.name == "nt":
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = project_root / ".venv" / "bin" / "python"

    if venv_python.exists() and Path(sys.executable).resolve() != venv_python:
        os.environ["ORGANICMART_SKIP_VENV_REEXEC"] = "1"
        os.execv(str(venv_python), [str(venv_python), *sys.argv])  # noqa: S606


def main() -> None:
    """Run Django management commands using local settings by default."""
    _relaunch_with_project_venv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django could not be imported. Activate the project's virtual "
            "environment and install requirements first."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
