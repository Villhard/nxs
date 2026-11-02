# Участие в разработке

Прочитай до правок. `CLAUDE.md` и `AGENTS.md` - равнозначные точки входа.

## Структура

Skill - самостоятельный каталог, устанавливаемый отдельно:

```text
skills/<name>/
  SKILL.md                     # frontmatter: name, description; invocation policy
  agents/openai.yaml           # необязательная политика явного вызова Codex
  references/                  # правила по месту использования
  assets/                      # шаблоны документов
README.md CONTRIBUTING.md SPEC.md GLOSSARY.md
```

Каталог: ровно `rnd-grill`, `to-spec`, `to-tickets`, `dev-exec`, `dev-review`, `rnd-debug`, `sync-spec`, `dev-commit`, `nxs-setup`. Не вводи aliases и дополнительные обязательные стадии. Имя - отдельное пользовательское намерение, а не запуск следующей команды. При совпадении имени проверь provenance установленного skill.

Ссылки skill ведут только внутрь его каталога. Установленный skill не зависит от developer checkout или чужой установки. Bundled procedure разрешает исполнение правил без отдельно установленного skill-владельца.

| Владелец | Ресурс и реальные потребители |
| --- | --- |
| `sync-spec` | `references/project-specs.md`; одинаковые копии у `rnd-grill`, `to-spec`, `to-tickets`, `dev-exec`, `dev-review`, `rnd-debug`. Шаблон project spec только у владельца. |
| `nxs-setup` | `references/tracker.md`; одинаковые копии у `to-spec`, `to-tickets`, `dev-exec`, `rnd-debug`, `dev-review`. Setup templates/readiness/capabilities принадлежат setup. |
| `to-tickets` | `references/ticket.md`; одинаковая копия у `dev-exec`. Шаблон нового ticket только у владельца. |
| `dev-commit` | `references/commit-format.md`; одинаковая копия у `dev-exec`. |
| `to-spec` | Семисекционный шаблон спеки задачи. |
| `rnd-debug` | Диагностика и поиск каталога функции. |
| `dev-exec` | Исполнение ticket и человеческие шаги. |
| `rnd-grill` | Компактное интервью в SKILL.md, без отдельной подсистемы сохранения. |
| `dev-review` | Два reviewer prompts в SKILL.md, без roles/verifier pipeline. |

Общие ресурсы копируй побайтово только реальным потребителям. Не размножай полную политику исполнения в шаблонах setup. Сохраняй пользовательские данные и чужие изменения: source cutover не разрешает миграцию records, установок, Git settings или внешних сервисов.

## Язык и безопасность

Пиши кратко и по-русски, с ASCII-дефисом и прямыми кавычками. Заголовки инструкций - ПРОПИСНЫМИ, руководств и артефактов - обычным регистром. Идентификаторы, статусы, пути и технические термины сохраняй. Старые записи читай без автоматической миграции заголовков.

Не публикуй частные пути/remotes, tracker IDs, секреты, environment values, личные контакты и raw sessions. Примеры нейтральные. Личные предпочтения принадлежат client/project instructions; setup пишет их только точным одобренным diff.

## Контракты инструкций

README объясняет использование, CONTRIBUTING - изменение, SPEC - реализованные контракты и существенное обоснование. Полные операционные правила принадлежат skills/references; не пересказывай их во всех документах.

- Укажи вход, проверки входа, действия, результат, остановки и передачу. Исключения держи рядом с шагом.
- Description различает намерения соседних команд. Явный вызов отделен от обсуждения и внутренних действий.
- Шаблон различает обязательные/необязательные поля, выполненное и отмененное требование.
- Ресурсы читаются по месту нужды; root docs не обязательный runtime context.
- Используй согласие в его пределах. Вызов dev-exec разрешает проверенные атомарные коммиты ticket, но не push/review/sync-spec. Неизвестный эффект сверяй до повтора.
- Не добавляй runtime, hooks, background skills, cross-skill injection, программные adapters или автоматическую установку.
- Project SPEC описывает только реализованное. Спека задачи хранит намерение; отдельного ADR writer и автоматической записи glossary нет.

<a id="checks"></a>

## Проверки

Проверяй соразмерно измененному поведению. Новых CI workflows, hooks и специальных source checkers нет.

- Discovery: `npx --yes skills@latest add . -l`, ровно девять имен выше.
- Разово проверь frontmatter, явную invocation policy, внутренние relative links и одинаковые bundled copies. Проверка формы не доказывает поведение модели.
- Для инструкций запусти измененный skill в реальном доступном клиенте на disposable fixture; наблюдай результат, а не только чтение prompt. Включи обычный вход, остановки и сохранность чужих данных. Для dev-exec проверь каждый атомарный commit и итоговую приемку.
- Для review нужны два независимых native subagents Standards/Spec и единый охват committed/staged/unstaged/untracked. Host-enforced read-only используй, где доступен; иначе сообщай prompt-only. Недоступный reviewer дает incomplete, не single-agent или nested-client fallback. Обсуждение и исполнение subagents не требуют.
- Для tracker проверь реально используемые операции и недоступную настройку без silent fallback. Local backend не доказывает remote API.
- Просмотри итоговый diff и ссылки. Отделяй source/packaging от live observations; неизвестную регистрацию/permissions/совместимость не объявляй проверенной.

Используй только disposable repos и ограниченные approvals. Не меняй пользовательские установки ради smoke. Не добавляй постоянные tests на формулировки prompt, побайтовые копии или шаблонную проводку.

<a id="local-development-and-release"></a>

## Локальная разработка и публикация

Candidate установка в одноразовый agents directory:

```bash
home=$(mktemp -d)
HOME="$home" npx skills@latest add "$PWD" -g -y -s '*' -a claude-code
```

Проверь файлы и bundled relative links. Это packaging check, не доказательство совместимости Claude Code. Клиент с временным HOME не получает обычные credentials/settings. Для реального smoke передай candidate SKILL.md и абсолютную resource base явно; не подменяй его старой установленной версией. После проверки удали только созданный временный каталог.

Публикация и обновление установок - отдельные действия пользователя. Source edits не требуют push и не обновляют установленные skills. Основной маршрут: rnd-grill → to-spec → to-tickets → dev-exec одного ticket; review и sync-spec отдельно. Небольшой согласованный вход можно передать to-tickets без промежуточного файла.
