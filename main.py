#!/usr/bin/env python3
"""
КОРЕНЬ ПРОГРАММЫ — точка входа проекта «Каталог библиотеки».

Запуск:
  python main.py              — интерактивный режим
  python main.py --help       — справка
  python main.py --version    — версия
  python main.py --demo       — демо без ввода с клавиатуры
"""

import argparse
import sys
from pathlib import Path

# Добавляем src в путь для импорта модулей
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from library_catalog import __version__  # noqa: E402
from library_catalog.cli import run_interactive  # noqa: E402
from library_catalog.service import LibraryService  # noqa: E402


def run_demo() -> int:
    """Демонстрация работы без участия пользователя."""
    svc = LibraryService()
    print("=== Демо каталога библиотеки ===\n")
    steps = [
        ("add", "9785012345678", "1869", "Война и мир", "Лев Толстой"),
        ("add", "9785023456789", "1965", "Мастер и Маргарита", "Михаил Булгаков"),
        ("search", "мир"),
        ("borrow", "9785012345678"),
        ("list",),
    ]
    for step in steps:
        op = step[0]
        if op == "add":
            _, isbn, year, title, author = step
            r = svc.add_book(isbn, title, author, year)
            print(f"add: {r.message}")
        elif op == "search":
            books = svc.search(step[1])
            print(f"search '{step[1]}': найдено {len(books)}")
            for b in books:
                print(f"  - {b.title}")
        elif op == "borrow":
            r = svc.borrow(step[1])
            print(f"borrow: {r.message}")
        elif op == "list":
            print("list:")
            for b in svc.list_all():
                st = "в наличии" if b.available else "выдана"
                print(f"  [{b.isbn}] {b.title} — {st}")
    print("\n=== Демо завершено ===")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Каталог библиотеки — учебный проект РПМ"
    )
    parser.add_argument("--version", action="store_true", help="Показать версию")
    parser.add_argument("--demo", action="store_true", help="Режим демонстрации")
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0
    if args.demo:
        return run_demo()
    return run_interactive()


if __name__ == "__main__":
    raise SystemExit(main())
