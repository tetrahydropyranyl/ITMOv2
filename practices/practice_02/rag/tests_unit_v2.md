# Unit-проверки

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| Формирование промпта | `ReviewService.review` строит строку с префиксом и `diff` | `diff = "X"` | Вызов `llm.generate` с `"Review this pull request and find problems:\nX"` | TRAINING_PR.diff: app/review_service.py:19-21 |
| Ровно один вызов LLM | `ReviewService.review` вызывает `llm.generate` один раз с точным промптом | `diff = "X"` | Ровно одна инвокация `llm.generate("Review this pull request and find problems:\nX")` | TRAINING_PR.diff: app/review_service.py:19-21 |
| Схема ответа | `ReviewService.review` возвращает словарь `{"comment": str}` | `answer = "ok"` | Возвращено `{"comment": "ok"}` | TRAINING_PR.diff: app/review_service.py:21-22; context.md: 24-25; 29-30 |
| Пустой `diff` | `ReviewService.review` при `diff = ""` | `diff = ""` | Вызов `llm.generate("Review this pull request and find problems:\n")`; структура ответа неизменна `{"comment": <строка>}` | TRAINING_PR.diff: app/review_service.py:19-22; context.md: 23-25 |
| Негатив: отсутствует ключ `diff` | `create_review(payload)` при отсутствии ключа | `payload = {}` | Бросается `KeyError` (текущее состояние, фиксируем риск) | TRAINING_PR.diff: app/api.py:35-37; context.md: 28-30; 49-61; problem.md: 5-9 |

## Как использовали AI

- Промпт: [prompt.md](./prompt.md)
- Что проверили и исправили сами:
  - Уточнили Evidence до диапазонов строк: TRAINING_PR.diff (app/review_service.py:19-22; app/api.py:35-37), context.md (23-25; 28-30; 49-61), problem.md (5-9).
  - Добавили граничный кейс пустого `diff`, негативный кейс отсутствия ключа `diff`, проверку ровно одного вызова `llm.generate`.
