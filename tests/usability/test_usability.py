#!/usr/bin/env python3
"""
ЮЗАБИЛИТИ — удобство использования: справка, понятные сообщения, предсказуемый CLI.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent / "tests"))

from _bootstrap import run_main, PROJECT_ROOT  # noqa: E402
from library_catalog.cli import HELP_TEXT, run_batch_commands  # noqa: E402
from library_catalog.service import LibraryService  # noqa: E402


def test_help_contains_all_commands():
    required = ["add", "find", "search", "list", "borrow", "return", "exit", "help"]
    lower = HELP_TEXT.lower()
    for cmd in required:
        assert cmd in lower, f"В справке нет команды: {cmd}"


def test_help_in_russian():
    assert "справка" in HELP_TEXT.lower() or "команды" in HELP_TEXT.lower()


def test_error_messages_readable():
    svc = LibraryService()
    r = svc.add_book("bad", "T", "A", 2020)
    assert len(r.message) > 5
    assert not r.message.startswith("Exception")


def test_unknown_command_hint():
    svc = LibraryService()
    out = run_batch_commands(svc, ["foobar"])
    assert any("help" in line.lower() for line in out)


def test_empty_catalog_message():
    svc = LibraryService()
    out = run_batch_commands(svc, ["list"])
    assert "пуст" in out[0].lower()


def test_main_help_flag():
    proc = run_main(["--help"])
    assert proc.returncode == 0
    assert "каталог" in proc.stdout.lower() or "библиотек" in proc.stdout.lower()


def test_demo_output_user_friendly():
    proc = run_main(["--demo"])
    assert "найдено" in proc.stdout.lower() or "add:" in proc.stdout.lower()
    assert proc.stderr.strip() == "" or len(proc.stderr) < 50


def test_search_no_results_message():
    svc = LibraryService()
    out = run_batch_commands(svc, ["search xyznonexistent"])
    assert out, "Команда search должна вернуть сообщение"
    assert "ничего" in out[0].lower() or "не найден" in out[0].lower()


def run_all() -> tuple[int, int]:
    tests = [
        test_help_contains_all_commands,
        test_help_in_russian,
        test_error_messages_readable,
        test_unknown_command_hint,
        test_empty_catalog_message,
        test_main_help_flag,
        test_demo_output_user_friendly,
        test_search_no_results_message,
    ]
    passed = failed = 0
    print("=== ЮЗАБИЛИТИ ===")
    print(f"Корень программы: {PROJECT_ROOT / 'main.py'}\n")
    for fn in tests:
        try:
            fn()
            print(f"  [OK] {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {fn.__name__}: {e}")
            failed += 1
    print(f"\nИтого: {passed} OK, {failed} FAIL")
    return passed, failed


if __name__ == "__main__":
    _, fail = run_all()
    sys.exit(1 if fail else 0)
