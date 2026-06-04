"""Бизнес-логика каталога (верифицируемое поведение по ТЗ)."""

from typing import Dict, List, Optional

from .models import Book, OperationResult
from .validators import validate_author, validate_isbn, validate_title, validate_year


class LibraryService:
    """
    Сервис каталога библиотеки.

    ТЗ (для верификации):
    - add_book: добавляет книгу по уникальному ISBN
    - find_by_isbn: возвращает книгу или None
    - search: поиск по подстроке в названии/авторе (без учёта регистра)
    - borrow / return_book: меняет флаг available
    - list_all: возвращает все книги, отсортированные по названию
    """

    def __init__(self) -> None:
        self._books: Dict[str, Book] = {}

    def count(self) -> int:
        return len(self._books)

    def add_book(
        self, isbn: str, title: str, author: str, year
    ) -> OperationResult:
        ok, isbn_or_err = validate_isbn(isbn)
        if not ok:
            return OperationResult(False, isbn_or_err)
        ok, title = validate_title(title)
        if not ok:
            return OperationResult(False, title)
        ok, author = validate_author(author)
        if not ok:
            return OperationResult(False, author)
        ok, year_str = validate_year(year)
        if not ok:
            return OperationResult(False, year_str)

        isbn_clean = isbn_or_err
        if isbn_clean in self._books:
            return OperationResult(False, "Книга с таким ISBN уже есть")

        book = Book(
            isbn=isbn_clean,
            title=title,
            author=author,
            year=int(year_str),
            available=True,
        )
        self._books[isbn_clean] = book
        return OperationResult(True, "Книга добавлена", book.to_dict())

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        ok, isbn_clean = validate_isbn(isbn)
        if not ok:
            return None
        return self._books.get(isbn_clean)

    def search(self, query: str) -> List[Book]:
        if not query or not str(query).strip():
            return []
        q = query.strip().lower()
        results = [
            b
            for b in self._books.values()
            if q in b.title.lower() or q in b.author.lower()
        ]
        return sorted(results, key=lambda b: b.title.lower())

    def borrow(self, isbn: str) -> OperationResult:
        book = self.find_by_isbn(isbn)
        if book is None:
            return OperationResult(False, "Книга не найдена")
        if not book.available:
            return OperationResult(False, "Книга уже выдана")
        updated = Book(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            year=book.year,
            available=False,
        )
        self._books[book.isbn] = updated
        return OperationResult(True, "Книга выдана", updated.to_dict())

    def return_book(self, isbn: str) -> OperationResult:
        book = self.find_by_isbn(isbn)
        if book is None:
            return OperationResult(False, "Книга не найдена")
        if book.available:
            return OperationResult(False, "Книга не была выдана")
        updated = Book(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            year=book.year,
            available=True,
        )
        self._books[book.isbn] = updated
        return OperationResult(True, "Книга возвращена", updated.to_dict())

    def list_all(self) -> List[Book]:
        return sorted(self._books.values(), key=lambda b: b.title.lower())

    def load_bulk(self, books: List[dict]) -> int:
        """Загрузка для нагрузочных тестов."""
        added = 0
        for item in books:
            r = self.add_book(
                item["isbn"], item["title"], item["author"], item["year"]
            )
            if r.success:
                added += 1
        return added
