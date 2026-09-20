# Unit-проверки

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| Формирование промпта | Метод ReviewService.review строит строку с префиксом и diff | diff = "X" | Вызов llm.generate с "Review this pull request and find problems:\nX" | TRAINING_PR.diff: 19–21; context.md: 18 |
| Схема ответа | Метод ReviewService.review возвращает словарь {comment: str} | answer = "ok" | {"comment": "ok"} | TRAINING_PR.diff: 22; context.md: 18; 24; 29 |

## Как использовали AI

- Строка в prompts.md: P2-03
- Что проверили и исправили сами:
  - Заменили Evidence на разрешённые источники: TRAINING_PR.diff (19–22) и context.md (18; 24; 29) вместо ссылок на app/*.py.
  - Сопоставили формирование промпта и вызов llm.generate (TRAINING_PR.diff: 19–21; context.md: 18).
  - Подтвердили схему ответа {"comment": str} (TRAINING_PR.diff: 22; context.md: 24; 29).
