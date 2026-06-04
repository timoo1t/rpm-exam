"""Общая настройка путей: все тесты обращаются к корню программы."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_SCRIPT = PROJECT_ROOT / "main.py"
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def run_main(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Запуск корня программы (main.py) как отдельного процесса."""
    cmd = [sys.executable, str(MAIN_SCRIPT)] + args
    return subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def import_app():
    from library_catalog.service import LibraryService
    from library_catalog import validators

    return LibraryService, validators
