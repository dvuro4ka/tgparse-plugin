# Проверки пакета TGParse

Дата: 03.11.2026. Claude Code 2.1.308, Codex CLI 0.161.0.
Сборка предназначена для собственного маркетплейса; публикация в официальные
каталоги и проверка в developer portal не выполнялись.

## Пакет и каталог Claude

Из корня репозитория:

```sh
claude plugin validate ./plugins/tgparse
claude plugin validate ./plugins/tgparse --profile directory --strict
claude plugin validate . --strict
python3 scripts/build_codex_compat.py --check
```

Все команды завершились с кодом 0. Обычная и строгая проверки каталога:
`These checks found nothing to report`, `Validation passed`.
Иконка действительно PNG, 1024 × 1024. В папке основного плагина находятся
README длиннее 40 слов, MIT LICENSE и метаданные издателя.
Локальный валидатор проверяет только часть требований каталога и не заменяет
проверку политики или безопасности в developer portal.

Навык `social-research` прошёл `quick_validate.py` из Skill Creator.
В нём объединены два навыка из TGParse `origin/main` (`3365bfd`):
`plugins/tgparse-social-research/skills/analyze-social-content/`
и `plugins/tgparse-claude-code/skills/social-research/`.
Иконка и ссылки на документы взяты из того же снимка исходного репозитория.

## Установка в изолированном окружении

Claude запускался с отдельным `CLAUDE_CONFIG_DIR`, Codex — с отдельным
`CODEX_HOME`, вне рабочего каталога пользователя.
Пользовательские постоянные конфигурации не изменялись.

```sh
claude plugin marketplace add /absolute/path/to/tgparse-plugin
claude plugin install tgparse@tgparse
claude plugin list
claude plugin details tgparse
```

Результат: плагин 1.0.0 включён; inventory — один навык `social-research`,
один MCP-сервер `tgparse`, ноль агентов и hooks.

```sh
codex plugin marketplace add /absolute/path/to/tgparse-plugin --json
codex plugin add tgparse@tgparse --json
codex plugin marketplace list
codex plugin list
```

Результат: маркетплейс `tgparse` добавлен, плагин 1.0.0 установлен и включён,
политика авторизации `ON_INSTALL`.
В финальном каталоге путь источника — `./plugins/tgparse-codex`.

Дополнительно через локальный `codex app-server --stdio` выполнен
`plugin/read`: он видит `mcpServers: ["tgparse"]` и навык
`tgparse:social-research`. Проверка установки не ограничивалась записью
плагина в список. Вход через Telegram в Codex не выполнялся.

Установка именно по GitHub-адресу не проверялась: изменения по условию
закоммичены только локально, удалённый репозиторий ещё не содержит пакет.
После публикации владельцем используются команды из README.

## Загрузка Claude без авторизации TGParse

Проверено с отдельным пустым каталогом конфигурации, без OAuth-токенов
и без пользовательских API-ключей:

```sh
claude --plugin-dir /absolute/path/to/tgparse-plugin/plugins/tgparse \
  --setting-sources "" --no-session-persistence \
  --debug-file /temporary/path/claude-load.log -p /mcp
```

Плагин загрузился, сервер определился как `plugin:tgparse:tgparse`.
Журнал показал успешный HTTP handshake с сервером TGParse 2.0.0,
согласованную версию `2025-11-25`, затем при получении инструментов:

```text
Authentication required; client registration is deferred until the user authenticates
```

Краткий вывод `-p /mcp` успел показать «1 connected» до отказа в чтении
инструментов; состояние авторизации подтверждено журналом.
Регистрация OAuth-клиента отложена, вход не выполнялся, инструменты и
платные действия не вызывались. БД, Railway CLI и настройки продакшена
не использовались.

## Расхождение Agent Plugins и OpenAI

[Схема plugin.json 1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
валидирует основной `plugins/tgparse/plugin.json` без ошибок.

[Схема mcp.json 1.0.0](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json)
задаёт для серверной записи `additionalProperties: false` и не разрешает
`extensions`. При этом
[OpenAI](https://developers.openai.com/plugins/build/plugins#configure-mcp-authentication)
предписывает OAuth именно в `mcpServers.<name>.extensions["com.openai"].auth`.
Поэтому полная проверка `mcp.json` этой базовой схемой **не проходит**;
проверка переносимых полей без OpenAI-расширения проходит.
Это ограничение не скрывается и не устраняется ослаблением исходной схемы.

Эксперимент с Codex 0.161.0 подтвердил влияние на загрузку:
с OAuth-расширением `plugin/read` возвращал пустой список серверов;
без расширения видел `tgparse`. Декларация пути `mcpServers` в inline-overlay
корневого манифеста это не исправила.

Для работающей установки через Codex/OpenAI-маркетплейс добавлена
совместимая сборка `plugins/tgparse-codex/` с поддерживаемыми
`.codex-plugin/plugin.json` и `.mcp.json` (`type: http`).
Она не содержит переносимого `plugin.json`, чтобы клиент действительно
использовал совместимый формат. OAuth обнаруживается клиентом по серверу.
Общий исходник навыка, README, лицензии и ресурсов находится в
`plugins/tgparse/`; `scripts/build_codex_compat.py` копирует их в сборку,
а `--check` обнаруживает рассинхронизацию. Копии — обычные Git-файлы,
не symlink; скрипт не выполняется при установке.

Основной пакет сохраняет переносимый формат, OpenAI auth с предпочтением CIMD
и Claude-манифест. Строгая совместимость с произвольным Agent Plugins-клиентом,
проверяющим нынешнюю закрытую MCP-схему, пока не гарантируется.
После исправления схемы/загрузчика можно убрать совместимую сборку,
изменив источник в каталоге OpenAI и заново проверив реальную загрузку.

## Полный pytest TGParse

Серверный код пакетом не изменяется. Для контрольного прогона взят чистый
снимок `origin/main` TGParse (`3365bfd`) через `git archive` в отдельную
временную папку: без рабочего `.env` и производственных настроек.

```sh
TELEGRAM_BOT_TOKEN=1:x /srv/bb/tmp/tgparse-merge-1410/venv/bin/python -m pytest -q
```

Результат: **1444 passed, 9 skipped, 11 warnings in 515.37s (0:08:35)**,
код завершения 0. Предупреждения относятся к устаревшим API зависимостей
и конфигурации pytest-asyncio. Этот прогон подтверждает состояние серверного
снимка, но не заменяет авторизованные проверки плагина в клиентах.

## Протокол и ручная проверка

[MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
меняет handshake и метаданные запросов. Пакет не задаёт protocolVersion.
Наблюдаемый сервер пока согласовал 2025-11-25; его обновление — отдельная задача.
[MCP Apps](https://apps.extensions.modelcontextprotocol.io/api/) предоставляет
UI-расширение сервера; один пакет плагина не добавляет поддержку этого UI.

Вручную после публикации проверить:

- Установку по `dvuro4ka/tgparse-plugin` в Claude Code и Codex.
- Add marketplace, Connectors и вход через Telegram в claude.ai/Desktop/Cowork.
- Личное MCP-подключение в ChatGPT и полный пакет в поддерживаемом desktop/Work.
- Возврат из OAuth, повторный вход после отзыва доступа, видимость инструментов.
- Анализ, скачивание и `get_account` на тестовом аккаунте.
- Один явно согласованный заказ уникализации: баланс, сохранение `request_id`,
  отсутствие дубля при повторе, ожидание готовности, Telegram-доставка,
  сроки прямой ссылки и страницы результата.

Ни OAuth, ни оплачиваемые сценарии этой проверкой не подтверждены.
