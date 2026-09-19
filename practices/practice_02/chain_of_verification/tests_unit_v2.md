# Unit-проверки

| Требование или правило | Что проверяем изолированно | Вход | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| Формирование промпта | Метод ReviewService.review строит строку с префиксом и diff | diff = "X" | Вызов llm.generate с "Review this pull request and find problems:\nX" | app/review_service.py:19-21 |
| Схема ответа | Метод ReviewService.review возвращает словарь {comment: str} | answer = "ok" | {"comment": "ok"} | app/review_service.py:21-22 |
| Эндпоинт POST /api/reviews (валидный вход) | Функция create_review читает payload["diff"] и делегирует ReviewService | payload = {"diff": "D"} | Вызов review_service.review("D") и возврат его результата | app/api.py:35-37 |
| Отсутствует ключ diff | Прямой доступ payload["diff"] приводит к KeyError (текущее поведение) | payload = {} | Исключение KeyError и 5xx (как есть сейчас) | app/api.py:37; context.md:28-30,60 |
| Протокол LLM | Совместимость вызова llm.generate(prompt: str) -> str | prompt = "..." | Вызов llm.generate(prompt) допустим по протоколу | app/review_service.py:9-13,21 |

## Как использовали AI

- Анализ TRAINING_PR.diff, context.md и problem.md для выделения unit-поведения и рисков.
- Сформирован перечень проверочных вопросов и уточнены Evidence по строкам diff.
- Исправлены пробелы покрытия: добавлены строки про эндпоинт, негативный сценарий и протокол LLM.
