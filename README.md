# TGParse

Плагин для исследования публичных аккаунтов соцсетей и работы с видео.
Сравнивайте конкурентов, находите сильные темы и сценарии, получайте метрики
публикаций и расшифровки. Скачивайте ролики, проверяйте тариф и баланс,
заказывайте уникализацию только тогда, когда она нужна.
Поддержка: [@parser_ai](https://t.me/parser_ai).

Сервер: `https://tgparse-production.up.railway.app/mcp`.
Вход — OAuth с подтверждением через Telegram. Ключи, токены и секреты
в пакет не входят. Отдельный локальный процесс или установка зависимостей
для использования плагина не нужны.

## Claude Code

В сессии Claude Code:

```text
/plugin marketplace add dvuro4ka/tgparse-plugin
/plugin install tgparse@tgparse
```

После установки откройте `/mcp`, выберите сервер TGParse и Authenticate,
затем подтвердите вход через Telegram.
Навык доступен как `/tgparse:social-research` и подбирается автоматически
по запросам о соцсетях и видео.

Команды из терминала:

```sh
claude plugin marketplace add dvuro4ka/tgparse-plugin
claude plugin install tgparse@tgparse
```

Для проверки рабочей копии без установки:

```sh
claude --plugin-dir ./plugins/tgparse
```

## claude.ai, Claude Desktop и Cowork

1. Откройте Customize → Plugins → Add → Add marketplace.
2. Укажите `dvuro4ka/tgparse-plugin` (либо полный URL этого репозитория).
3. Выберите TGParse и установите плагин.
4. На вкладке Connectors плагина добавьте/подключите TGParse
   и подтвердите OAuth-вход через Telegram.
5. В новом разговоре попросите, например: «Сравни эти два аккаунта».

Если организационные настройки запрещают сторонние маркетплейсы или коннекторы,
подключение должен разрешить администратор.
На Team/Enterprise владелец добавляет коннектор для организации,
а пользователь подключает свой аккаунт.

Можно загрузить пакет вручную: создайте ZIP содержимого `plugins/tgparse/`
(с `.claude-plugin/` и `.mcp.json`), затем
Customize → Plugins → Add → Upload plugin. Корнем архива должна быть папка плагина,
а не весь репозиторий с каталогами маркетплейсов.

## Codex

Проверено на Codex CLI 0.161.0:

```sh
codex plugin marketplace add dvuro4ka/tgparse-plugin
codex plugin add tgparse@tgparse
codex plugin list
```

Правильный путь команд — `codex plugin marketplace`; отдельной команды
`codex marketplace` в этой версии нет.
После установки пройдите авторизацию подключения TGParse через OAuth/Telegram
в интерфейсе клиента. Вызовы инструментов требуют входа.

Для локальной рабочей копии замените GitHub-источник абсолютным путём к
корню репозитория:

```sh
codex plugin marketplace add /absolute/path/to/tgparse-plugin
codex plugin add tgparse@tgparse
```

Основной пакет `plugins/tgparse/` использует переносимые `plugin.json` и `mcp.json`.
OAuth объявлен как `extensions["com.openai"].auth` записи сервера:
`type: oauth`, `client.mode: cimd`. Это предпочтение CIMD с возможностью
DCR fallback со стороны поддерживающего клиента; статических client ID и секретов нет.
Codex 0.161.0 пропускает запись сервера с этим расширением, поэтому каталог OpenAI
устанавливает совместимую сборку `plugins/tgparse-codex/`: `.codex-plugin/plugin.json`
и `.mcp.json` с OAuth discovery клиента. Имя плагина, сервер и навык те же.
Ограничение базовой JSON Schema и результаты проверки описаны в
[протоколе](docs/VALIDATION.md).

## ChatGPT

Для личного плагина с инструментами сервера:

1. Откройте Plugins → + → Add custom MCP server.
2. Задайте имя TGParse и URL `https://tgparse-production.up.railway.app/mcp`.
3. Выберите OAuth. Не вводите выдуманный client ID или API-ключ:
   используйте автоматическое обнаружение/регистрацию клиента.
4. Прочитайте предупреждение интерфейса и выберите Create as a plugin.
5. Подтвердите вход в Telegram и включите TGParse в разговоре.

Так подключаются инструменты MCP. Навык из этого репозитория не переносится
автоматически при создании подключения по URL.

Полный пакет со skills можно устанавливать через локальный каталог в
поддерживаемом ChatGPT desktop/Work. Клонируйте репозиторий, откройте его как
проект в клиенте: здесь уже есть `.agents/plugins/marketplace.json`.
Перезапустите клиент, в Plugins Directory выберите источник TGParse
и установите плагин. Либо добавьте этот репозиторий командой Codex выше
в том же локальном окружении. Наличие этого источника зависит от поверхности
и настроек аккаунта. Эти пути не заменяют личное MCP-подключение в веб-клиенте:
универсальная установка произвольного GitHub-пакета через веб-интерфейс
в проверенной документации не описана.

Пакет не содержит `.app.json` с чужим `plugin_asdk_app...`:
идентификатор личного подключения создаётся ChatGPT для конкретного аккаунта.

## Инструменты

| Задача | Инструменты |
| --- | --- |
| Профиль и анализ аккаунта | `get_profile`, `analyze_profile` |
| Сравнение 2–5 аккаунтов | `compare_profiles` |
| Метрики публикации | `get_media_metrics` |
| Расшифровка одного / до 10 видео | `get_transcript`, `get_transcripts` |
| Поиск тем и похожих роликов | `search_content`, `find_similar_content` |
| Скачать видео Instagram / YouTube / TikTok | `download_video` |
| Баланс, тариф, квоты и ссылки на покупку | `get_account` |
| Создать заказ уникализации | `create_versions` |
| Статус, готовые файлы и история | `get_versions_order`, `list_versions_orders` |

Поддерживаемые площадки и параметры определяет текущая схема сервера.
Сервер применяет тарифы, квоты и ограничения аккаунта.
Покупка выполняется в боте или Mini App, по ссылкам из `get_account`.

Уникализация запускается по явной просьбе, после проверки баланса, выбора
количества и режима. Повторы одного заказа сохраняют `request_id` и параметры,
а готовность проверяется по `order_id` с паузами.
Ссылки на скачанные видео и версии временные; фактический срок возвращает сервер.
Версии также доставляются в личный Telegram.

## Данные и приватность

Плагин отправляет на сервер TGParse указанные аккаунты и ссылки, поисковые фразы,
параметры анализа, расшифровки, скачивания и уникализации.
OAuth связывает подключение с вашим Telegram; идентификатор пользователя
используется для квот, баланса и доступа к вашим заказам.
Для обработки сервер получает исходное видео. Результаты, расшифровки,
метрики и ссылки возвращаются в выбранный AI-клиент; готовые версии также
отправляются в Telegram. Сервис может обращаться к поставщикам данных
и распознавания согласно своей политике конфиденциальности.

Сам пакет не запускает скрипты, не считывает рабочие файлы и не содержит секретов.
Приватные ссылки дают доступ к файлам до истечения срока: не публикуйте их.
Хранение и обработка регулируются условиями TGParse и выбранного AI-клиента.

- [Политика конфиденциальности](https://telegra.ph/POLITIKA-KONFIDENCIALNOSTI-07-24-157)
- [Пользовательское соглашение](https://telegra.ph/POLZOVATELSKOE-SOGLASHENIE-07-24-55)
- [Поддержка — @parser_ai](https://t.me/parser_ai)

## Структура и проверка

```text
.claude-plugin/marketplace.json       # каталог Claude
.agents/plugins/marketplace.json     # каталог Codex / OpenAI
plugins/tgparse/
  plugin.json                       # Agent Plugins + OpenAI interface
  mcp.json                          # Streamable HTTP + OAuth
  .claude-plugin/plugin.json         # Claude
  .mcp.json                         # Claude HTTP
  skills/social-research/SKILL.md    # общий навык
  assets/tgparse.svg
  assets/tgparse.png                 # 1024 × 1024
  README.md
  LICENSE
plugins/tgparse-codex/               # сборка для Codex 0.161 / OpenAI desktop
  .codex-plugin/plugin.json
  .mcp.json
  skills/, assets/, README.md, LICENSE
scripts/build_codex_compat.py        # синхронизация сборки из общего пакета
```

```sh
claude plugin validate ./plugins/tgparse
claude plugin validate ./plugins/tgparse --profile directory --strict
claude plugin validate . --strict
```

Редактируйте общий навык и ресурсы в `plugins/tgparse/`, затем выполните:

```sh
python3 scripts/build_codex_compat.py
python3 scripts/build_codex_compat.py --check
```

Сборка уже включена в Git; при установке Python не нужен. Проверка `--check`
обнаруживает любые расхождения файлов, включая навык, метаданные и иконку.

[Протокол и результаты проверок](docs/VALIDATION.md) ·
[Текст для /connect](docs/CONNECT.md).

Форматы сверены 03.11.2026:
[Claude: структура](https://claude.com/docs/plugins/build),
[проверки каталога](https://claude.com/docs/plugins/pre-submission-checklist),
[OpenAI: пакет и маркетплейсы](https://developers.openai.com/plugins/build/plugins),
[Agent Plugins: схемы](https://agent-plugins.org/schemas).
Текущая ревизия [MCP — 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog);
пакет не фиксирует protocolVersion и использует согласование клиента с сервером.
[MCP Apps](https://apps.extensions.modelcontextprotocol.io/api/) — отдельное
расширение для встроенного UI; этот пакет не добавляет серверу UI-ресурсы.

Код пакета — [MIT](LICENSE). В официальные каталоги пакет не подаётся.
