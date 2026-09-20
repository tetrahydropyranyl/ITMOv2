# Unit-проверки

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| Формирование промпта | Метод ReviewService.review строит строку с префиксом и diff | diff = "X" | Вызов llm.generate с строкой "Review this pull request and find problems:\nX" | app/review_service.py:19-21 |
| Схема ответа | Метод ReviewService.review возвращает словарь {comment: str} | answer = "ok" | {"comment": "ok"} | app/review_service.py:21-22 |
| Ровно один вызов llm.generate | Кратность и аргумент вызова LLM | diff = "X" | Ровно один вызов llm.generate с точным промптом, без дополнительных вызовов | app/review_service.py:19-22 |
| Пустой diff | Формирование промпта при пустой строке | diff = "" | Вызов llm.generate с "Review this pull request and find problems:\n" (существует перевод строки после двоеточия) | app/review_service.py:19-21 |
| Делегирование API | POST /api/reviews делегирует в review_service.review(payload["diff"]) | payload = {"diff": "D"} | Вызов review_service.review("D") и возврат его результата без изменений | app/api.py:35-37 |
| Негатив: отсутствует ключ diff | Поведение при отсутствии обязательного поля | payload = {} | Возникает KeyError на обращении payload["diff"] (риск 500 вместо 4xx) | app/api.py:37; practices/practice_01/context.md:28-30,60; practices/practice_01/problem.md:5-9 |

## Как использовали AI

- Что проверили и исправили сами:
  - Уточнили Evidence до конкретных строк исходников из TRAINING_PR.diff, context.md и problem.md.
  - Добавили негативный и граничный кейсы (пустой diff; отсутствие ключа diff).
  - Добавили проверку делегирования из POST /api/reviews в review_service.review.
