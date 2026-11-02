# Участие в разработке

Прочитай до правок. `CLAUDE.md` и `AGENTS.md` - равнозначные точки входа.

## Структура

Каждый из [девяти skills](README.md#какой-скилл-выбрать) устанавливается отдельно:

```text
skills/<name>/
  SKILL.md              # name, description, invocation policy
  agents/openai.yaml    # необязательная invocation policy Codex
  references/           # правила по месту нужды
  assets/               # шаблоны
README.md CONTRIBUTING.md SPEC.md GLOSSARY.md
```

Ссылки skill ведут только внутрь его каталога, без зависимости от checkout или чужой установки. Не вводи aliases и обязательные стадии. При совпадении имени проверь provenance.

| Владелец | Shared reference и потребители одинаковых копий |
| --- | --- |
| `sync-spec` | `project-specs.md`: `rnd-grill`, `to-spec`, `to-tickets`, `dev-exec`, `dev-review`, `rnd-debug` |
| `nxs-setup` | `tracker.md`: `to-spec`, `to-tickets`, `dev-exec`, `rnd-debug`, `dev-review` |
| `to-tickets` | `ticket.md`: `dev-exec` |
| `dev-commit` | `commit-format.md`: `dev-exec` |

References лежат в `references/`. Меняй владельца и побайтовые копии только реальных потребителей вместе. Bundled procedure не требует установки владельца. Шаблоны принадлежат: task spec - `to-spec`, project spec - `sync-spec`, ticket - `to-tickets`; setup assets/readiness/capabilities - `nxs-setup`. Не размножай политику исполнения в setup templates.

## Язык и безопасность

Пиши кратко, по-русски, с ASCII-дефисом и прямыми кавычками. Заголовки инструкций - ПРОПИСНЫМИ, руководств/артефактов - обычным регистром. Идентификаторы, статусы и пути сохраняй; старые заголовки/records не мигрируй ради формы.

Не публикуй частные пути/remotes, tracker IDs, секреты, environment values, контакты и raw sessions. Примеры нейтральные. Личные предпочтения принадлежат client/project instructions; setup меняет их только точным одобренным diff. Сохраняй пользовательские данные и чужие изменения.

## Контракты инструкций

README - использование, CONTRIBUTING - изменение, SPEC - реализованные контракты и обоснование, GLOSSARY - определения. Операционные правила принадлежат skills/references; не пересказывай их повсюду.

- Укажи вход, проверки, действия, результат, остановки и передачу; исключения рядом с шагом.
- Description различает намерения; явный вызов отделен от обсуждения/внутренних действий.
- Шаблон различает обязательные/необязательные поля, выполненное/отмененное требование.
- Resources читаются по месту нужды; root docs не обязательный runtime context.
- Согласие действует в своих пределах: dev-exec разрешает проверенные коммиты ticket, не push/review/sync-spec. Неизвестный эффект сверяй до повтора.
- Не добавляй runtime, hooks, background skills, cross-skill injection, adapters или автоустановку.
- Project SPEC описывает реализованное, task spec - намерение. Отдельного ADR writer/автозаписи glossary нет. Source cutover не мигрирует records/установки/settings/сервисы.

<a id="checks"></a>

## Проверки

Проверяй соразмерно поведению, без новых CI workflows, hooks и source checkers:

- `npx --yes skills@latest add . -l`: ровно девять имен каталога.
- Разово проверь frontmatter, invocation policy, внутренние links и одинаковые bundled copies.
- Измененный skill запусти в доступном реальном клиенте на disposable fixture: обычный вход, остановки, сохранность чужого. Для dev-exec проверь каждый атомарный commit и итоговую приемку.
- Review: два независимых native Standards/Spec subagents, общий committed/staged/unstaged/untracked охват. Используй host-enforced read-only, иначе сообщи prompt-only. Недоступный reviewer - incomplete, без single-agent/nested-client fallback. Обсуждение/исполнение subagents не требуют.
- Tracker: реальные операции и недоступная настройка без silent fallback. Local backend не доказывает remote API.
- Просмотри diff/links. Source/packaging не доказывают live invocation, регистрацию, permissions или совместимость.

Только disposable repos и ограниченные approvals, без изменения пользовательских установок. Не добавляй постоянные tests формулировок, копий или шаблонной проводки.

<a id="local-development-and-release"></a>

## Локальная разработка и публикация

Candidate установка в одноразовый agents directory:

```bash
home=$(mktemp -d)
HOME="$home" npx skills@latest add "$PWD" -g -y -s '*' -a claude-code
```

Проверь файлы/relative links. Это packaging, не live compatibility Claude Code. Временный HOME не получает обычные credentials/settings. Для live smoke явно передай candidate SKILL.md и абсолютную resource base, не старую установку. Удали только созданный временный каталог.

Публикация и обновление установок - отдельные действия пользователя; source edits не требуют push.
