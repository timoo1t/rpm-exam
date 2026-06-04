# Каталог библиотеки — проект для экзамена РПМ

Учебный проект: консольный каталог книг с тестами верификации, валидации, юзабилити и нагрузочным тестированием.

## Корень программы

```
main.py
```

## Быстрый старт

```bash
cd C:\Users\Ваня\Desktop\123
python main.py --demo
python tests\run_all_tests.py
python tests\performance\benchmark.py
```

## Структура

- `src/library_catalog/` — модули приложения
- `tests/verification/` — верификация (ТЗ)
- `tests/validation/` — валидация (ввод данных)
- `tests/usability/` — юзабилити (CLI)
- `tests/performance/` — скорость и память
- `docs/RPM_REPORT.md` — отчёт для сдачи
- `docs/FLOWCHARTS.md` — блок-схемы (Mermaid)
- `docs/uml/` — UML-диаграммы кода (PNG): классы, последовательность, компоненты, прецеденты

## Требования

Python 3.10 или новее.
