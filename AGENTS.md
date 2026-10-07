# Агентские правила проекта

Этот файл читается агентами как часть инструкций. Основные правила:

1. Использовать skill `api-contract-smoke` для быстрой проверки ключевых эндпоинтов и готовности сервиса.
2. После правок backend или OpenAPI запускать smoke перед коммитом или в pre-push.
3. Сохранять отчёты в `.opencode/skills/api-contract-smoke/reports/` и прикладывать к защите.
4. Не расширять список эндпоинтов более 4 — это smoke, не полный тест.

Конфигурация smoke не привязана к проекту: 
- Укажите путь к конфигу через переменную окружения `API_SMOKE_CONFIG`, либо создайте `config/api_smoke.json`.
- Если ни один из вариантов не найден, хук pre-push пропустит проверку.

## Git hook pre-push

- Хук хранится в `.opencode/hooks/pre-push`. Для активации создайте симлинк:
  `ln -sf ../../.opencode/hooks/pre-push .git/hooks/pre-push && chmod +x .opencode/hooks/pre-push`
- Хук запускает `.opencode/scripts/api_contract_smoke.py` с конфигом `config/local_example.json` и блокирует пуш при FAIL.
- Отчёт: `.opencode/skills/api-contract-smoke/reports/pre_push.md`.

## MCP: RepoGuard

- В проект добавлен MCP-сервер RepoGuard (`practices/practice_04/mcp/server.py`), который предоставляет инструменты:
  - `scan_secrets(path?, include_exts?, exclude_dirs?)` — сканирует репозиторий/папку на наличие секретов.
  - `rules()` — возвращает список применяемых правил.
- Сервер подключён к OpenCode через `opencode.json` (`mcp.repo-guard`), запускается локально через `./.venv/bin/mcp run practices/practice_04/mcp/server.py`.
- Среда: Python venv в `.venv`, зависимости в корневом `requirements.txt` (`mcp[cli]`).
- Агент может вызывать `scan_secrets` для всей папки `ITMOv2` (путь по умолчанию — `REPO_ROOT=.`).
