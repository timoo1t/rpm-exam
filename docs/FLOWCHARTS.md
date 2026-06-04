# Блок-схемы проекта «Каталог библиотеки»

## 1. Общая структура Git-проекта

```mermaid
flowchart TB
    subgraph ROOT["Корень репозитория C:/Users/Ваня/Desktop/123"]
        MAIN["main.py<br/>ТОЧКА ВХОДА"]
        README["README.md"]
        subgraph SRC["src/library_catalog/"]
            VAL["validators.py<br/>Валидация"]
            MOD["models.py<br/>Модели"]
            SVC["service.py<br/>Бизнес-логика"]
            CLI["cli.py<br/>Интерфейс"]
        end
        subgraph TESTS["tests/"]
            RUN["run_all_tests.py"]
            VER["verification/"]
            VALT["validation/"]
            USR["usability/"]
            PERF["performance/"]
        end
        DOCS["docs/"]
    end
    MAIN --> CLI
    MAIN --> SVC
    CLI --> SVC
    SVC --> VAL
    SVC --> MOD
    RUN --> MAIN
    RUN --> VER
    RUN --> VALT
    RUN --> USR
    RUN --> PERF
    VER --> MAIN
    VER --> SVC
    VALT --> MAIN
    VALT --> VAL
    USR --> MAIN
    USR --> CLI
    PERF --> SVC
```

## 2. Блок-схема корня программы (main.py)

```mermaid
flowchart TD
    A([Старт main.py]) --> B{Аргументы?}
    B -->|--version| C[Вывести версию]
    B -->|--demo| D[run_demo]
    B -->|нет флагов| E[run_interactive CLI]
    B -->|--help| F[Справка argparse]
    C --> Z([exit 0])
    F --> Z
    D --> D1[Создать LibraryService]
    D1 --> D2[add / search / borrow / list]
    D2 --> Z
    E --> E1{Цикл ввода}
    E1 -->|exit| Z
    E1 -->|команда| E2[Разбор команды]
    E2 --> E3[Вызов service / help]
    E3 --> E1
```

## 3. Модуль service.py (бизнес-логика)

```mermaid
flowchart TD
    A([Вызов метода service]) --> B{Метод?}
    B -->|add_book| C[validate isbn, title, author, year]
    C --> D{Все OK?}
    D -->|нет| E[OperationResult success=False]
    D -->|да| F{ISBN есть?}
    F -->|да| G[Ошибка: дубликат]
    F -->|нет| H[Сохранить Book]
    H --> I[success=True]
    B -->|search| J[query пустой?]
    J -->|да| K[пустой список]
    J -->|нет| L[Фильтр + сортировка]
    B -->|borrow| M[find_by_isbn]
    M --> N{найдена и available?}
    N -->|нет| E
    N -->|да| O[available=False]
    B -->|return_book| P[find + проверка выдана]
    P --> Q[available=True]
```

## 4. Модуль validators.py

```mermaid
flowchart TD
    A([validate_*]) --> B{Поле пустое?}
    B -->|да| C[False + сообщение]
    B -->|нет| D{Тип проверки}
    D -->|ISBN| E[10 или 13 цифр?]
    D -->|title/author| F[длина в пределах?]
    D -->|year| G[1000..2100 int?]
    E -->|нет| C
    E -->|да| H[True + нормализованное значение]
    F --> H
    G --> H
```

## 5. Подсхема: тест верификации

```mermaid
flowchart TD
    A([test_verification.py]) --> B[Импорт через _bootstrap]
    B --> C{Тест API или корня?}
    C -->|API| D[LibraryService в памяти]
    C -->|корень| E[subprocess: python main.py]
    D --> F[Проверка по ТЗ]
    E --> G["--version / --demo"]
    F --> H{assert OK?}
    G --> H
    H -->|да| I[[OK]]
    H -->|нет| J[[FAIL]]
```

## 6. Подсхема: тест валидации

```mermaid
flowchart TD
    A([test_validation.py]) --> B[Корректные данные]
    A --> C[Некорректные: ISBN, год, пусто]
    B --> D[Ожидание success=True]
    C --> E[Ожидание success=False]
    A --> F[main.py --unknown-flag]
    F --> G[returncode != 0]
    D --> H{Итог}
    E --> H
    G --> H
```

## 7. Подсхема: тест юзабилити

```mermaid
flowchart TD
    A([test_usability.py]) --> B[HELP_TEXT]
    B --> C[Все команды + русский язык]
    A --> D[run_batch_commands]
    D --> E[Пустой каталог / неизвестная команда]
    A --> F[main.py --help / --demo]
    F --> G[Понятный вывод, без лишних ошибок в stderr]
```

## 8. Подсхема: нагрузочный тест

```mermaid
flowchart TD
    A([benchmark.py]) --> B[Для N in 100, 500, 1000, 5000]
    B --> C[Генерация N книг]
    C --> D[tracemalloc.start]
    D --> E[load_bulk + замер времени]
    E --> F[search + list_all]
    F --> G[peak memory KB]
    G --> H[Запись строки в таблицу]
    H --> B
    B -->|конец| I[benchmark_results.json]
```

## 9. run_all_tests.py

```mermaid
flowchart TD
    A([run_all_tests.py]) --> B[python main.py --version]
    B --> C{OK?}
    C -->|нет| D([exit 1])
    C -->|да| E[verification]
    E --> F[validation]
    F --> G[usability]
    G --> H[benchmark]
    H --> I{Ошибки?}
    I -->|нет| J([exit 0])
    I -->|да| D
```
