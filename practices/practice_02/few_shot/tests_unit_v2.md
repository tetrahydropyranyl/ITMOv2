# Unit-проверки

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| Формирование промпта | `ReviewService.review` строит строку с точным префиксом и передаёт `diff` без модификаций | diff = "X" | Вызов `llm.generate` с `"Review this pull request and find problems:\nX"` | app/review_service.py:19-21 |
| Ровно один вызов LLM | `ReviewService.review` вызывает `llm.generate` один раз | diff = "X" | Ровно одна инвокация `llm.generate` с ожидаемым промптом | app/review_service.py:21 |
| Схема ответа | `ReviewService.review` возвращает словарь `{comment: str}` | answer = "ok" (из фейкового LLM) | `{"comment": "ok"}` | app/review_service.py:21-22 |
| Пустой diff | `ReviewService.review` корректно обрабатывает пустой `diff` | diff = "" | Вызов `llm.generate` с `"Review this pull request and find problems:\n"`; возврат структуры `{"comment": <строка>}` | app/review_service.py:19-22 |
| Негативный кейс API | Функция `create_review(payload)` при отсутствии ключа `"diff"` | payload = {} | Бросается `KeyError` (фиксирует текущий риск реализации) | app/api.py:35-37 |

## Как использовали AI

- Строка в [prompts.md](../prompts.md): Few Shot для уточнения покрытия и Evidence.
- Что проверили и исправили сами:
  - Уточнили Evidence до конкретных строк из TRAINING_PR.diff.
  - Добавили негативный кейс для отсутствующего ключа `diff` и граничный кейс пустого `diff`.
  - Зафиксировали требование ровно одного вызова `llm.generate` с точным промптом.
