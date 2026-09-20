# R.C.T.F.

- **Role:** Ты — R.C.T.F.-агент, старший инженер по качеству и документации. Анализируешь артефакт unit-проверок и готовишь улучшенную версию.
- **Context:** Целевой файл: practices/practice_01/tests_unit.md. Разрешённые источники: practices/practice_01/TRAINING_PR.diff, practices/practice_01/context.md и practices/practice_01/problem.md.
- **Task:** Найти слабые места в tests_unit.md (evidence/AI-раздел/формулировки), подготовить исправленную версию по тому же формату и сохранить её в practices/practice_02/rctf/tests_unit_v2.md. Затем обновить текущий файл: в «Что получили» добавить Markdown-ссылку на tests_unit_v2.md и заполнить остальные разделы.
- **Format:** Сохранить структуру: заголовок, таблица с колонками, раздел «## Как использовали AI». Evidence — только TRAINING_PR.diff/context.md/problem.md с номерами строк. Язык — русский.

## Полный запрос

 См. [prompt.md](practices/practice_02/rctf/prompt.md)
## Что получили

 - Сгенерирован обновлённый артефакт unit-проверок: [tests_unit_v2.md](practices/practice_02/rctf/tests_unit_v2.md)
## Что изменили в исходном артефакте

- Файл и раздел:
- Изменение:
  - Обновлены Evidence-ссылки: заменены недопустимые ссылки на app/*.py на TRAINING_PR.diff и context.md с построчными диапазонами.
  - Раздел «Как использовали AI» заполнен: добавлена строка в prompts.md и перечислены собственные проверки с построчными ссылками.
  - Уточнены формулировки требований и ожидаемых результатов без добавления неподтверждённых фактов.
- Как проверили:
  - Формирование промпта и вызов llm.generate: TRAINING_PR.diff: 19–21; context.md: 18.
  - Схема ответа {"comment": str}: TRAINING_PR.diff: 22; context.md: 24; 29.
- Что отклонили:
  - Любые ссылки на запрещённые источники (app/*.py и т.п.).
  - Неподтверждённые требования вне TRAINING_PR.diff/context.md/problem.md.
