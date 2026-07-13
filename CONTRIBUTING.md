# CONTRIBUTING (nxs)

Гайд по авторингу нового скилла или агента для плагина `nxs`. Прозаические пояснения - русский; шаблоны, frontmatter, таблицы, имена команд, пути и идентификаторы - English (runtime language, verbatim).

Маршрут контрибьютора: назвать артефакт (NAMING) -> решить, куда он ложится (ADDING A SKILL OR AGENT) -> написать его (AUTHORING PLAYBOOK) -> знать, куда пишут его выходы (ARTIFACT PATHS).

## REPO LAYOUT

```
nxs/
  .claude-plugin/
    plugin.json          # name: nxs (namespace всех команд)
    marketplace.json     # local dev marketplace (source "./")
  skills/
    <name>/              # tier 2, command skill -> /nxs:<name>
      SKILL.md
      reference/         # опционально, on-demand деталь
      scripts/           # опционально, детерминированная логика
    <background-name>/   # tier 3, user-invocable: false
      SKILL.md
      reference/
  agents/
    <agent-name>.md      # автономный subagent (всё нужное внутри файла)
  README.md CONTRIBUTING.md
```

Tier 1 (global `~/.claude/CLAUDE.md`) и `settings.json` - НЕ в репо плагина: их пишет пользователь руками, плагин их не шипит.

## THREE TIERS

- Tier 1 - global `~/.claude/CLAUDE.md`: tool-level always-on, работает в каждом ответе без команды. Вне репо плагина.
- Tier 2 - command skills `/nxs:<flow>-<action>`: workflow, видны в `/` меню.
- Tier 3 - background skills (`user-invocable: false`): общие правила, грузятся по релевантности, в `/` меню не видны.

## NAMING

- Формат команды: `/nxs:<name>` - плоское имя, без флоу-префикса.
- Имя команды = имя ДИРЕКТОРИИ скилла. `skills/plan/` -> `/nxs:plan`.
- Namespace `nxs` берётся из `plugin.json` поля `name: nxs`. Инвокация плагин-скилла всегда namespaced (`/nxs:...`), bare-алиаса нет. Уникальность даёт `nxs:`, флоу-префикс не нужен.

Текущий набор команд (14, плоские имена):

| area | commands |
|---|---|
| build | `plan`, `exec`, `review`, `plancheck`, `bug` |
| think | `rnd`, `dialectic`, `epic`, `wrong` |
| understand | `explain` |
| document | `userdoc`, `techdoc` |
| git / project | `recommit`, `clean` |

Modes (редкие, по инференсу): `exec` (default / auto), `explain` (глубина). Остальные - один режим. `area` - только группировка для чтения, не префикс команды.

Background skills не следуют схеме `<flow>-<action>`: у них ролевое имя (`commit-conventions`, `plan-conventions`, `review-protocol`), потому что command skills ссылаются на них по имени. Имя фиксируется при добавлении и не меняется без обновления всех потребителей.

## ADDING A SKILL OR AGENT

Новый артефакт не заводится по привычке "давай ещё один скилл". Сначала - куда идея ложится, потом ярус, потом файл.

### DESTINATION FILTER

Каждая новая идея получает ровно один пункт назначения:

| destination | when to choose |
|---|---|
| new command skill (tier 2) | отдельный частый пользовательский intent, заслуживает слот в `/` меню; идея стабильна, не экспериментальна |
| upgrade of an existing skill | внешний рецепт - лучшая процедура для уже покрытого intent (шаг внутри существующего скилла, более точный фильтр) |
| new background skill (tier 3) | переиспользуемое правило / словарь / критерий оценки, который делят НЕСКОЛЬКО скиллов |
| inline rule | правило нужно ровно одному скиллу (в его `SKILL.md` или `reference/`) или одному агенту (в его файл) |
| new agent | новая read-only роль, которой нет у текущих reviewer-ов / explorer-а |
| reject | domain-specific рецепт, устаревшее, дубль с косметической разницей, "на всякий случай" без конкретного failure mode |

### PLACEMENT RULE

Куда положить правило / политику / терм:

- always-on (язык, стиль, безопасность, token economy) -> tier 1 (`~/.claude/CLAUDE.md`), вне плагина.
- потребляется ОДНОЙ командой -> inline в её `SKILL.md` (или её `reference/`).
- потребляется НЕСКОЛЬКИМИ командами -> tier 3 background skill.
- контент делят несколько агентов -> живёт в single-source файле (background skill или `reference/`-файл оркестрирующего скилла). Оркестратор читает этот файл один раз и инжектит его полный текст в prompt каждого агента.
- в файле самого агента остаётся только guard-строка ("Follow the protocol provided in your input; if missing, stop and report `protocol missing` - do not review from memory") и его domain-specific содержимое.
- правило нужно ровно одному агенту -> inline прямо в файл этого агента (single-source файл не нужен для того, что использует только один потребитель).

Правило критичности: security-критичное содержимое (never commit secrets, no force-push to main, confirm destructive) НЕ вешать на tier 3 - авто-load эвристичен, не гарантирован. Такое идёт в tier 1 (always-on, детерминированно). На tier 3 остаётся только workflow-деталь: формат сообщения, атомарность, mode-gating.

### WHEN A NEW COMMAND SKILL

Новый tier-2 command skill заводится только когда выполнены ВСЕ условия сразу:

- intent отдельный (не сводится к существующей команде даже через mode-слово);
- intent частый (пользователь реально вызовет его несколько раз в месяц, не раз в квартал);
- заслуживает отдельный autocomplete-слот в `/` меню;
- идея стабильна, не экспериментальна.

Не выполнено хотя бы одно - это не команда, а upgrade существующего скилла, background skill или inline-правило.

### REGISTRATION

- Command skill: создать `skills/<flow>-<action>/SKILL.md`. Имя команды = имя директории. Регистрации в манифесте не требуется - плагин обнаруживает скиллы по директориям.
- Background skill: создать `skills/<name>/SKILL.md` с `user-invocable: false`. Имя фиксируется здесь; command skills ссылаются на него по имени в теле своего `SKILL.md`.
- Agent: создать `agents/<name>.md`, автономный. Общий протокол инжектится оркестратором в prompt агента (см. PLACEMENT RULE).

### MAPPING IS MANDATORY

Когда идея приходит из внешнего скилла / рецепта другого харнесса, до написания файла зафиксировать блок:

```
- failure mode: <что в текущем workflow ломается без этой идеи>
- affected skills/agents: <какие скиллы/агенты затронуты>
- target: command | skill upgrade | background skill | inline | agent | reject
- why a lighter integration is not enough: <почему именно этот target, а не более лёгкий>
```

Без явного mapping идею не принимают.

### WHAT NOT TO DO

- не копировать внешний скилл целиком, даже "так удобнее";
- не делать side-правки "пока я здесь";
- не заводить отдельную команду под каждый импортированный скилл - это ровно тот bloat, против которого фильтр;
- не добавлять абстрактный "general guidance" без конкретного failure mode.

## AUTHORING PLAYBOOK

Подтверждено прототипом (claude 2.1.201).

- Имя команды = имя ДИРЕКТОРИИ скилла. `skills/plan/` -> `/nxs:plan`.
- НЕ ставить frontmatter `name` во вложенных скиллах: `name` - это display-label, он прячет namespace-префикс в `/` меню (показывает bare-имя). Без `name` меню показывает `nxs:<dir>`.
- Тело `SKILL.md` - компактный English (runtime language). Язык вывода пользователю задаёт tier 1, не скилл.
- Тело входит в контекст при вызове и остаётся на сессию: писать standing-инструкции (постоянные правила), не одноразовые шаги.
- `reference/*.md` - тяжёлая деталь, грузится по требованию, когда `SKILL.md` на неё ссылается.
- `scripts/*` - детерминированная логика вместо промпта; вызов `${CLAUDE_SKILL_DIR}/scripts/...`.
- Background skill: `user-invocable: false` + `description` с явным триггером ("load before ...", "use when ...").
- Валидация каждого шага: `claude plugin validate --strict`.

### COMMAND SKILL FRONTMATTER

```yaml
---
description: <one line, drives model-invocation; when-to-use trigger + short what-it-produces, not the process>
argument-hint: "[...]"
---
```

Правило SDO (`description` = when-to-use, не пересказ процесса): `description` называет ТОЛЬКО триггер (когда тянуться за скиллом) плюс короткий clause что скилл производит - не перечисляет фазы, шаги и механику тела. Пересказывающий workflow `description` заставляет модель действовать по этому пересказу и пропускать тело скилла, где и живёт процедура. Тело каждого command skill несёт одну строку `Example:` с реальной инвокацией сразу после intro - это помогает авто-вызову, не раздувая `description`.

### BACKGROUND SKILL FRONTMATTER

```yaml
---
description: <what these rules are> - load before/when <trigger>. Background knowledge, not a user command.
user-invocable: false
---
```

### DEV LOOP

Install кэширует СНИМОК плагина, не читает репо вживую. Цикл правки:

```
# один раз - подключить локальный dev marketplace
claude plugin marketplace add ~/nxs
claude plugin install nxs@nxs

# после каждой правки в репо
claude plugin marketplace update nxs
# затем reinstall плагина
```

Инвокация обновлённого скилла в текущей сессии - только после рестарта сессии.

### VERSIONING

- Любая правка bundled-контента (skills / agents / manifests) - bump поля `version` в `plugin.json` по semver.
- К каждому bump - запись в `CHANGELOG.md` (Keep a Changelog, секция новой версии сверху).

## ARTIFACT PATHS

Куда пишут выходы каждой команды. Human reference: каждый producing skill инлайнит СВОЮ строку пути; эта таблица - общий обзор. Пути относительны текущего рабочего репозитория, если не сказано иное.

| command | artifact |
|---|---|
| `/nxs:rnd` | `docs/briefs/YYYYMMDD-<slug>.md` (с ключом трекера: `YYYYMMDD-<KEY>-<slug>.md`) |
| `/nxs:bug` | `docs/briefs/YYYYMMDD-<slug>-root-cause.md` (с ключом трекера: `YYYYMMDD-<KEY>-<slug>-root-cause.md`) |
| ADR (via decision-log) | `docs/adr/NNNN-<slug>.md` (project ADR convention, если она есть) |
| `/nxs:plan` | `docs/plans/YYYYMMDD-<slug>.md` (с ключом трекера: `YYYYMMDD-<KEY>-<slug>.md`) |
| `/nxs:plancheck` | chat findings; опционально секция `## PLAN REVIEW NOTES` в плане |
| `/nxs:exec` | изменения кода + обновлённые чекбоксы плана |
| `/nxs:review` | chat report |
| `/nxs:clean` | перемещённые файлы (`docs/plans/completed/`, `docs/briefs/archive/`) |
| `/nxs:techdoc` | `docs/techdoc/<slug>.md` (локальный черновик, `docs/` gitignored; durable - Confluence) |
| `/nxs:userdoc` | `docs/userdoc/<slug>.md` (локальный черновик, `docs/` gitignored; durable - Confluence) |

Правила путей:

- `docs/briefs/`, `docs/plans/`, `docs/plans/completed/`, `docs/briefs/archive/` - в текущем рабочем репозитории, source-of-truth для workflow. Это локальные рабочие артефакты: `docs/` не трекается (gitignored), в код не коммитятся и в снимок плагина не входят.
- Doc-артефакты (`techdoc`, `userdoc`) пишутся в `docs/<kind>/` рабочего репо; `docs/` gitignored, это локальный черновик, durable-дом - Confluence. В код доки не коммитятся.
- Молча создавать файлы вне этих шаблонов запрещено.

### PUBLIC SAFETY

Durable-артефакты (`docs/plans/`, `docs/briefs/`, ADR, коммитнутые заметки) могут попасть в public-репозиторий. Перед коммитом убрать личный контекст: локальные пути `/Users/<name>`, приватные git-remote, реальные tracker-ключи и URL, secrets / tokens / `.env`, имена и почты коллег, сырой session/tool output. Использовать нейтральные плейсхолдеры (`<user_home>`, `<local_user>`, `<github_owner>/<repo>`, `PROJ-123`).
