# История изменений

Значимые изменения nxs. До `0.17.0` продукт назывался `nxs`, до `0.43.0` включительно поставлялся как plugin `dev`.

Формат - [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), версии - [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Прежние незавершенные работы и история дизайна. Датированный контракт семи скиллов ниже заменяет устаревшие маршруты; журнал не доказывает публикацию/cutover.

### Добавлено

- Записи дизайна lead (2026-10-30): координатор, plan/decision-log, autonomy/reapproval, модели, одобренные environment steps, companions, узкое R&D, parallel worktrees, общий журнал и Codex-first проверка.
- Дизайн надежности lead (2026-10-30): сначала последовательный цикл/восстановление, ограниченные структурированные outcomes/helpers; названы пределы журнала ручных companions.
- Решение интеграции companions (2026-10-30) отличает ручной диалог от проверенного lead execution и оставляет выборочный перенос в nxs будущему исследованию.
- `CONTRIBUTING.md` задает правило `dev-` и короткого узнаваемого слова без конфликтов companions/client commands; [ADR 0007](docs/adr/0007-skill-names.md) объясняет сохраненные имена.

### Изменено

- `dev-commit` (2026-11-01) убирает обязательный journal context и сверяет сомнительные коммиты перед продолжением.
- `rnd-debug` (2026-11-01) передает подходящие подтвержденные причины прямо `dev-exec`.
- Execution context `dev-exec` (2026-11-01) допускает прямо одобренные environment actions и необязательные каталоги задачи.
- `dev-spec` (2026-11-01) убирает обязательную координацию, требует покрытия работы до записи.
- `dev-review` (2026-11-01) предлагает `dev-exec` для подходящих новых/покрытых tickets вместо `/plan`, не запускает исполнение.
- `to-tickets`, `dev-review`, `dev-exec`, `nxs-setup` (2026-11-01) используют `dev-exec` в новых шаблонах, сохраняя прежнее исполнение/запреты.
- `dev-review` (2026-11-01) допускает prompt-only при отсутствии host enforcement, с обязательной сверкой repo и честными пределами; сценарии покрывают непроверенный маршрут.
- `dev-exec` (2026-11-01) выполняет разрешенные проверенные checkpoint через `dev-commit` в своей сессии; без выбранных коммитов/при запрете продолжает без них.
- `nxs-lead` и controlled-run references (2026-11-01) делегируют checkpoint исполнителю, сохраняют независимую приемку/review после ticket.
- Ticket templates `to-tickets`, `dev-review`, `dev-exec`, `nxs-setup` (2026-11-01) различают approved checkpoints, старые no-commit tickets и `/plan`.
- `nxs-lead` (2026-11-01) выбирал исследование при существенной неопределенности и коммитил принятые блоки до переноса checkpoint в `dev-exec`.
- README/схемы (2026-11-01) показывают входы, условные передачи, записи и setup с текущими разрешениями.
- Каталог README/схемы (2026-11-01) группируют скиллы по назначению/условным переходам.
- README, CONTRIBUTING, GLOSSARY, project spec, сценарии/схемы описывают дополнительный каталог, сохраненные legacy routes и непроверенный cutover.
- README "Run a ticket" объясняет остановку при недостающем результате блокера.

### Исправлено

- `dev-review` (2026-11-01) проверяет checkpoint handoff до empty-scope stop/staging suggestion, сохраняя чужое и охват.
- `dev-exec`, `nxs-lead`, `dev-review`, `dev-spec` (2026-11-01) передают checkpoint scope и останавливаются при пропуске/неясном покрытии задачи в default diff.
- `to-tickets` (2026-11-01) согласует копирование checkpoint template; сценарии/checker защищают от старой формулировки.
- `dev-exec`, `nxs-lead` (2026-11-01) по умолчанию предлагают/проверяют явные checkpoint scopes, сохраняя approval/no-commit.
- `dev-exec` (2026-11-01) допускает свежий bounded run после сверки/одобрения при недокументированном continuation, сохраняя план/границы.
- `dev-commit` (2026-11-01) возвращает same-session checkpoint в `dev-exec`, сохраняя самостоятельную остановку.
- Shell checker валидирует frontmatter scalars/даты и запрещает пустые releases.
- README различает одноименные nxs/companion skills до выбора маршрута.
- `## Done when` ticket/трекера `dev-setup` записывает missing blocker одной строкой `## Comments` и останавливается без вопроса, чтобы Claude Code Plan Mode записал ее после одобрения плана.

## [0.78.0] - 2026-11-01

### Изменено

- Семь скиллов, reviewer roles, references и шаблоны переведены на русский и сокращены без удаления условий работы; пользовательские артефакты и установки не меняются.
- Заголовки новых артефактов стали русскими; читатели принимают прежние английские заголовки. Служебные поля и статусы сохранены; изменение формата требует minor release.
- `CONTRIBUTING.md` задает русский язык инструкций; `check-skills.sh` проверяет русские формы с прежними гарантиями безопасности и структуры.
- README, GLOSSARY, AGENTS/CLAUDE, PR template и обе темы шести SVG-схем переведены; README сокращен до выбора команд, примеров и основных границ со ссылками на полные правила.
- ADR, архив клиентских сценариев и CHANGELOG переведены с сохранением решений, версий, дат, наблюдений и ограничений доказательств.

## [0.77.0] - 2026-11-01

### Добавлено

- ADR 0009 (2026-11-01) фиксирует семь прямых скиллов вместо прежней координации/журнала, сохраняя исторические ADR.
- Архив сценариев (2026-11-01) сохраняет прежний протокол/наблюдения отдельно от текущих ожиданий.

### Изменено

- `rnd-grill` (2026-11-01) объединяет соразмерное исследование, зависимые вопросы, обзоры, дизайн границы, изолированные опыты и прямое одобренное сохранение без обязательных стадий.
- `rnd-debug` (2026-11-01) передает подтвержденное прямо `dev-exec`, сохраняя intent agreement, uncertain stops, диагноз/ticket.
- `dev-exec` (2026-11-01) владеет делением, tickets/handoff, прямыми environment approvals и selected fixes с plan/check/commit boundaries.
- `dev-review`/roles (2026-11-01) закрепляют полный итог с committed/staged/unstaged/untracked, независимых finders/verifier и прямую передачу исправлений.
- `dev-spec` (2026-11-01) записывает существенное лишь после покрытия работы, сохраняя private/visible и защиту постороннего.
- `dev-commit` (2026-11-01) сохраняет scope approval, atomic staging/foreign-index safety без обязательной координации/повтора неизвестного.
- `nxs-setup` (2026-11-01) использует семь владельцев и нужный report-only readiness без lead/journal.
- README, `CONTRIBUTING.md`, SPEC, GLOSSARY (2026-11-01) описывают семь скиллов, прямую передачу, владельцев, необязательные записи и source/install границы.
- Шесть пар SVG (2026-11-01) показывают сокращенный процесс, обсуждение, диагноз, записи, setup и ticket states в Mono; подписи/accessibility согласованы, render verification pending.
- Сценарии (2026-11-01) покрывают прямой вход, необязательные записи/tickets, полный review/spec, fixes, checkpoint safety/setup; behavioral verification NOT RUN.

### Исправлено

- `review-simplification` (2026-11-01) явно запрещает любые файлы/отчет/Git принятой общей формулировкой без изменения checker.
- CONTRIBUTING (2026-11-01) ограничивает obsolete-route scan исходниками `skills/`, не root guides.

### Удалено

- Команды `rnd-map`, `rnd-research`, `rnd-prototype`, `rnd-audit`, `rnd-design`, `to-decision`, `to-spec`, `to-questionnaire` (2026-11-01) объединены в `rnd-grill` без aliases/скрытого процесса.
- `to-tickets`, `to-handoff` (2026-11-01) объединены в `dev-exec`.
- `nxs-lead`, `nxs-retro`, lead/auto, обязательные journals/controlled envelopes, review ticket-export (2026-11-01) удалены из active contracts; пользовательские записи/история сохранены.
- Осиротевшие bundle/map SVG пары (2026-11-01) удалены после замены единственного embed; посторонние изображения/история сохранены.

## [0.76.0] - 2026-11-01

### Изменено

- `nxs-retro` дает каждой доказанной проблеме конкретное решение в отчете/ответе.
- `nxs-lead` ждет обязательные результаты, перечисляет оставшиеся worktrees и защищает cleanup; README/сценарии описывают scoped update/пределы.

## [0.75.0] - 2026-11-01

### Удалено

- `dev-rnd`, `dev-bug`, `dev-lead`, `dev-setup` из source catalog без смены установок/доказательства cutover.

### Изменено

- Shared project-spec/controlled-run/ticket references используют сохраненных владельцев, старые recovery paths сохранены.
- `rnd-debug`, `dev-review`, `dev-spec`, `dev-exec`, `to-spec` не называют удаленные команды действующими.
- Checker, CI, README, CONTRIBUTING, GLOSSARY, сценарии отражают удаление/непроверенное.

## [0.74.2] - 2026-11-01

### Изменено

- `dev-review` проверяет схемы/accessibility при смене команд, отличает current/legacy.
- Сценарии закрепляют финальные fixtures/resources и требуют повторной проверки измененного.

## [0.74.1] - 2026-11-01

### Исправлено

- Ticket-state схемы показывают выбранного исполнителя после человека; workflow/README выделяют `dev-exec`, убирают legacy section.

## [0.74.0] - 2026-11-01

### Изменено

- `to-tickets` передает готовое `dev-exec`; ticket/setup/triage поддерживают его и старый `/plan`, включая human return.
- README, CONTRIBUTING, сценарии описывают передачу и реальные пределы проверки.

## [0.73.1] - 2026-11-01

### Изменено

- Project/`to-tickets` specs согласуют дополнительный процесс и непроверенное.

### Исправлено

- Shell checks отклоняют неверный/дублированный frontmatter, invocation policy, reference-style links.
- Pre-commit проверяет staged snapshot против обхода partial staging.
- README помещает collisions/ограничения до install/update.

## [0.73.0] - 2026-11-01

### Изменено

- Каталог/upgrade `nxs-setup` различают 19 команд, retained routes и непроверенную регистрацию.

## [0.72.0] - 2026-11-01

### Добавлено

- `nxs-setup`: независимый global config и source map 15 возможностей.

## [0.71.0] - 2026-11-01

### Добавлено

- `nxs-setup`: scoped goal/project setup с одобрением и report-only readiness; `nxs-retro` использует общие writing rules.

## [0.70.0] - 2026-11-01

### Изменено

- Shared controlled-run принимает явное разрешение `nxs-lead` наряду со старым lead.
- `dev-review`/contributor guide называют native subagents сохраненных маршрутов.

## [0.69.0] - 2026-11-01

### Добавлено

- `nxs-lead`: явный guarded auto и локальная HTML-защита.

## [0.68.0] - 2026-11-01

### Добавлено

- `nxs-lead`: продолжение по доказательствам без recovery engine.

## [0.67.0] - 2026-11-01

### Добавлено

- `nxs-lead`: явный ordinary native-subagent coordinator candidate.

## [0.66.0] - 2026-11-01

### Добавлено

- `nxs-retro`: разбор одной сессии и доказанные улучшения в пределах разрешения.

## [0.65.0] - 2026-11-01

### Добавлено

- `to-handoff`: контекст продолжения с журналом или без.

## [0.64.0] - 2026-11-01

### Добавлено

- `to-questionnaire`: вопросы адресату без незапрошенной отправки/выдуманных ответов.

## [0.63.0] - 2026-11-01

### Добавлено

- `rnd-map`: локальные decision maps с разрешением на каждый вопрос/сохранением зависимостей.

## [0.62.0] - 2026-11-01

### Добавлено

- `rnd-audit`: приоритетный architecture survey или ограниченный доказательствами no-change без реализации.

## [0.61.0] - 2026-11-01

### Добавлено

- `rnd-design`: сравнение/сохранение согласованного дизайна выбранного модуля без реализации.

## [0.60.0] - 2026-11-01

### Добавлено

- `rnd-prototype`: гипотеза, сохраненный опыт/вывод без разрешения product changes.

## [0.59.0] - 2026-11-01

### Добавлено

- `rnd-research`: результаты с источниками/пределами как дополнительный candidate без решения/следующей стадии.

## [0.58.0] - 2026-11-01

### Добавлено

- `dev-review`: дополнительная передача выбора в `to-tickets`, который создает tickets по актуальным findings; старый review-to-fix сохранен.

## [0.57.0] - 2026-11-01

### Добавлено

- `rnd-debug`: доказанный диагноз без fix tickets; `to-tickets` принимает подходящие причины как дополнительный candidate.

## [0.56.0] - 2026-11-01

### Исправлено

- `dev-exec` записывает/выполняет полные обязательные проверки, оставляет unresolved при missing/failing test/linter; `tests/client-scenarios.md` покрывает завершение.

## [0.55.0] - 2026-11-01

### Добавлено

- `dev-lead` делегирует bounded steps native subagents через `references/subagents.md`, хранит вопросы/прогресс обычными файлами через `references/questions.md`; missing capability останавливает шаг.
- `dev-review` запускает finders/verifier только native subagents, отличает host permissions от prompt.
- `.github/scripts/check-skills.sh` и `.github/scripts/check-no-runtime.sh` заменяют Python checker в CI/pre-commit.
- [ADR 0008](docs/adr/0008-native-subagent-coordination.md): native coordination и удаление custom runtime.
- `tests/client-scenarios.md` покрывает delegation, local questions, capability stops и source checks.

### Изменено

- `dev-lead`, `dev-review`, readiness `dev-setup`, `README.md`, `SPEC.md`, `CONTRIBUTING.md` не требуют Python 3, terminal session/controller/HUD, nested CLI и старое terminal app.
- Journals/controlled packets - append-only текст; ticket `## Done when`/setup copy фиксируют journal/native continuation.
- Setup/workflow схемы и alt описывают native subagents/current readiness.

### Удалено

- Весь Python репозитория: lead runner/approval/status/inventory/harness/outcome/mechanics/commit helpers, review adapters, все journal.py, checker/regressions, `tests/test_dev_lead.py`, `tests/test_harnesses.py`.
- Bundled scripts/__pycache__, bounded CLI review и terminal identity/HUD/questionnaire waiter/owned cleanup contracts.

## [0.54.0] - 2026-10-31

### Добавлено

- `dev-exec`: standalone ticket/clear-request executor с plan approval, prerequisites/human gates и отдельными review/spec/commit.

### Изменено

- Checker/fixtures включают dev-exec policies/self-contained resources, сохраняя templates/`/plan`.
- README, CONTRIBUTING, сценарии описывают дополнительного исполнителя, копии и соразмерные пределы.

## [0.53.0] - 2026-10-31

### Добавлено

- `to-tickets`: независимое деление feature spec, сохранение истории, зависимости/одобренные правки со старым `/plan`.

### Изменено

- `to-tickets` владеет идентичными ticket rules/template для dev-rnd/dev-bug/dev-review, старые маршруты/исполнение сохранены.
- Checker/shared expectations/tracker block/regressions включают candidate.
- README, CONTRIBUTING, сценарии описывают tickets, источник копий/пределы наблюдений.

## [0.52.0] - 2026-10-31

### Добавлено

- `to-spec`: отдельная подготовка feature spec по решению/запросу, разрешенные drafts/source/dependencies/safety, без tickets.

### Изменено

- Checker/fixtures включают policies/self-contained resources; feature template у to-spec, legacy routes сохранены.
- README, CONTRIBUTING, сценарии описывают candidate, владельцев/пределы наблюдений.

## [0.51.0] - 2026-10-31

### Добавлено

- `rnd-grill`: discussion-only candidate с доказанными раундами выбора, общими discussion/domain rules и resume boundaries.
- `to-decision`: согласованное/незавершенное сохранение, glossary/ADR, прямые доменные запросы и сохранность повторов.
- Checker/сценарии покрывают candidates, explicit policies/self-containment; manual/coordinator routes сохранены.

### Изменено

- README описывает вызов/отдельное согласие сохранения, CONTRIBUTING - владельцев/расширение имен независимых процессов.

## [0.50.0] - 2026-10-31

### Изменено

- `dev-lead` завершает HUD до release controller, сохраняя final status, чужой UI и non-replayed close evidence при recovery.

## [0.49.0] - 2026-10-31

### Добавлено

- `dev-lead`: lead-only timestamped status/HUD и durable bounded questionnaire transport, recovery ownership обновленного HUD, реальные approval/form regressions и release-controlled pending fixtures; решения остаются lead.
- `dev-setup`: явный global/project `--readiness` с native discovery, реальными диагнозами/советами без setup writes/install.

### Изменено

- `dev-lead` проверяет, review/spec/commit-ит принятые реализации/fixes до следующего независимого ticket, сохраняет conservative commit recovery/final feature review. README/восемь SVG пар показывают agterm-only delegation, manual routes, readiness, local status/journal/runs, отдельные ticket/checkpoint acceptance, Mono/читаемые подписи.
- Runtime tests/сценарии покрывают checkpoint composition, lost commit replies, foreign index, readiness/setup, отличают fixtures от consumer/live.

### Исправлено

- Lead outcome packets/schema/controlled rules уточняют status fields/file artifacts native emitters.
- `dev-lead`/`dev-review` runner заново проверяют артефакты/команды после terminal observation с journal-prefix growth; regressions покрывают missing/changed evidence до cleanup.
- Generated-form regression запускает submit script существующим Node, проверяет decoded choice/text; без Node пропускается лишь JS, controls/probes работают.

## [0.48.0] - 2026-10-30

### Исправлено

- `dev-lead`/`dev-review` runner (2026-10-30) требуют stopped processes/groups до продолжения/launch, в том числе после exit 0; regressions - surviving children/destination rejection.

### Изменено

- Lead требует verified agterm entry до эффектов координации, закрепляет destinations/normalized unique labels.
- Lead/review runner отдельно хранят terminal/pane ownership и native session, закрывают проверенно остановленные shell/command-wait terminals, включая answered/resolved blocked turns принятого exact continuation, с recorded non-replayed cleanup.
- Runtime tests/сценарии: identity/focus/names/cleanup/lost close reply, fixtures отдельно от live.

## [0.47.0] - 2026-10-30

### Изменено

- `dev-lead` поддерживает native Claude Code/Codex/OpenCode v2 discovery, effort validation, outcomes и exact-session continuation без подмены runtime.
- `dev-review` содержит native CLI adapter всех ролей с enforced write denial в Claude Code/OpenCode read-only runs.
- Packets/guides/сценарии различают registration/pinned context, native permissions, protocol/live; shared helpers/CI покрывают адаптеры.

## [0.46.0] - 2026-10-30

### Добавлено

- `dev-lead`: Codex-only последовательный координатор с feature/ticket approval, видимыми agterm workers, bounded outcomes, независимой приемкой.
- Lead helpers обнаруживают реальные skills/models, сохраняют launch/commit intent, проверяют outcomes/recovery без повтора неизвестного.
- Идентичные journal/controlled resources в dev-lead/dev-rnd/dev-bug/dev-review/dev-spec/dev-commit.
- Регрессии: вопросы, неверные результаты, обнаружение возможностей, блокировки, прерывания, потерянные ответы, дубли и устаревшие доказательства.

### Изменено

- `dev-rnd --decision-only` сохраняет вывод/доказательства/вопросы без tickets; обычный вызов сохраняет spec/slicing.
- Executor/tracker записывают outcomes, принимают lead approval лишь в явно разрешенном controlled context.
- Review содержит Codex read-only finders/verifier со старыми ролями/владельцем отчета.
- Spec/commit сохраняют source/Git boundaries, записывая journal events; spec readers включают lead.
- `SPEC.md` фиксирует построенные controller/journal/acceptance boundaries.
- Шаблоны `dev-setup` предлагают journal rules без изменения установки при source development.
- README, CONTRIBUTING, сценарии описывают lead, invocation, local artifacts/пределы.
- Checker валидирует седьмой skill/shared runner/journal/runtime isolation; CI сохраняет `House style + frontmatter` и lead regressions.

### Исправлено

- CI объявляет `pull_request` вместе с `push`, чтобы PR запускал обязательные checks.

## [0.45.0] - 2026-10-28

### Добавлено

- `dev-spec` записывает постоянные specs построенного: committed SPEC.md или private .SPEC.md через exclude клона.
- `dev-setup project` одним approved diff пишет `## nxs`, правило веток, test/lint/typecheck и ignore .scratch/.
- Setup принимает global/project, без аргумента спрашивает внутри Git и выбирает global снаружи.
- `dev-setup global` соединяет Claude Code/Codex/OpenCode с `~/.agents/AGENTS.md`, объединяя старое вместо замены, добавляет nxs (spec reading/ветки) и выбранные rule groups одним diff.
- Global предлагает `mattpocock/skills` Core (grilling/domain/to-spec/to-tickets), Wayfinding/Architecture/Sessions; добавляет/объясняет зависимости, сверяет upstream, устанавливает одобренное, пишет `## Engineering skill defaults` и `~/.agents/docs/{issue-tracker,triage-labels,domain}.md` с local .scratch/ и нумерацией после старых.
- Global пропускает покрытые вне секции правила nxs с указанием источника; пустая секция не создается.
- Global считает path->source wired, не заменяет его; identical copy связывает без merge, удаляет owned headings из merge, один real file объединяет раз.
- Setup секции принадлежат template: правка внутри nxs заменяется повтором, личное снаружи учитывается covered. Merge под своим `## Merged from <path>`, не внутри конечного nxs.
- Project использует realpath `AGENTS.md`/`CLAUDE.md` и считает nxs по реальным файлам, повтор `CLAUDE.md -> AGENTS.md` обновляет одну секцию.
- Shared project-specs задает чтение dev-rnd/dev-bug/dev-review/dev-spec.

### Изменено

- Ticket/tracker/triage: человек выполняет шаг `ready-for-human`, возвращает ready-for-agent, повторяет /plan; исполнитель проверяет среду, не повторяет шаг.
- Ticket/tracker `## Done when` проверяют реальный результат каждого прямого блокера до правок; одного resolved мало, reference обновлен.
- CONTRIBUTING разрешает setup писать config/rules в client instructions лишь approved diff.
- Dev-spec не создает module spec рядом с foreign SPEC.md, сообщает пропуск.
- Dev-bug классифицирует right/silent/wrong/feature по domain/specs; feature без ticket идет в dev-rnd.
- Wrong fix ticket использует spec лишь контекстом, dev-spec исправляет после кода.
- Dev-rnd принимает root-cause.md источником.
- Review сообщает spec contradiction.
- Согласованную matching замену spec review сохраняет pending dev-spec с тем же verifier rule, не finding.
- Feature-directory считает specs доменными документами.
- Dev-rnd группирует independent questions, варианты как поведение, внутреннее решает сам с причиной в spec.
- Checker test покрывает все shared copies.
- Checker/test ловят различие fenced Done when setup tracker и dev-rnd template.
- Setup единым CONTRACT задает approval/ownership/repeat/no-op/checks; global использует coverage table, project template ссылается на AUDIT step 3.
- Global считает mattpocock установленным лишь по lock source, same-name без него unverified/не перезаписывает/не устанавливает и блокирует dependents.
- Setup tracker нумерует wayfinder child tickets после старых в `issues/`.
- README называет целевых клиентов и `tests/client-scenarios.md` вместо одинакового поведения.

### Исправлено

- CI использует требуемый skills CLI Node 22.

## [0.44.0] - 2026-10-27

### Изменено

- Поставка переходит с plugin dev (marketplaces/OpenCode installer) на standalone skills через skills CLI в shared agents directory с client links.
- rnd/bug/review/commit переименованы в dev-rnd/dev-bug/dev-review/dev-commit.
- Skills объявляют name/frontmatter, содержат свои references/templates/roles.
- Agent launch оставляет generic fresh-context/full-prompt route; plugin agent identities/installer route удалены.

### Удалено

- Упаковка plugins/dev, nxs marketplace manifest, OpenCode installer.

## [0.43.0] - 2026-10-26

### Изменено

- Rnd останавливается после вариантов, stress/spec показывает лишь после выбора; один вопрос в ответе.
- Rnd показывает все четыре части stress перед spec.

### Исправлено

- Rnd после предложения /plan для слишком простой для spec задачи останавливается без spec/tickets.
- `**Branch:**` предлагается и без project branch rule.
- Review tickets всегда содержат `**Blocked by:**`.

## [0.42.0] - 2026-10-23

### Изменено

- OpenCode вызывает rnd/bug/review/commit через `@<name>`.

### Удалено

- OpenCode installer больше не создает `/dev/rnd`, `/dev/bug`, `/dev/review`, `/dev/commit`; update их удаляет.

## [0.41.1] - 2026-10-23

### Изменено

- Commit формулирует правило один раз, заканчивает отчетом шага 5.
- Commit format дает простые глаголы без списка запрещенных.
- Rnd/bug оставляют handoff лишь во введении; rnd сначала изучает код, затем неясный термин.
- `review-quality`/`review-testing` передают naming findings severity bar; `review-simplification` описывает большие in-scope fixes как reviewer.
- Client-testing guidance перенесен из agent launch в contributor guide.
- Заголовок review использует lowercase имя команды.

## [0.41.0] - 2026-10-23

### Изменено

- Commit description охватывает ограниченные запросы ("commit only X") и все коммиты ведет через скилл.

### Исправлено

- Bug сохраняет `root-cause.md`/open ticket при той же подтвержденной причине.
- Commit format запрещает body/trailers без запроса.

## [0.40.1] - 2026-10-22

### Изменено

- README больше не описывает необязательный revdiff-planning.

## [0.40.0] - 2026-10-21

### Добавлено

- OpenCode 2 installer `opencode/install.py`: копирует версию в config, регистрирует skills, `dev/review-*` subagents, `/dev/<name>` и `/plan`, если его нет.
- Agent launch OpenCode: subagent с установленными `dev/<role>` и host permissions.
- Сценарии установки, invocation, /plan и review launch OpenCode.

### Изменено

- Rnd/bug/review/commit descriptions называют OpenCode `/dev/<name>`.
- Rnd/bug предлагают `/plan <ticket-path>` и в OpenCode.
- README описывает установку/проверенные шаги OpenCode.

## [0.39.0] - 2026-10-21

### Добавлено

- Review-verify проверяет каждого объединенного кандидата, возвращает confirmed/plausible/refuted с цитатой.
- Review сохраняет plausible не выше major, с подтверждением в summary/tickets.
- Собственная conventions check цитирует правило `CLAUDE.md`/`AGENTS.md` и нарушенную строку.
- `review-simplification` проверяет reuse и неверный уровень fix.
- `review-quality` проверяет потерянные при переносе guards и wrappers, обходящие экземпляр.

### Изменено

- Review VERIFY применяет verdict verifier вместо собственных проверок.
- Finders дают `Scenario:`; quality передает неясный trigger verifier вместо удаления.
- Report требует `verdict:` у findings/dismissals, старый без verdict невалиден и запускает новый проход.

## [0.38.3] - 2026-10-18

### Изменено

- README называет проверенные Codex шаги и однокомандную установку Claude Code.
- Descriptions rnd/bug/review/commit называют Codex `$dev:<name>`.

### Удалено

- Email автора из Claude Code manifest.

## [0.38.2] - 2026-10-17

### Добавлено

- README называет revdiff-planning необязательным /plan companion, проверенным Claude Code.

## [0.38.1] - 2026-10-16

### Исправлено

- Review scenarios восстанавливают fixture .scratch/ перед каждым ticket answer, полностью игнорируют .scratch/.
- Повторное review явно запрашивает fresh sweep; Checked requirements stage-ит diff feature branch.
- Requirements ожидает spec.md вместе с resolved ticket.

## [0.38.0] - 2026-10-16

### Изменено

- Review tickets включают location/Problem каждого finding в What to build.
- `Branch:` записывается и на base branch, опускается только detached HEAD.
- Review ищет покрытие в открытых `.scratch/reviews/<branch-slug>/issues/` и `issues/` установленной функции.
- Bug при новой причине и open fix ticket спрашивает до записи: обновить приемку или закрыть.
- Ticket reference убирает список command branch values; bug берет project rule с `<type>` = fix.

### Исправлено

- Staged review/currency не зависят от origin/HEAD/main/master.
- Status/Branch ticket читаются из той же staged-версии текста.
- Покрытый finding сохраняет ticket path после ответа вместо none.

## [0.37.1] - 2026-10-16

### Исправлено

- Ticket reference не требует общей ветки всех tickets, соответствует `Branch:`, записанным bug/review.

## [0.37.0] - 2026-10-16

### Изменено

- Bug пишет следующий fix ticket, если прежний resolved/wontfix.
- Сценарии покрывают resolved repeat, `ready-for-human`/clarification в Plan Mode, clear-request /plan, review feature/ticket, documentation check, base-branch tickets.

## [0.36.0] - 2026-10-16

### Изменено

- Review ticket начинает приемку с воспроизведения до fix; невоспроизведенное названо/критерии сняты, wontfix лишь если ничто не воспроизвелось.
- Ticket reference разрешает исполнителю снять такие критерии, wontfix лишь при полном невоспроизведении.
- Review без аргумента читает resolved tickets текущей ветки в `.scratch/reviews/<branch-slug>/issues/`.
- Покрытое открытым ticket уходит в `Already ticketed:` вместо нового предложения, `review.md` сохраняет путь в `ticket:`.
- Agent launch убирает saved notes из пакета reviewer.

## [0.35.0] - 2026-10-16

### Изменено

- Review предлагает группы номеров: отдельный critical/major без причины объединения, minor с major того же места, остальные minor вместе.
- Ответ - номера ("1, 3", "all", "7 separately", "1 and 3 together", "none"), выбранное следует группам.
- Review показывает открытый выбор/рекомендацию; нерешенное замечание получает отдельный needs-info.
- `review.md` до ответа хранит `ticket: proposed <finding numbers>`.

### Удалено

- Метки `T<n>` предлагаемых tickets.

## [0.34.0] - 2026-10-16

### Изменено

- Rnd передает ясное клиентскому /plan вместо /dev:plan.
- Commit/commit format только для самостоятельных коммитов.
- Agent launch покрывает лишь три review roles.
- Ticket reference не упоминает `## Implementation`; статусы ready-for-human/resolved ставит executor Done when.

### Удалено

- Команды `plan`/`exec`, шаблон реализации и режим `exec no commits`.
- Роль `worker`.
- Каталог `checks/` функции.

## [0.33.0] - 2026-10-16

### Добавлено

- Review предлагает tickets, объединяя общую причину/fix/перекрытие, создает лишь выбранное текстом.
- Поле `ticket:` у каждого finding в `review.md`.
- Проверка ожидаемой нагрузки в `review-quality`.

### Изменено

- Один review mode: staged, иначе branch против base; empty index на базе останавливает.
- Review сам проверяет требования/docs, summary дает назначение, проблему, fix, цену отказа.
- Требования находятся по resolved tickets с `Branch:` текущей ветки.
- Report заменяет `## Mode` на `## Sweep`.
- Ticket reference допускает wontfix по первому критерию review ticket.

### Удалено

- Команда `fix`.
- Режим `review quick`, селекторы staged/пути и аргумент fix.
- Роли `review-implementation`/`review-documentation`.
- Поля `fix:`, `fixed at:`, `re-check:`, `result:`, `mode:` и marker `review_phase: recheck`.

## [0.32.0] - 2026-10-16

### Добавлено

- Ticket reference владеет template, номерами, полями/статусами rnd/bug/plan.
- Необязательный `Branch:` и дословный Done when для `/plan <ticket-path>` в harness Plan Mode.

### Изменено

- Bug пишет один fix ticket подтвержденной причины, ни одного неподтвержденной.
- Rnd/bug предлагают `/plan <ticket-path>`.
- Rnd предлагает `Branch:` каждому ticket; bug ставит `fix/<feature-slug>`.
- Plan пишет новые tickets по reference.
- Exec не исполняет Done when ticket.

## [0.31.0] - 2026-10-16

### Изменено

- Review quick запускает `review-quality`/`review-implementation` в обычных границах без tests/simplification/docs.
- Fix коммитит `fix(<scope>): address review findings`.

### Удалено

- Prompt marker review_mode: quick и quick-mode секции ролей quality/implementation.

## [0.30.1] - 2026-10-16

### Изменено

- Review/fix читают severity/verification из findings.
- Review/fix читают format/validation/currency из review-report.
- Commit/exec читают message/Git rules из commit-format.
- Rnd/plan/bug читают location/storage/tracker/external specs/domain из feature-directory.
- Agent-launch - единый reviewer packet review/fix с read-only checks.

## [0.30.0] - 2026-10-16

### Добавлено

- Rnd сохраняет исследование/raw data в research/ функции.
- Bug сохраняет probes в research/.
- Plan кладет local checks в `checks/<NN>-<slug>/`.

### Изменено

- Exec пишет `Branch:` для каждого нового старта с коммитами.
- Review находит resolved tickets ignored .scratch/ по `Branch:`.

## [0.29.3] - 2026-10-14

### Изменено

- Commit определяет scope по области, останавливается лишь при неясном type.

### Удалено

- Повтор branch naming rule в commit.

## [0.29.2] - 2026-10-14

### Добавлено

- `review-quality` проверяет контракты комментариев измененного кода.
- `review-quality` проверяет retries/restarts/instances, необеспеченные допущения и непроверенные входы file/network/subprocess/environment.

## [0.29.1] - 2026-10-13

### Исправлено

- Codex plugin metadata включает discovery семи dev commands в BB.

## [0.29.0] - 2026-10-08

### Изменено

- Exec заново читает следующий ticket: plan для непланированного, exec для планированного.
- Exec один раз спрашивает перед новым committing start на review base branch.
- Plan пишет по существующему ticket без отдельного approval turn, если вопросов нет.
- Plan перед записью сопоставляет приемку/task checkboxes, спрашивает при буквальном несовпадении.
- Plan предлагает точную spec revision, когда ответ меняет принятое решение.
- Сценарии покрывают unplanned/next-ticket/base starts/named plans/spec revision.

## [0.28.0] - 2026-10-05

### Изменено

- Rnd/bug/plan read-only читают существующие глоссарий/решения затронутой области.
- Rnd показывает противоречащий решению подход; plan переносит термины/решения в Conventions.
- `review-documentation` и `review-implementation` в quick сообщают устаревший из-за diff glossary/decision record.

## [0.27.2] - 2026-09-18

### Изменено

- CHANGELOG сокращен до однострочных bullets, формат задан CONTRIBUTING.

## [0.27.1] - 2026-09-18

### Исправлено

- Rnd пропускает ordinary/bold Type при выборе implementation ticket для plan handoff.

## [0.27.0] - 2026-09-18

### Изменено

- Rnd/plan только local Markdown, без tracker config/backend/выдуманных внешних команд.
- Rnd принимает approved specs/совместимые артефакты, сохраняет решения/блокеры/историю при slicing.
- Rnd классифицирует decision inputs, требует source/parent/blocker evidence, отвергает части, проверяемые лишь финальной интеграцией.
- Plan сообщает missing execution plans по наблюдаемому.

## [0.26.0] - 2026-09-18

### Изменено

- Руководства упрощены вокруг выбора команды.
- Plan отделяет new-ticket planning от frontier, блокирует fix неподтвержденной причины, сохраняет гипотезы до опровержения.
- Exec проверяет clarification до старта, сверяет completed commits до повторных checks.
- Exec требует полных worker packets, останавливается при partial result.
- Review/fix читают отмеченную приемку как требования, разделяют report gates.
- Commit только standalone, сохраняет постороннее staged/unstaged.
- Guides описывают контракты/повторяемые сценарии вместо line-count targets.

## [0.25.0] - 2026-09-17

### Изменено

- Exec/review/fix используют явные packets/capability checks, fresh-context наряду с native named agents.
- Review планирует всех обязательных reviewers по доступной емкости.
- Guides описывают prompt-only, пределы клиентов и воспроизводимые сценарии.

## [0.24.0] - 2026-09-17

### Изменено

- Rnd/bug/plan/exec/review/fix требуют явного вызова Codex, как Claude Code; commit принимает natural-language requests.
- Обсуждение, цитаты и handoff не вызывают команды.

## [0.23.4] - 2026-09-10

### Изменено

- Rnd/plan templates перенесены в skill-local assets.

## [0.23.3] - 2026-09-10

### Изменено

- Guides кратко переписаны с централизованным client setup/ссылками на владельцев правил.

## [0.23.2] - 2026-09-10

### Изменено

- Guides добавляют Codex setup, invocation, isolated preview.

## [0.23.1] - 2026-09-10

### Изменено

- Guides описывают оба клиента, routing/no-commit/review scope/commit activation.

## [0.23.0] - 2026-09-07

### Добавлено

- Exec сохраняет worker decisions/deviations в Comments и передает следующим.
- Exec записывает task/git mode/start commit/остаток и сверяет прерванное при новом вызове.

### Изменено

- Resume exec сохраняет no commits, останавливается при неатрибутируемых изменениях.
- Tracked ticket получает task commit как receipt, без bookkeeping commit.

## [0.22.2] - 2026-09-07

### Изменено

- Rnd до подходов показывает поведение, точки правки/reuse и пишет находки в spec.
- Plan переносит решения/исключения в task text или Conventions.

## [0.22.1] - 2026-09-07

### Изменено

- Review/fix используют одну severity bar каждому reviewer.
- Verification прослеживает reachable triggers, цитирует, отличает доказанное от выведенного.
- Неясные/ошибочные identifiers - minor; стиль сам не finding.

## [0.22.0] - 2026-09-06

### Добавлено

- Fix применяет saved report, проверяет open findings, коммитит код до записи результата.
- Review сохраняет confirmed/dismissals/follow-ups в `review.md` между сессиями.
- Review quick запускает двух более широких reviewers, пишет mode.

### Изменено

- Review пишет лишь report; fix владеет bounded re-check.
- `review-quality`/`review-implementation` принимают `review_phase: recheck`.
- Test runs могут создавать disposable caches/build, tracked не меняются.

### Удалено

- Fix как argument review.

## [0.21.0] - 2026-09-06

### Добавлено

- Exec переоткрывает переданный resolved ticket после называния нарушенной приемки/вопроса.
- Exec передает связанную приемку как `Serves:` и сверяет task changes до commit.
- Review принимает ticket/feature как цель.
- Worker сообщает точные команды и запуск после последней правки.

### Изменено

- Exec закрывает ticket до последнего task commit, полный suite/linter один раз при закрытии.
- Exec не повторяет уже успешный после последней worker edit тест.
- Plan убирает 3-7 tasks/final verify task, предлагает direct edit для одношагового, владеет needs-info/ready-for-agent.
- Review пишет base для staged, читает resolved из diff, после третьего re-check остаток unresolved.
- Bug убирает минимум 3-5 гипотез.

## [0.20.1] - 2026-09-05

### Изменено

- Worker results могут содержать Decisions/Deviations, exec/review fix передают в final report.
- Review передает verification/fix history обоим re-check agents.

## [0.20.0] - 2026-08-29

### Добавлено

- Rnd делит spec на `issues/NN-<slug>.md` по зависимостям.
- Exec идет по frontier, один ticket/run, пишет `**Status:**` claimed/resolved/ready-for-human/needs-info.
- Rnd/plan проверяют tracker config до первой записи новой функции.
- Rnd/bug/plan не пишут в каталог с map.md.
- Plan сам проверяет headings/checkboxes/blocker order.

### Изменено

- Артефакты в `.scratch/<feature-slug>/`: `spec.md`, `root-cause.md`, `issues/`.
- Rnd пишет spec с семью заголовками.
- Plan добавляет `## Conventions`/`## Implementation` в ticket вместо plan file.
- Exec коммитит code+tracked ticket вместе, иначе только code.
- Review берет цель ticket без status line.
- README/CONTRIBUTING описывают features/tickets/status/frontier.

### Устарело

- Story directory, без миграции.

## [0.19.2] - 2026-08-11

### Добавлено

- `review-quality` проверяет смысл каждой удаленной/замененной строки.

### Изменено

- `review-quality` читает enclosing function целиком и называет конкретные ловушки.
- `review-testing` покрывает несовпадающие setup/teardown.

## [0.19.1] - 2026-08-11

### Изменено

- Rnd/bug/plan принимают local ticket на строке `- Tracker:`.

## [0.19.0] - 2026-08-09

### Добавлено

- Review read-only по умолчанию; review fix применяет confirmed через worker, коммитит/re-check.
- Report review называет dismissed.

### Изменено

- Review: пять agents, затем два re-check лишь при confirmed critical/major.
- Worker принимает список confirmed findings единицей работы.
- Exec/plan указывают review fix рядом с review.

### Исправлено

- Selectors staged/path доходят reviewers; `PR / MR URL` удален.
- `review-implementation`/`review-documentation` работают с branch без plan/цели.
- Plan заполняет `## Conventions`, передает plan -> exec.

## [0.18.0] - 2026-08-09

### Изменено

- Rnd/bug/plan/exec/review type-only (disable-model-invocation: true), commit сохраняет model invocation.
- Rnd/bug/plan снова несут tracker-ticket rule.

### Удалено

- SessionStart hook и hooks/.

## [0.17.0] - 2026-08-08

### Изменено

- Plugin nxs -> dev в `plugins/dev/`; команды `/dev:<name>`, agents `dev:<name>`.
- CONTRIBUTING/README ограничены plugin, repository-wide rules в корне.
- docs/nxs/ остается путем артефактов.

### Исправлено

- Frontmatter review-simplification снова валиден.

## [0.16.1] - 2026-08-08

### Изменено

- Commit description называет trigger: просьба коммитить вне exec.

## [0.16.0] - 2026-08-08

### Изменено

- CONTRIBUTING добавляет ubiquitous-language table и все три handoff contracts.
- Rnd/bug называют story/slug/date rules; task в rnd становится request.
- Plan читает source по заголовкам, не затирает plan.md молча.
- `review-implementation` принимает требования root cause.

### Удалено

- Archiving rule plan/exec; архивирует пользователь.

## [0.15.0] - 2026-08-08

### Изменено

- Review запускает пять agents параллельно, проверяет, исправляет confirmed/коммитит до трех раундов.
- Plan поглощает plancheck/plan-conventions с template/decomposition.
- Exec выполняет план целиком, коммитит каждую green task.
- Commit поглощает commit-conventions.
- Rnd/bug сокращены.

### Добавлено

- `review-quality`, `review-implementation`, `review-testing`, `review-simplification`, `review-documentation` - самодостаточные read-only reviewers.

### Удалено

- Background skill tier, plancheck, plan-reviewer, две старые review lenses, development approaches, review внутри exec, examples/.

## [0.14.0] - 2026-07-31

### Изменено

- Plan task - полная способность через слои; plan-conventions нацелен на 2-5 задач, потолок 7, задает критерии деления.
- Exec сравнивает large diff с Files задачи, поднимает review-fix до пяти раундов.
- Plancheck считает slicing NIT, не BLOCK.

### Удалено

- Цель ~5 checkboxes/task и split/merge thresholds.

## [0.13.1] - 2026-07-28

### Удалено

- Recaps `## RULES`, дубли exec, essence summaries plan-conventions, лишнее self-description.

### Изменено

- Reviewer instructions - простые повелительные фразы, термин один на понятие.

## [0.13.0] - 2026-07-28

### Добавлено

- Plancheck: plan review policy BLOCK/NIT/DROP и fixtures.
- Review-fit-reviewer заменяет implementation/simplification.
- Review выносит axes reference из policy.

### Изменено

- Plancheck классифицирует, требует `Impact:` с конечным состоянием.
- `review-quality-reviewer` владеет также test coverage/quality.
- Review/plancheck reports начинаются с verdict/counts/scope.

### Удалено

- Роли `review-implementation-reviewer`, `review-testing-reviewer`, `review-simplification-reviewer`.

## [0.12.0] - 2026-07-28

### Добавлено

- Read-only fallback на docs/nxs/briefs/ и docs/nxs/plans/ в Spec axis.

### Изменено

- Один story directory `docs/nxs/stories/YYYYMMDD-<slug>/` с `brief.md`/`root-cause.md`/`plan.md`.
- Plancheck/exec выбирают последнюю story с plan.md.

## [0.11.0] - 2026-07-23

### Добавлено

- Commit делает atomic conventional commits рабочих правок.
- SessionStart hook внедряет using-nxs discipline.

### Изменено

- Commit-conventions - только соглашение, exec commit gate у exec.
- Rnd/bug/plan убирают INTAKE.

### Удалено

- Фоновый скилл `intake`.

## [0.10.1] - 2026-07-22

### Исправлено

- Source section plan имеет одно имя `## SOURCE ARTIFACTS`.
- Review/plancheck разрешают protocol path внутри plugin.
- Exec определяет TDD по `## DEVELOPMENT APPROACH`.
- Headings/template fields/self-descriptions согласованы.

### Удалено

- examples/epic-sample.md, examples/adr-sample.md, повторный output block plan-reviewer.

### Изменено

- Rnd/bug принимают вход без tracker key.
- CONTRIBUTING описывает agent frontmatter/полную структуру.

## [0.10.0] - 2026-07-22

### Изменено

- Brief suffix называет автора-команду: -rnd.md/-bug.md.

## [0.9.2] - 2026-07-22

### Удалено

- Справочник исходных code smells Fowler.

### Изменено

- Review сокращен до того, что модель не может вывести из проекта.

## [0.9.1] - 2026-07-22

### Изменено

- Review/plancheck findings используют `Issue:`/`Impact:`/`Fix:`.
- Review-protocol: четыре шага verification, unconfirmed удаляются.
- Plan-reviewer сверяет план с repo, пишет реальную команду.
- CONTRIBUTING переведен на английский.

## [0.9.0] - 2026-07-22

### Удалено

- Команды `dialectic`, `wrong`, `epic`, `explain`, `clean`, `recommit`, `techdoc`, `userdoc`.
- Фоновые скиллы `stress-test`, `doc-draft`, `decision-log`.
- Агенты `explorer`, `diagnose-investigator`.
- Разделение `exec` на default/auto.

### Изменено

- Plancheck использует одного plan-reviewer.
- Exec/commit-conventions вносят references в SKILL.md.
- Артефакты в docs/nxs/plans/ и docs/nxs/briefs/.

## [0.8.0] - 2026-07-22

### Добавлено

- Необязательный `## CONVENTIONS` в plan.

### Изменено

- Exec передает task/приемку/conventions каждому worker.
- Worker следует переданному, остальное берет из окружающего кода.

## [0.7.0] - 2026-07-14

### Добавлено

- Epic получает Tasks/statuses/map header/modes/notes/closure.
- Clean архивирует завершенные epic maps.
- Образец `examples/epic-sample.md`.

### Изменено

- Имя epic map с tracker key, Frontier task -> prep.
- Plan проверяет все блокеры до планирования epic task.

## [0.6.0] - 2026-07-13

### Изменено

- Bug root-cause brief содержит tracker ID в имени.

## [0.5.0] - 2026-07-13

### Добавлено

- Rnd пишет inline brief skeleton с Acceptance criteria и предлагает full-collapse escape hatch.

### Изменено

- Brief/plan names содержат tracker ID.

### Исправлено

- Приемка rnd имеет фиксированное место в brief.

## [0.4.0] - 2026-07-11

### Добавлено

- MIT LICENSE, manifest metadata, `CHANGELOG.md`/version convention, CI и PR template.
- `examples/` с CLAUDE.md.sample и образцами артефактов.
- Doc-draft предупреждает, если docs/ не ignored Git.

### Изменено

- Review lenses технически read-only.
- Descriptions задают triggers, каждая команда получает Example.

### Исправлено

- Дубли commit/review, старые self-names, противоречия exec/doc-draft.

## [0.3.0] - 2026-07-09

### Добавлено

- Epic для многосессионной работы.
- Fowler code-smell baseline в quality/simplification.

## [0.2.0] - 2026-07-08

### Изменено

- Orchestrator внедряет единый protocol kernel каждому lens agent.
- Shared kernels для stress/doc drafting/TDD/bug diagnosis.
- Skills используют tool-agnostic tracker.

## [0.1.0] - 2026-07-06

### Добавлено

- Первый выпуск /nxs:* command skills, background rules и read-only review/plan agents.
