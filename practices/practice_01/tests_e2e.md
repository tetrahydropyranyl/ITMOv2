# E2E-проверки

| Сценарий пользователя | Предусловия | Действие | Наблюдаемый результат | Evidence |
|---|---|---|---|---|
| Позитивный | Запущено API | POST /api/reviews с телом {"diff": "diff --git a/x b/x\n..."} | 200 OK, тело содержит ключ comment | app/api.py:35-37; app/review_service.py:19-22 |
| Негативный | Запущено API | POST /api/reviews с пустым телом {} | Ошибка из-за KeyError (ожидаем 500 в текущей реализации) | app/api.py:37 |
| Граничный | Запущено API | POST /api/reviews с минимальным diff, напр. "" (пустая строка) | 200 OK, возврат {comment: str} как есть от LLM | app/review_service.py:19-22 |

## Как использовали AI

- Строка в [`prompts.md`](prompts.md): P1-03
- Что проверили и исправили сами:
  - P1-03
  - Сопоставили сценарии с линиями TRAINING_PR.diff.
