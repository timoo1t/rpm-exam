#!/usr/bin/env python3
"""
Главный запускатель всех тестовых программ РПМ.
Обращается к корню программы (main.py) и запускает модули тестирования.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN = PROJECT_ROOT / "main.py"

MODULES = [
    ("Верификация", PROJECT_ROOT / "tests" / "verification" / "test_verification.py"),
    ("Валидация", PROJECT_ROOT / "tests" / "validation" / "test_validation.py"),
    ("Юзабилити", PROJECT_ROOT / "tests" / "usability" / "test_usability.py"),
    ("Производительность", PROJECT_ROOT / "tests" / "performance" / "benchmark.py"),
]


def main() -> int:
    print("=" * 60)
    print("  ТЕСТИРОВАНИЕ ПРОЕКТА РПМ — Каталог библиотеки")
    print(f"  Корень программы: {MAIN}")
    print("=" * 60 + "\n")

    # Проверка доступности корня
    proc = subprocess.run(
        [sys.executable, str(MAIN), "--version"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("[КРИТИЧНО] main.py недоступен или не запускается")
        return 1
    print(f"Корень OK, версия: {proc.stdout.strip()}\n")

    total_fail = 0
    for name, script in MODULES:
        print("\n" + "=" * 60)
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode != 0 and "performance" not in str(script):
            total_fail += 1

    print("\n" + "=" * 60)
    if total_fail:
        print(f"ЗАВЕРШЕНО С ОШИБКАМИ: {total_fail} модуль(ей)")
        return 1
    print("ВСЕ ТЕСТОВЫЕ МОДУЛИ ПРОЙДЕНЫ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
