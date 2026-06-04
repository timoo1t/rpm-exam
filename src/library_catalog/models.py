from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Book:
    """Книга в каталоге."""

    isbn: str
    title: str
    author: str
    year: int
    available: bool = True

    def to_dict(self) -> dict:
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            isbn=data["isbn"],
            title=data["title"],
            author=data["author"],
            year=int(data["year"]),
            available=bool(data.get("available", True)),
        )


@dataclass
class OperationResult:
    """Результат операции для CLI и тестов."""

    success: bool
    message: str
    data: Optional[dict] = None
