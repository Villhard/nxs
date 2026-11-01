# Участие в разработке

Прочитай до правок. `CLAUDE.md` и `AGENTS.md` - равнозначные точки входа.

## Структура

Скилл - самостоятельный каталог, устанавливаемый отдельно:

```text
skills/<name>/
  SKILL.md                     # frontmatter: name, description; необязательные argument-hint, disable-model-invocation
  agents/openai.yaml           # необязательная политика вызова Codex
  references/                  # правила, читаемые по необходимости
  assets/                      # шаблоны документов
  roles/                       # независимые reviewer roles dev-review
tests/client-scenarios.md
README.md CONTRIBUTING.md CHANGELOG.md
```

Ссылки скилла ведут только внутрь его каталога. Общие ресурсы копируй реальным потребителям побайтово, без зависимости от developer checkout, helper или другой установки.

| Владелец | Ресурсы |
| --- | --- |
| `rnd-grill` | Обсуждение, предметная область, методы исследования/опыты, шаблоны решения, описания функции и опросника. |
| `rnd-debug` | Диагностика и поиск каталога функции. |
| `dev-exec` | Контекст исполнения, деление работы, tickets и handoff с правилами/шаблонами. |
| `dev-review` | Снимок, замечания, отчет, native launch и четыре роли; не создает tickets. |
| `dev-spec` | Чтение проектных спецификаций и их шаблон. |
| `dev-commit` | Безопасность/формат коммитов. |
| `nxs-setup` | Шаблоны настройки, готовность, возможности и написание инструкций. |

`skills/dev-spec/references/project-specs.md` копируй в `rnd-grill`, `rnd-debug`, `dev-exec`, `dev-review`. Ticket rules/template только у `dev-exec`, feature-description template - у `rnd-grill`, не диагностики. Не требуй общих копий без потребителей. Блок "Условия завершения" для setup tracker копируй дословно из `skills/dev-exec/assets/ticket.md` в `skills/nxs-setup/assets/issue-tracker.md`. Каталог потребителей checker обновляй при переносе ресурсов.

Старые пользовательские tickets, журналы, решения, прототипы и worktrees не мигрируй/не удаляй. В прямом процессе нет обязательных journal, controlled-run packet, approval hashes, locks и worker envelope. Конфликт старых инструкций разрешай явно, не эмулируй удаленное.

Правила процесса держи у владельца/роли, общие - в одной shared reference с одинаковыми копиями. Личные предпочтения - в client/project instructions. Исключение setup: он пишет правила/config туда только точным одобренным diff. Не добавляй background skills, cross-skill injection и hooks. Новый скилл нужен лишь для отдельного устоявшегося частого намерения; иначе расширяй имеющийся.

## Имена

Имя - команда пользователя: короткое, понятное с первого взгляда, без конфликтов с клиентом/установленными скиллами. Пространства: `rnd-` для исследования, `dev-` для разработки, `nxs-` для настройки. При совпадении проверь путь/provenance; имя не запускает следующую стадию. [ADR 0007](docs/adr/0007-skill-names.md) - прежнее решение, [ADR 0009](docs/adr/0009-seven-skill-direct-flow.md) - семь сохраненных имен вместо прежнего фиксированного префикса/каталога.

## Язык и безопасность

Пиши кратко и по-русски, с ASCII-дефисом и прямыми кавычками. Заголовки инструкций - ПРОПИСНЫМИ, README и CHANGELOG - обычным регистром. Заголовки артефактов тоже русские; служебные ключи, статусы, пути и технические термины сохраняются. Старые артефакты читаются с прежними заголовками без автоматической миграции.

Не публикуй частные пути/remotes, tracker IDs, секреты, environment values, личные контакты и raw sessions. Примеры нейтральные.

## Контракты инструкций

README объясняет использование, CONTRIBUTING - изменение. Полные правила исполнения принадлежат skills/roles/references: ссылайся вместо пересказа. Имена моделей и оценки не включай в руководства.

- Укажи вход, проверки входа, порядок, результат, остановки и передачу. Исключения рядом с шагом, конкурирующие состояния таблицей.
- Description задает конкретный trigger, результат и отличие соседних команд; вызов отделен от обсуждения/внутреннего действия.
- Поля шаблона помечай обязательными/необязательными; структурные имена сохраняй, выполненное отличай от удаленного требования.
- Установленный скилл самодостаточен, bundled resources читаются по месту нужды; root docs не runtime context.
- Используй согласие в его пределах, недостающие доказательства называй.
- Проверяй обычное и неверное прочтение по действиям/артефактам: строки и structural lint не доказывают качество.

## Версии

Только корневой CHANGELOG хранит версии, manifests у скиллов нет. Любая bundled правка, включая docs/modes, требует датированной записи под Keep a Changelog (`Added`, `Changed`, `Fixed`, `Removed`, `Deprecated`): один bullet на строку с именем скилла/роли/артефакта. Все старые версии/даты сохраняй от новых к старым; записи можно сокращать, не удалять.

Неизменный контракт - patch. В `0.x` смена контракта требует minor; после `1.0.0` breaking change - major. Контракт: имена, аргументы, invocation policy, роли/launch/context packets, пути/форматы/передача артефактов, write/Git boundaries.

<a id="checks"></a>

## Проверки

Из корня с Git и Bash:

```bash
bash .github/scripts/check-skills.sh
bash .github/scripts/check-no-runtime.sh
bash .github/scripts/lint-house-style.sh
git diff --check
```

Structural checker только читает рабочее дерево. Его каталог содержит ровно семь README skills, не допускает лишних. Покрывай frontmatter/invocation, роли, реальные shared copies, tracker execution block, ticket/review handoffs, self-contained links, external-path boundaries и dated CHANGELOG. Runtime guard запрещает bundled runtime; obsolete-route scan смотрит `skills/`, не root guides. Исторические CHANGELOG/ADR/архивные сценарии не текущий контракт. Link checker не проверяет anchors/весь Markdown: просмотри вручную. Untracked Markdown явно передай style script. Source pass не доказывает live behavior/permissions/registration.

[Pre-commit hook](.githooks/pre-commit) запускает обе structural checks на временном staged snapshot во всех клиентах. Включение на клон: `git config core.hooksPath .githooks`.

Только независимому review нужен выбранный native reviewer route; обсуждению/исполнению subagents не нужны. Сохрани три finder и независимый verifier; direct pass лишь для разрешенного trivial case. Возможности узнавай без hardcoded model/effort. Доступные host-enforced restrictions используй, иначе честно prompt-only. Before/after state checks обязательны в обоих случаях: видят persistent differences, не все попытки/отмененные записи. Нет nested-client fallback. Live observations отделяй от source/protocol fixtures, missing CLI оставляет клиент непроверенным. Только disposable repos/fixture approvals, не установка пользователя.

Для поведения используй [сценарии](tests/client-scenarios.md), для docs - соразмерные source/command/link checks, без повторных workflows. Review/spec cases включают checkpoint и нужные staged/unstaged/untracked без staged-only default. При явно одобренной implementation-only работе с отдельным проверяющим не запускай исключенные checks/renders/diff audit: укажи NOT RUN, оставь verification pending. Иначе просмотри diff и обе темы измененных диаграмм, captions/accessibility, сохранность истории.

<a id="local-development-and-release"></a>

## Локальная разработка и публикация

Проверяй candidate в одноразовом agents directory:

```bash
home=$(mktemp -d)
HOME="$home" npx skills@latest add "$PWD" -g -y -s '*' -a claude-code
```

Запусти клиент с этим HOME, затем удали временный каталог; credentials вне Git. После правок повтори add для обновления копий. Во временном HOME нет обычных auth/settings; при нужде войди.

Публикация: push в `main` до обновления установок; пользователь обновляет `npx skills update`. Не меняй установленные скиллы при source edits без запроса.

Каталог - семь скиллов. `rnd-grill`, подходящий диагноз и выбранные замечания прямо передаются `dev-exec`, без обязательной цепочки документов. `dev-spec` необязателен, коммиты требуют явного охвата. Source edits не обновляют установки/регистрацию; setup не предлагает companions/установку каталога. Текущие границы/доказательства - в [README](README.md) и [сценариях](tests/client-scenarios.md).
