# UML-диаграммы проекта «Каталог библиотеки»

PNG-версии сгенерированы из исходников Mermaid (`.mmd`).

| Файл | Описание |
|------|----------|
| `class_diagram.png` | Диаграмма классов — модели, сервис, валидаторы, CLI |
| `sequence_add_book.png` | Диаграмма последовательности — добавление книги |
| `component_diagram.png` | Компонентная диаграмма — модули и тесты |
| `use_case.png` | Диаграмма прецедентов — сценарии использования |

Пересборка PNG (нужен Node.js):

```bash
npx @mermaid-js/mermaid-cli -i docs/uml/class_diagram.mmd -o docs/uml/class_diagram.png -b white
npx @mermaid-js/mermaid-cli -i docs/uml/sequence_add_book.mmd -o docs/uml/sequence_add_book.png -b white
npx @mermaid-js/mermaid-cli -i docs/uml/component_diagram.mmd -o docs/uml/component_diagram.png -b white
npx @mermaid-js/mermaid-cli -i docs/uml/use_case.mmd -o docs/uml/use_case.png -b white
```
