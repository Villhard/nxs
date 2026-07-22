# CONTRIBUTING (nxs)

Гайд по авторингу скилла или агента для плагина `nxs`. Прозаические пояснения - русский; шаблоны, frontmatter, таблицы, имена команд, пути и идентификаторы - English (runtime language, verbatim).

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
    <background-name>/   # tier 3, user-invocable: false
  agents/
    <agent-name>.md      # автономный subagent
  README.md CONTRIBUTING.md
```

Tier 1 (global `~/.claude/CLAUDE.md`) и `settings.json` - НЕ в репо плагина: их пишет пользователь руками.

## THREE TIERS

- Tier 1 - global `~/.claude/CLAUDE.md`: always-on, работает в каждом ответе. Вне репо плагина.
- Tier 2 - command skills `/nxs:<name>`: workflow, видны в `/` меню. Сейчас их шесть: `rnd`, `bug`, `plan`, `plancheck`, `exec`, `review`.
- Tier 3 - background skills (`user-invocable: false`): общие правила, грузятся по релевантности. Сейчас их пять: `plan-conventions`, `review-protocol`, `verify`, `commit-conventions`, `intake`.

## NAMING

- Формат команды: `/nxs:<name>` - плоское имя, без флоу-префикса.
- Имя команды = имя ДИРЕКТОРИИ скилла. `skills/plan/` -> `/nxs:plan`.
- Namespace `nxs` берётся из `plugin.json` поля `name`. Инвокация всегда namespaced, bare-алиаса нет.
- Background skills имеют ролевое имя (`commit-conventions`, `plan-conventions`), потому что command skills ссылаются на них по имени. Имя фиксируется при добавлении и не меняется без обновления всех потребителей.

## PLACEMENT RULE

Куда положить правило, политику или терм:

- always-on (язык, стиль, безопасность) -> tier 1, вне плагина;
- потребляется ОДНОЙ командой -> inline в её `SKILL.md` (или её `reference/`);
- потребляется НЕСКОЛЬКИМИ командами -> tier 3 background skill;
- контент делят несколько агентов -> живёт в single-source файле; оркестратор читает его один раз и инжектит полный текст в prompt каждого агента;
- правило нужно ровно одному агенту -> inline в файл этого агента.

Правило критичности: security-критичное содержимое (never commit secrets, no force-push, confirm destructive) НЕ вешать на tier 3 - авто-load эвристичен, не гарантирован. Такое идёт в tier 1. На tier 3 остаётся только workflow-деталь.

## КОГДА ЗАВОДИТЬ НОВЫЙ АРТЕФАКТ

Репо намеренно держится маленьким: шесть команд, пять фоновых скиллов, шесть агентов. Новый tier-2 command skill заводится только когда выполнены ВСЕ условия сразу:

- intent отдельный (не сводится к существующей команде даже через слово-режим);
- intent частый (реально вызывается несколько раз в месяц, не раз в квартал);
- заслуживает отдельный autocomplete-слот в `/` меню;
- идея стабильна, не экспериментальна.

Не выполнено хотя бы одно - это не команда, а upgrade существующего скилла, background skill или inline-правило.

Что не делать: не копировать внешний скилл целиком; не заводить отдельную команду под каждый импортированный рецепт; не добавлять абстрактный "general guidance" без конкретного failure mode; не делать side-правки "пока я здесь".

## AUTHORING PLAYBOOK

- Имя команды = имя ДИРЕКТОРИИ скилла.
- НЕ ставить frontmatter `name` во вложенных скиллах: `name` - это display-label, он прячет namespace-префикс в `/` меню. Без `name` меню показывает `nxs:<dir>`.
- Тело `SKILL.md` - компактный English. Язык вывода пользователю задаёт tier 1, не скилл.
- Тело входит в контекст при вызове и остаётся на сессию: писать standing-инструкции, не одноразовые шаги.
- `reference/*.md` - тяжёлая деталь, грузится по требованию, когда `SKILL.md` на неё ссылается.
- Валидация каждого шага: `claude plugin validate --strict .`

### COMMAND SKILL FRONTMATTER

```yaml
---
description: <one line, drives model-invocation; when-to-use trigger + short what-it-produces, not the process>
argument-hint: "[...]"
---
```

Правило SDO (`description` = when-to-use, не пересказ процесса): `description` называет ТОЛЬКО триггер плюс короткий clause что скилл производит - не перечисляет фазы и механику тела. Пересказывающий workflow `description` заставляет модель действовать по этому пересказу и пропускать тело скилла, где живёт процедура. Тело каждого command skill несёт одну строку `Example:` с реальной инвокацией сразу после intro.

### BACKGROUND SKILL FRONTMATTER

```yaml
---
description: <what these rules are> - load before/when <trigger>. Background knowledge, not a user command.
user-invocable: false
---
```

## ARTIFACT PATHS

Каждый producing skill инлайнит СВОЮ строку пути в секции `## ARTIFACT` - это единственный источник. Общей таблицы здесь намеренно нет: она была дублем и расходилась со скиллами. Обзор для человека - в README.

Все рабочие артефакты лежат под `docs/nxs/` текущего репозитория. Молча создавать файлы вне этих шаблонов запрещено.

### PUBLIC SAFETY

Durable-артефакты могут попасть в public-репозиторий. Перед коммитом убрать личный контекст: локальные пути `/Users/<name>`, приватные git-remote, реальные tracker-ключи и URL, secrets / tokens / `.env`, имена и почты коллег, сырой session/tool output. Использовать нейтральные плейсхолдеры (`<user_home>`, `<github_owner>/<repo>`, `PROJ-123`).

## DEV LOOP

Install кэширует СНИМОК плагина, не читает репо вживую:

```
# один раз - подключить локальный dev marketplace
claude plugin marketplace add ~/nxs
claude plugin install nxs@nxs

# после каждой правки
claude plugin marketplace update nxs   # затем reinstall плагина
```

Инвокация обновлённого скилла в текущей сессии - только после рестарта сессии.

## VERSIONING

Любая правка bundled-контента (skills / agents / manifests) - bump поля `version` в `plugin.json` плюс запись в `CHANGELOG.md` (Keep a Changelog, секция новой версии сверху). Какой разряд двигать, решает не размер диффа, а то, тронут ли КОНТРАКТ.

### ЧТО ТАКОЕ КОНТРАКТ

То, на что опирается пользователь или другой файл плагина:

1. имена команд `/nxs:<name>`, их аргументы и режимы;
2. имена background skills и агентов - другие скиллы ссылаются на них по имени;
3. пути и схемы имён артефактов (`docs/nxs/plans/YYYYMMDD-<slug>.md`);
4. секции артефактов, которые читает другой скилл: `## SOURCE ARTIFACTS`, `## ACCEPTANCE CRITERIA`, `## DEVELOPMENT APPROACH`, `## CONVENTIONS`, чекбоксы `- [ ]`;
5. гейты, решающие судьбу git и файлов: когда разрешён коммит, что является stop condition, что скилл пишет на диск.

Всё, что не в этом списке, - внутреннее устройство: формулировки внутри `SKILL.md`, критерии и focus areas линз, состав `reference/`-файлов, README и CONTRIBUTING.

### РАЗРЯДЫ

- **PATCH** - контракт не тронут: переписана формулировка, уточнён критерий линзы, переставлены `reference/`-файлы без смены поведения, поправлена документация.
- **MINOR** - контракт изменился: команда добавлена / удалена / переименована, сменились её аргументы, переименован скилл или агент, сменилась схема путей, изменилась обязательная секция артефакта или гейт.
- **MAJOR** - `0.x` это initial development по semver: публичный контракт не стабилизирован и может меняться в любом minor. `1.0.0` выпускается вместе с объявлением контракта стабильным - с этого момента ломающее изменение требует major-бампа. До этого major не двигается, каким бы крупным ни был diff.

Тест, если сомневаешься: наберёт пользователь завтра то же, что вчера, - получит то же самое и в том же месте? Да, но качество разбора другое -> patch. Нет -> minor.
