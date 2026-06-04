#!/usr/bin/env python3
"""
ВЕРИФИКАЦИЯ — проверка соответствия реализации техническому заданию.

ТЗ:
1. ISBN уникален при добавлении
2. search — подстрока в title/author, без учёта регистра
3. borrow снимает available; return восстанавливает
4. list_all сортирует по названию
5. find_by_isbn возвращает книгу или None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent / "tests"))

from _bootstrap import run_main, PROJECT_ROOT  # noqa: E402
from library_catalog.service import LibraryService  # noqa: E402


def test_unique_isbn():
    svc = LibraryService()
    assert svc.add_book("1234567890", "A", "Author", 2000).success
    r = svc.add_book("1234567890", "B", "Other", 2001)
    assert not r.success
    assert "уже есть" in r.message.lower() or "ISBN" in r.message


def test_search_case_insensitive():
    svc = LibraryService()
    svc.add_book("1111111111", "Python Guide", "Ivanov", 2020)
    assert len(svc.search("python")) == 1
    assert len(svc.search("IVANOV")) == 1
    assert len(svc.search("guide")) == 1


def test_borrow_return_cycle():
    svc = LibraryService()
    svc.add_book("2222222222", "Book", "Author", 1999)
    assert svc.borrow("2222222222").success
    b = svc.find_by_isbn("2222222222")
    assert b is not None and not b.available
    assert not svc.borrow("2222222222").success
    assert svc.return_book("2222222222").success
    b2 = svc.find_by_isbn("2222222222")
    assert b2 is not None and b2.available


def test_list_sorted_by_title():
    svc = LibraryService()
    svc.add_book("3333333333", "Яблоко", "A", 2000)
    svc.add_book("4444444444", "Абрикос", "B", 2000)
    titles = [b.title for b in svc.list_all()]
    assert titles == sorted(titles, key=str.lower)


def test_find_missing():
    svc = LibraryService()
    assert svc.find_by_isbn("9999999999") is None


def test_main_version_via_root():
    """Верификация: корень программы отвечает на --version."""
    proc = run_main(["--version"])
    assert proc.returncode == 0
    assert "1.0.0" in proc.stdout


def test_main_demo_via_root():
    """Верификация: демо-режим корня выполняется без ошибок."""
    proc = run_main(["--demo"])
    assert proc.returncode == 0
    assert "Демо" in proc.stdout or "демо" in proc.stdout.lower()


def run_all() -> tuple[int, int]:
    tests = [
        test_unique_isbn,
        test_search_case_insensitive,
        test_borrow_return_cycle,
        test_list_sorted_by_title,
        test_find_missing,
        test_main_version_via_root,
        test_main_demo_via_root,
    ]
    passed = failed = 0
    print("=== ВЕРИФИКАЦИЯ ===")
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
