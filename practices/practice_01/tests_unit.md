# Unit-проверки

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| Формирование промпта | Метод ReviewService.review строит строку с префиксом и diff | diff = "X" | Вызов llm.generate с "Review this pull request and find problems:\nX" | app/review_service.py:19-21 |
| Схема ответа | Метод ReviewService.review возвращает словарь {comment: str} | answer = "ok" | {"comment": "ok"} | app/review_service.py:21-22 |

## Как использовали AI

- Строка в [`prompts.md`](prompts.md):
- Что проверили и исправили сами:
  - P1-03
  - Утверждения выведены из TRAINING_PR.diff по конкретным строкам.
