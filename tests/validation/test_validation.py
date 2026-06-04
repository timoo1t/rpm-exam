#!/usr/bin/env python3
"""
ВАЛИДАЦИЯ — проверка, что программа принимает корректные данные
и отклоняет некорректные (соответствие ожиданиям пользователя/ввода).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent / "tests"))

from _bootstrap import run_main, PROJECT_ROOT  # noqa: E402
from library_catalog.service import LibraryService  # noqa: E402
from library_catalog.validators import (  # noqa: E402
    validate_isbn,
    validate_title,
    validate_author,
    validate_year,
)


def test_valid_inputs_accepted():
    svc = LibraryService()
    r = svc.add_book("9780123456789", "Valid Title", "Valid Author", 2024)
    assert r.success, r.message


def test_empty_title_rejected():
    svc = LibraryService()
    r = svc.add_book("1234567890", "   ", "Author", 2020)
    assert not r.success


def test_invalid_isbn_rejected():
    ok, msg = validate_isbn("abc")
    assert not ok
    svc = LibraryService()
    r = svc.add_book("abc", "Title", "Author", 2020)
    assert not r.success


def test_short_isbn_rejected():
    ok, _ = validate_isbn("12345")
    assert not ok


def test_year_out_of_range():
    ok, _ = validate_year(500)
    assert not ok
    ok, _ = validate_year(3000)
    assert not ok


def test_year_non_numeric():
    ok, _ = validate_year("нечисло")
    assert not ok


def test_author_too_long():
    ok, _ = validate_author("A" * 150)
    assert not ok


def test_search_empty_query_returns_empty():
    svc = LibraryService()
    svc.add_book("1234567890", "X", "Y", 2000)
    assert svc.search("") == []
    assert svc.search("   ") == []


def test_borrow_unknown_isbn():
    svc = LibraryService()
    r = svc.borrow("0000000000")
    assert not r.success


def test_main_rejects_unknown_flag():
    """Валидация CLI: неизвестный аргумент — ненулевой код выхода."""
    proc = run_main(["--unknown-flag-xyz"])
    assert proc.returncode != 0


def run_all() -> tuple[int, int]:
    tests = [
        test_valid_inputs_accepted,
        test_empty_title_rejected,
        test_invalid_isbn_rejected,
        test_short_isbn_rejected,
        test_year_out_of_range,
        test_year_non_numeric,
        test_author_too_long,
        test_search_empty_query_returns_empty,
        test_borrow_unknown_isbn,
        test_main_rejects_unknown_flag,
    ]
    passed = failed = 0
    print("=== ВАЛИДАЦИЯ ===")
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
