"""Интерфейс командной строки (юзабилити)."""

import sys
from typing import List

from .service import LibraryService

HELP_TEXT = """
Каталог библиотеки — команды:
  help                          — эта справка
  add <isbn> <год> <название...> <::> <автор>
                                — добавить книгу (автор после ::)
  find <isbn>                   — найти по ISBN
  search <запрос>               — поиск по названию/автору
  list                          — список всех книг
  borrow <isbn>                 — выдать книгу
  return <isbn>                 — принять возврат
  exit                          — выход

Пример:
  add 9785012345678 2020 Война и мир :: Лев Толстой
""".strip()


def format_book_line(book) -> str:
    status = "в наличии" if book.available else "выдана"
    return f"[{book.isbn}] {book.title} — {book.author} ({book.year}), {status}"


def run_interactive(service: LibraryService | None = None) -> int:
    svc = service or LibraryService()
    print("Добро пожаловать в каталог библиотеки. Введите 'help' для справки.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо свидания.")
            return 0
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ("exit", "quit", "выход"):
            print("До свидания.")
            return 0
        if cmd == "help":
            print(HELP_TEXT)
            continue
        if cmd == "list":
            books = svc.list_all()
            if not books:
                print("Каталог пуст.")
            else:
                for b in books:
                    print(format_book_line(b))
            continue
        if cmd == "find" and len(parts) >= 2:
            book = svc.find_by_isbn(parts[1])
            if book:
                print(format_book_line(book))
            else:
                print("Книга не найдена.")
            continue
        if cmd == "search" and len(parts) >= 2:
            query = " ".join(parts[1:])
            books = svc.search(query)
            if not books:
                print("Ничего не найдено.")
            else:
                for b in books:
                    print(format_book_line(b))
            continue
        if cmd == "borrow" and len(parts) >= 2:
            r = svc.borrow(parts[1])
            print(r.message)
            continue
        if cmd == "return" and len(parts) >= 2:
            r = svc.return_book(parts[1])
            print(r.message)
            continue
        if cmd == "add":
            result = _parse_add_command(parts[1:])
            if result is None:
                print(
                    "Формат: add <isbn> <год> <название> :: <автор>"
                )
                continue
            isbn, year, title, author = result
            r = svc.add_book(isbn, title, author, year)
            print(r.message)
            continue

        print(f"Неизвестная команда: {cmd}. Введите 'help'.")


def _parse_add_command(args: List[str]):
    if len(args) < 4 or "::" not in args:
        return None
    sep = args.index("::")
    isbn = args[0]
    year = args[1]
    title = " ".join(args[2:sep])
    author = " ".join(args[sep + 1 :])
    if not title or not author:
        return None
    return isbn, year, title, author


def run_batch_commands(service: LibraryService, commands: List[str]) -> List[str]:
    """Выполнение команд без input() — для тестов юзабилити."""
    outputs: List[str] = []
    for line in commands:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        if cmd == "help":
            outputs.append(HELP_TEXT)
        elif cmd == "list":
            books = service.list_all()
            outputs.append(
                "\n".join(format_book_line(b) for b in books) or "Каталог пуст."
            )
        elif cmd == "find" and len(parts) >= 2:
            book = service.find_by_isbn(parts[1])
            outputs.append(
                format_book_line(book) if book else "Книга не найдена."
            )
        elif cmd == "search" and len(parts) >= 2:
            books = service.search(" ".join(parts[1:]))
            outputs.append(
                "\n".join(format_book_line(b) for b in books) or "Ничего не найдено."
            )
        else:
            outputs.append(f"Неизвестная команда: {cmd}. Введите 'help'.")
    return outputs
