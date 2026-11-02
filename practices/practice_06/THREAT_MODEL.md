# Threat Model — Mini Shop (до фиксов)

Контекст и границы
- Локальный HTTP (127.0.0.1), SQLite in-memory, файлы в sandbox (/tmp), без внешнего Интернета.
- Акторы: customer (alice/bob), staff, LLM Planner (Shop-Planner), серверный исполнитель инструментов.
- Активы: ПДн профилей, чеки пользователей, служебная записка, записи заказов.

Сценарии и угрозы (STRIDE)
- Spoofing: заголовок X-Role ранее давал роль.
- Tampering: delete_tree доступен всем залогиненным.
- Repudiation: логи сохраняют заголовки и тела.
- Information Disclosure: IDOR /profile, /orders, /files; /admin/export.
- Denial of Service: delete_tree удаляет учебные файлы.
- Elevation of Privilege: X-Role + инструменты ассистента без RBAC.

Контрмеры (план)
- Сессии: id и role только с сервера; игнорировать X-Role.
- SQL: параметризованные запросы и фильтры по owner.
- /files: привязка к владельцу; staff — подкаталог files/.
- Ассистент: RBAC на инструменты, ограничение путей.
- XSS: экранирование html в /reviews/view.

Проверка
- Атаки подтверждены до фиксов (см. evidence/before/), после фиксов — закрыты тестами.
