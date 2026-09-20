# Unit-проверки

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| Формирование промпта | `ReviewService.review` строит строку с точным префиксом и подставляет `diff` | diff = "X" | Сформирован prompt: "Review this pull request and find problems:\nX" | TRAINING_PR.diff: app/review_service.py:19-20; context.md: 18-19 |
| Ровно один вызов LLM | `ReviewService.review` вызывает `llm.generate` один раз с собранным prompt | diff = "X" | Одна инвокация `llm.generate("Review this pull request and find problems:\nX")` | TRAINING_PR.diff: app/review_service.py:20-21; context.md: 18-19 |
| Схема ответа фиксирована | `ReviewService.review` возвращает словарь с комментарием | answer = "ok" | {"comment": "ok"} | TRAINING_PR.diff: app/review_service.py:21-22; context.md: 24-25; 29 |
| Пустой diff не меняет контракт | Поведение `ReviewService.review` при `diff = ""` | diff = "" | Вызов `llm.generate("Review this pull request and find problems:\n")`; возврат {"comment": <строка>} | TRAINING_PR.diff: app/review_service.py:19-22; context.md: 24-25; 29 |
| Текущее поведение create_review при отсутствии ключа | `create_review(payload)` обращается к `payload["diff"]` | payload = {} | `KeyError` (риск 5xx в текущей реализации) | TRAINING_PR.diff: app/api.py:35-37; context.md: 28; 51-60; problem.md: 5-9 |

## Как использовали AI

- Промпт: practices/practice_02/react/prompt.md
- Что проверили и исправили сами:
  - Уточнили формирование промпта и единичный вызов LLM по TRAINING_PR.diff: app/review_service.py:19-21; context.md: 18-19.
  - Зафиксировали схему ответа по TRAINING_PR.diff: app/review_service.py:21-22; context.md: 24-25; 29.
  - Добавили граничный случай пустого diff по TRAINING_PR.diff: app/review_service.py:19-22; context.md: 24-25; 29.
  - Добавили негативный кейс отсутствующего ключа `diff` по TRAINING_PR.diff: app/api.py:35-37; context.md: 28; 51-60; problem.md: 5-9.
