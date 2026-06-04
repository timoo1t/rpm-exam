#!/usr/bin/env python3
"""
Нагрузочное тестирование: скорость и память при разных объёмах данных.
Результаты сохраняются в benchmark_results.json и выводятся таблицей.
"""

import json
import sys
import time
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from library_catalog.service import LibraryService  # noqa: E402

LOADS = [100, 500, 1000, 5000]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "benchmark_results.json"


def _make_books(n: int) -> list[dict]:
    return [
        {
            "isbn": f"{9780000000 + i:010d}"[:13],
            "title": f"Книга номер {i}",
            "author": f"Автор {i % 50}",
            "year": 2000 + (i % 25),
        }
        for i in range(n)
    ]


def measure_load(n: int) -> dict:
    books = _make_books(n)
    tracemalloc.start()
    t0 = time.perf_counter()
    svc = LibraryService()
    added = svc.load_bulk(books)
    load_ms = (time.perf_counter() - t0) * 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t1 = time.perf_counter()
    _ = svc.search("книга")
    search_ms = (time.perf_counter() - t1) * 1000
    _, peak_search = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t2 = time.perf_counter()
    _ = svc.list_all()
    list_ms = (time.perf_counter() - t2) * 1000
    current, peak_list = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "records": n,
        "added": added,
        "load_ms": round(load_ms, 2),
        "search_ms": round(search_ms, 2),
        "list_all_ms": round(list_ms, 2),
        "memory_peak_kb": round(max(peak, peak_search, peak_list) / 1024, 2),
        "memory_current_kb": round(current / 1024, 2),
    }


def print_table(results: list[dict]) -> None:
    print("\n=== ТАБЛИЦА ПРОИЗВОДИТЕЛЬНОСТИ ===\n")
    header = (
        f"{'Нагрузка':>10} | {'Загрузка, мс':>12} | {'Поиск, мс':>10} | "
        f"{'Список, мс':>10} | {'Память пик, КБ':>14}"
    )
    print(header)
    print("-" * len(header))
    for r in results:
        print(
            f"{r['records']:>10} | {r['load_ms']:>12} | {r['search_ms']:>10} | "
            f"{r['list_all_ms']:>10} | {r['memory_peak_kb']:>14}"
        )
    print()


def run_benchmark() -> list[dict]:
    print("=== НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ ===")
    print(f"Корень программы: {PROJECT_ROOT / 'main.py'}\n")
    results = []
    for n in LOADS:
        print(f"  Тест при {n} записях...")
        results.append(measure_load(n))
    print_table(results)
    OUTPUT_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Результаты сохранены: {OUTPUT_FILE}")
    return results


if __name__ == "__main__":
    run_benchmark()
