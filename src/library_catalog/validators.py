"""Валидация входных данных (проверка корректности ввода)."""

import re
from typing import Tuple

ISBN_PATTERN = re.compile(r"^\d{10}(\d{3})?$")
MIN_YEAR = 1000
MAX_YEAR = 2100
MAX_TITLE_LEN = 200
MAX_AUTHOR_LEN = 100


def _ok(value: str) -> Tuple[bool, str]:
    if value is None or not str(value).strip():
        return False, "Поле не может быть пустым"
    return True, ""


def validate_isbn(isbn: str) -> Tuple[bool, str]:
    ok, msg = _ok(isbn)
    if not ok:
        return ok, msg
    cleaned = isbn.replace("-", "").strip()
    if not ISBN_PATTERN.match(cleaned):
        return False, "ISBN должен содержать 10 или 13 цифр"
    return True, cleaned


def validate_title(title: str) -> Tuple[bool, str]:
    ok, msg = _ok(title)
    if not ok:
        return ok, msg
    t = title.strip()
    if len(t) > MAX_TITLE_LEN:
        return False, f"Название не длиннее {MAX_TITLE_LEN} символов"
    return True, t


def validate_author(author: str) -> Tuple[bool, str]:
    ok, msg = _ok(author)
    if not ok:
        return ok, msg
    a = author.strip()
    if len(a) > MAX_AUTHOR_LEN:
        return False, f"Автор не длиннее {MAX_AUTHOR_LEN} символов"
    return True, a


def validate_year(year) -> Tuple[bool, str]:
    try:
        y = int(year)
    except (TypeError, ValueError):
        return False, "Год должен быть целым числом"
    if y < MIN_YEAR or y > MAX_YEAR:
        return False, f"Год должен быть от {MIN_YEAR} до {MAX_YEAR}"
    return True, str(y)
