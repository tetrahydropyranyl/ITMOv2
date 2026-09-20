# Журнал экспериментов Практики 2

- Выбранный слабый артефакт Практики 1: [tests_unit.md](../practice_01/tests_unit.md)
- Что в нём нужно улучшить: полнота проверок (пустой `diff`, отсутствие ключа `diff`, ровно один вызов `llm.generate`), точность Evidence с номерами строк из [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff), сохранение исходного формата.
- Как поймём, что изменение полезно: каждая строка таблицы трассируется к [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff), [context.md](../practice_01/context.md), [problem.md](../practice_01/problem.md) с диапазонами строк; покрыты негативные и граничные сценарии; формат не изменён.

| Техника | Файл эксперимента | Изменённый файл Практики 1 | Конкретное изменение | Проверка | Что отклонили |
|---|---|---|---|---|---|
| Few-shot | [`few_shot/experiment.md`](few_shot/experiment.md) | [`tests_unit_v2.md`](few_shot/tests_unit_v2.md) | Добавлены кейсы: пустой `diff`, отсутствие ключа `diff`, ровно один вызов `llm.generate`; Evidence уточнены до строк TRAINING_PR.diff | Сопоставлено с [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff): app/review_service.py:19-22; app/api.py:35-37; с [context.md](../practice_01/context.md) | Новые колонки/изменение формата |
| R.C.T.F. | [`rctf/experiment.md`](rctf/experiment.md) | [`tests_unit_v2.md`](rctf/tests_unit_v2.md) | Заменили недопустимые Evidence на ссылки к TRAINING_PR.diff/context.md с диапазонами; уточнили формулировки без расширения формата | Проверено по [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff) и [context.md](../practice_01/context.md); ссылки на строки зафиксированы в артефакте | Ссылки на app/*.py и неподтверждённые требования |
| Chain of Verification | [`chain_of_verification/experiment.md`](chain_of_verification/experiment.md) | [`tests_unit_v2.md`](chain_of_verification/tests_unit_v2.md) | Добавлены 3 строки: делегирование POST /api/reviews, негатив отсутствия `diff`, соответствие протоколу LLM; Evidence уточнены | CoV-вопросы и подтверждения по [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff) и [context.md](../practice_01/context.md) | Изменение поведения/схемы ответа вне diff |
| Tree of Thoughts | [`tree_of_thoughts/experiment.md`](tree_of_thoughts/experiment.md) | [`tests_unit_v2.md`](tree_of_thoughts/tests_unit_v2.md) | Уточнили Evidence; добавили строки про кратность вызова `llm.generate`, пустой `diff`, делегирование из /api/reviews, негатив при отсутствии `diff` | Ручная валидация ссылок на [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff) | Расширение формата таблицы |
| RAG | [`rag/experiment.md`](rag/experiment.md) | [`tests_unit_v2.md`](rag/tests_unit_v2.md) | Evidence приведены к диапазонам разрешённых источников; добавлены «Ровно один вызов LLM», «Пустой diff», «Негатив: отсутствует `diff`»; уточнены формулировки | Каждая строка сопоставлена с [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff), [context.md](../practice_01/context.md), [problem.md](../practice_01/problem.md) | Требования вне TRAINING_PR.diff/context.md/problem.md |
| ReAct | [`react/experiment.md`](react/experiment.md) | [`tests_unit_v2.md`](react/tests_unit_v2.md) | Уточнили формулировки; добавили проверки на ровно один вызов, пустой `diff`, негатив отсутствия `diff`; поставили точные Evidence | Сверка с [TRAINING_PR.diff](../practice_01/TRAINING_PR.diff) (app/review_service.py; app/api.py) и выдержками из [context.md](../practice_01/context.md), [problem.md](../practice_01/problem.md) | Неподтверждённые утверждения и ссылки вне разрешённых источников |

## Независимое ревью

| Замечание другой команды | Где исправили | Evidence |
|---|---|---|
| Двусмысленность |  |  |
| Непроверяемое требование |  |  |
| Пропущенный риск или источник |  |  |
