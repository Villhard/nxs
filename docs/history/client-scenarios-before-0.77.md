# Архив клиентских сценариев до 0.77

Архивировано 2026-11-01 при переходе на семь скиллов. Ниже перевод исторического протокола: старые инструкции/неподдержанные команды, наблюдения, ошибки и пределы сохранены по смыслу. Это не текущий test plan и не доказательство новых ресурсов. Текущий контракт - [сценарии](../../tests/client-scenarios.md) и [ADR 0009](../adr/0009-seven-skill-direct-flow.md). Старые относительные пути/локальные evidence references сохраняют прежний смысл, не считаются заново проверенными ссылками. Служебные строки и заголовки старых fixtures приводятся в исходной форме.

## Исторический каталог

Сценарии сочетали source checks/прежние наблюдения, не доказывающие registration/end-to-end. Каталог содержал 19 команд; dev-rnd/dev-bug/dev-lead/dev-setup были удалены из source. Installation/route cutover не проверены. Старые сценарии не команды текущего каталога и не гарантия клиента. Прежний dev-setup предлагал companions, nxs-setup нет. To-tickets предлагает dev-exec для готовых tickets; source removal не мигрирует старые tickets/установки.

## Делегирование встроенным subagents

Nxs-lead передает ограниченную работу native subagents клиента: fresh context, полный prompt, ответ/ожидание. Имени tool мало; записываются tool/schema/model/effort/wait/permissions/continuation.

| Случай | Нужное наблюдение |
| --- | --- |
| Capabilities | Изучи exposed tools/schemas; отсутствие context/wait/model/protection сообщается по причине. Prompt-only review отдельно от enforcement, без nested CLI. |
| Writing | Один writer получает полный packet/cwd/allowed writes/result contract без parent chat; lead пишет intent до запуска. |
| Needs input | Ticket planning возвращает needs_input; lead сохраняет вопрос/approval, продолжает ту же session только при документированной поддержке, иначе новый bounded run с approved plan. |
| Независимая приемка | Done сверяется с артефактами, приемкой, командами/Git, сам envelope не принимает работу. |
| Read-only review | Три finders, затем verifier native; отчет пишет lead. Prompt-only не называется enforcement; state checks и при enforcement. |
| Потеря ответа | Launch сверяется с host records/artifacts, не повторяется автоматически. |
| Вопросы | Native dialog, если доступен, иначе разговор; точные question/answer/one-time use в журнале. |
| Recovery | До повтора сверяются journal, packets, IDs, артефакты, HEAD/index/tree. |
| Два результата не по порядку | Связать ответы с host IDs, дождаться обоих, проверить каждого до зависимого. Launch acknowledgment не result. |
| Pending/lost, нет wait/auto continuation | Сообщить incomplete/реальный предел, не обещать background/завершение, сверить эффект до повтора. |
| Branch/worktrees | При чужом worktree и ignored data перечислить пути/ветки без "stale"/удаления. Отдельный cleanup сначала осматривает tracked/untracked/ignored; неполный осмотр/сохранность блокируют. |
| Нет worktree listing | Сообщить ошибку, не заявлять пустоту и не чистить. |
| GitHub/targeted update | В disposable установить опубликованные выбранные skills, обновить одно имя; повторить collision/different source. Сверить paths/provenance/чужие bytes до/после. Name filter не source filter, local preview отдельно; до наблюдения непроверено. |

По случаю на клиент: версия, tool/model/effort, permissions, prompt class, результат. Недоступное не заменяется симуляцией/другим клиентом; наблюдение не гарантия.

Наблюдалось 2026-11-01: OpenCode 2.2.5 exposed subagent; свежий explore прочитал skills/dev-lead/SKILL.md и references/subagents.md, вернул capabilities/stop, отсутствие terminal/HUD/controller, seven-field envelope/lost-reply rule. Свежий general создал только `.scratch/native-subagent-observation/write.txt`; независимый `od -c` подтвердил 3 bytes (`ok` и newline). Codex CLI 0.166.0 exposed collaboration.spawn_agent/followup_task; read-only codex exec запустил child, прочитавшего GLOSSARY.md/вернувшего `# nxs`, parent ждал через collaboration. Claude Code не установлен, без попытки install. Это только случаи, не полное packet propagation/enforcement/development cycle.

## Структурные проверки

Check-skills проверяет catalog/frontmatter/invocation/roles/shared/ticket Done when/внутренние links/external boundaries/CHANGELOG; check-no-runtime запрещает .py, bundled scripts/__pycache__ и active docs со старым Python/terminal/helper. Обе CI/pre-commit; source pass не behavior pass. При source removal проверяется ровно 19 команд/отказ extra, shared bytes, сохраненный research/dev-lead/ в recovery reference и прежнее исполнение tickets, не live recovery.

## Вызов

Каждый случай в новой сессии, смотри tools/artifacts, не только ответ.

| Вход | Ожидание |
| --- | --- |
| Объяснить off-by-one/refactor/оценку diff/правила AGENTS | Без вызова нет workflow/artifacts/instruction writes. |
| Оценить цитату handoff с rnd-debug/rnd-grill/dev-review/dev-spec/nxs-setup | Только обсуждение, цитата не вызов. |
| Явно выбрать каждый из пяти выше | Доступен, соблюдает входные условия на synthetic artifacts. |
| Попросить commit prepared fixture | Natural-language selection допустим. |
| Объяснить коммит | Без коммита. |
| Завершить research/review/spec/setup | Стоп на передаче, дальше лишь по новому запросу. |

## Локальные передачи

Это прежние маршруты, не текущие команды. Для измененного используй baseline/candidate и repeated native-run из прежних "Contract regressions". Fixtures готовь заранее; закрепи все bytes/source/tests/index/HEAD, raw prompts/events/snapshots/per-expectation outcomes держи в disposable root. Проверь реальные installed resources, не version label. Не меняй live tracker/обычную установку.

Маленькая greeting function, готовые checks, без deps. Spec - старый seven-heading template с опускаемыми пустыми optional, ticket - local template/optional Branch/Comments. External consumer проверяется дословным заполнением изученных to-spec/to-tickets templates с source version/hash вне пакета; это конкретная ревизия, не live production/all upstream.

| Случай и вход | Нужное наблюдение |
| --- | --- |
| Standalone rnd: нет feature, согласованы default/uppercase, разрешен local spec/ticket | Читает свои templates/ticket rules, пишет spec/ready ticket с предложенным Branch/дословным Done when/без Implementation, предлагает `/plan <ticket-path>`. Нет external/setup/code/next launch. |
| Clear request: одношаговая greeting-правка | Называет spec церемонией, предлагает прямо /plan; до согласия нет файлов/кода/следующей команды. |
| Bug fix: limit=0; повторы same/new cause при open, затем resolved/new cause, затем невоспроизводимый симптом | Без domain records класс silent, намерение согласуется до ticket. Confirmed: root-cause + issues/01-*.md с `fix/<feature-slug>`, repro/regression criteria, /plan handoff; код неизменен. Same open: нет дубля. New cause/open: вопрос до записи, оба файла прежние. New cause/resolved: issues/02 и его /plan, 01 прежний. Unconfirmed: нет ticket/ready handoff. |
| Bug classes: по одному root GLOSSARY/accepted ADR/module .SPEC говорят limit=0 пуст; повтор говорят fallback ten | Right в Root cause без вопроса намерения, один ticket. Wrong с путем записи: сначала одобрение исправления. What to build для glossary/ADR называет исправляемую запись; spec лишь контекст с "dev-spec corrects it after the fix", без spec edit. Wrong spec предлагает dev-spec, glossary/ADR/right нет. Bytes записей прежние. |
| Ticket Plan Mode: fresh Claude /plan и approval | Работает на Branch, полный suite/linter pass, все criteria/resolved/Comments на решение, HEAD прежний, без commit. Needs-info, unresolved Blocked by, открытый marker в ready ticket и feature spec - до любых edits вопрос. New third-party dep - ready-for-human, одна Comments с dep, без кода. |
| Blocker после выбора Branch: resolved result сначала есть; (a) ветка без кода, (b) новая с carried uncommitted, (c) squash/cherry-pick, (d) ancestor затем revert | A/d пишут одну missing Comments и стоп до реализации без вопроса; b/c evidence Comments и продолжение. Не merge/cherry-pick/implement блокер. |
| Human return: человек вернул ready-for-agent (e) с install, (f) без | E проверяет среду без повторного install, resolved/evidence Comments; f снова ready-for-human/Comments, без code/install. |
| Clarify: два независимых выбора, третий зависим, один internal-only | Первый раунд два вопроса вместе с 2-4 вариантами поведения/рекомендацией; зависимый позже, internal не спрашивается, reason в Implementation Decisions. |
| Direct spec: одобренный two-unit, затем one-unit, внешний источник | Reuse/осмотр/slicing без повторного shaping, one-unit один ticket; разрешенная локальная копия внешнего сохраняет source bytes. |
| Source marker | Нет ready ticket/handoff, назван точный вопрос. Вопрос spec блокирует все slicing, draft approval не отвечает. |
| Collision: другой external spec/target map.md | Без overwrite; differing spec требует конкретной revision, map прежняя/отдельная feature. |
| Repeat: ready, ready с legacy Implementation/Comments, resolved с checked criteria | Все bytes/graph сохранены, одобренное новое после max number; graph revision требует конкретного согласия, не general save. |
| Decision: явный Type вне map, отдельно map input | Классификация до записи, preserve, отдельный implementation deliverable, если не дан; не /plan decision. |
| Mixed: без map, approved spec, 01-decision Type: decision и 02-implementation без Type, оба ready/no blockers; повтор bold Type | Оба прежние, /plan лишь 02, decision context сохранен, запусков нет. |
| Remote parent missing | Назван missing parent context, нет ready handoff/выдуманных условий/remote writes. |
| Remote blocker unknown | Запрос доказательств, не None, разрешенный draft needs-info. |
| Open/unmapped remote, номер совпал с чужим local | Готовность остановлена, нет implicit local dependency, ограничения сохранены. |
| Mapped: open затем resolved без pending close; также verified closed remote | Local number сохранен, blocked до local resolution; resolved передается, удовлетворенное remote evidence в контексте, без sync. |
| Local storage: нет tracker config, затем чужая GitHub/GitLab preference | Только local .scratch после content/input gates, без поиска preferences/setup/backend/storage consent/remote calls. Legacy config bytes прежние. Isolated client settings/наблюдаемая host config записаны без заявления config-free host. |
| Domain: термин/avoid synonym + accepted ADR, запрос против обоих; повтор без них | Канонический термин без вопроса, конфликт с путем до записи, glossary/ADR прежние. Без документов то же поведение, без вопроса отсутствия. |

Проверено для 0.32.0 в Claude Code CLI 2.1.301: Bug fix первый/open repeat/unconfirmed; Plan Mode needs-info stop. Clear request, resolved repeat (0.37.0), new cause repeat (0.38.0), прочий Plan Mode и Codex /plan не проверены. Для 0.45.0 в Claude Code CLI 2.1.312 проверены b/c/e/f. После 0.45.0 в том же клиенте a/d пишут missing Comments и останавливаются без вопроса/merge/cherry-pick/implementation; b/c пишут evidence и продолжают.

Remote используй synthetic/read interface, без live writes. Stop-case доказывает лишь границу. Полный candidate rnd -> /plan -> review проверяй отдельно fresh invocations с artifact/Git evidence. Для handoff-only не повторяй посторонние review/launch, сохрани контракты ниже.

## Проверка изменений

Fixture: reachable defect, устаревшая фраза README, pinned requirement/feature branch; .scratch ignored, source/index/HEAD до каждого прохода.

1. Stage diff, review без аргумента: quality/testing/simplification параллельно/группами одинакового scope, verifier после всех/все merged candidates. Scope staged, complete лишь после results/currency. Собственный documentation finding цитирует README. Summary: назначение, серьезность/номера, что/проблема/fix/цена, verdict, `Dismissed: N`, tickets. Code/index/HEAD прежние.
2. Grouping: два несвязанных major, minor рядом с первым и два minor отдельно, один с выбором. Recommended tickets группирует номера без labels, majors отдельно, первый minor с major, прочие вместе с рекомендацией выбора. Перед каждым ответом верни .scratch к исходному без review/issues, новая сессия. Ответы: major+первый minor (один ticket), all, separately, оба majors together (один), нерешенный choice (отдельный needs-info, прочие ready), неизвестный номер (вопрос/без записи), none. Только выбранное, template/Branch=current/repro first, ticket field путь/none.
3. Commit diff, review без staged: scope branch против merge-base. Unstaged в Not checked, не review.
4. Base branch/empty index: объяснение/без report. Review quick/code path останавливают до записи. Base со staged: scope staged, выбранный ticket Branch=base. Без origin/HEAD/main/master и отдельно с обеими main/master staged review все равно идет.
5. Нет agent route/читаемого exposed verifier: стоп до отчета, trivial direct pass допустим. Mid-run launch failure incomplete, не успех.
6. Без feature: выбранный finding дает `.scratch/reviews/<branch-slug>/issues/` с текущей веткой/repro first. Новый fresh review до исполнения показывает путь/Already ticketed без дубля. После /plan и git add ticket resolved с repro Comments. Новый review читает ticket disk Requirements/What to build goal, не no stated goal, report там же. Combined ticket из двух, один уже hand-fixed: resolved, не wontfix, dead finding Comments/его criteria сняты.
7. Staged/feature: spec Problem Statement/Solution, resolved+ready tickets без Branch: Requirements включает resolved/spec, не ready; цель оттуда. Явный ready ticket вместо feature включает этот ticket независимо от status/Branch и spec.
8. Verdicts: staged нарушает правило AGENTS, check-then-write на README-разрешенном concurrent shared file без теста и apparent unguarded строка с guard выше. Conventions цитирует rule/path/line. Guarded refuted с guard, race plausible <=major/confirm, summary plausible/What would confirm it, ticket plausible; confirm. Report 0.38.3 без verdict невалиден/новый sweep.
9. Agreed spec change: staged против Contracts корневого project SPEC (другой заголовок делает foreign). Resolved current-branch ticket называет заменяющее поведение и diff совпадает: не finding, Follow-ups pending dev-spec с origin/citation/path. То же явный ready ticket - не finding. Только spec path без поведения, второе непроговоренное противоречие, несовпадающий replacement diff - findings.
10. Смена executor: неизмененный SVG вне diff со старой активной командой - finding, отдельная точная legacy description нет. Повтор со stale accessibility. Staged SVG stale/index и fixed/unstaged - finding, обратное - нет. До наблюдения непроверено, source inspection не pass.
11. Prompt-only host/fixtures с staged/unstaged/untracked/ignored: честные ограничения, реальные HEAD/index/full-tree comparisons вокруг groups/verifier, продолжение лишь unchanged. Повтор host enforcement - checks остаются. Persistent mutation каждого state или unreadable/incomplete compare дают incomplete, все preserve, без reset/ticket selection. Missing другая capability до report mutation. Fingerprints без secrets; reverted-between не обнаруживается. Нужен native run.
12. Nested repo/submodule: захвати content, внедри persistent change во время group, повтор unavailable full inspection. Incomplete до verifier/ticket selection, предел/изменение названо, без reset/cleanup. Нужен native run.

Проверено 0.33.0 в Claude Code CLI 2.1.301: 1/3, one-ticket answer старых labels, оба stops 4. Documentation 1 (0.37.0), staged variants 4 (0.38.0), numbers/grouping 2 (0.35.0), 5, cycle 6 (0.36.0), requirements 7 (0.37.0), verdicts 8 (0.39.0), Codex не проверены. Для 0.45.0 в Claude Code CLI 2.1.312 проверены все пять случаев 9.

## Спецификации

Та же greeting fixture, feature branch/.scratch ignored. До каждого source/index/HEAD/exclude.

| Случай и вход | Нужное наблюдение |
| --- | --- |
| First: нет specs, uncommitted boundary rule модуля, feature path | До записи один вопрос visible/hidden. Visible пишет только module SPEC с установленным/template, без root; code/index/HEAD/.scratch прежние, предлагает dev-commit. |
| Только local variable rename | Без вопроса/записи, "nothing durable changed". |
| Повтор first | Собственный SPEC не вход, без правок. |
| Hidden, повтор fresh | .SPEC + одна exclude line, status скрывает spec и показывает лишь fixture; повтор без вопроса. Уже .gitignore - без exclude. Последняя *.log без newline - отдельные строки *.log/.SPEC, logs еще ignored. |
| Оба вида рядом/в разных модулях | Spec стоп до записи с путями/ручным rename/delete. Review/rnd/bug читают по пути и сообщают ту же ручную правку. |
| Committed private; затем untracked/unignored | Первый стоп с именем, второй hidden без вопроса, exclude до записи, status скрывает private. |
| Case-insensitive macOS, только spec.md с нарушаемым контрактом | Нет SPEC/.SPEC, исходный spec прежний, модуль skipped с именем. Staged review не берет его в finding. |
| Foreign proto/SPEC своего формата; изменение proto/greeting с boundary | Foreign bytes прежние, нет proto/.SPEC, не считается для MODE (вопрос), proto skipped. |
| Missing feature path | Стоп до вопроса/записи. |
| Причина boundary нигде не указана | Inferred reason unconfirmed без content question, назван в отчете; последующее противоречие только ему не finding. |
| Уже committed на base, больше ничего | Стоп: committed base-branch work не поддерживается. |
| Readers/.SPEC contract | Staged contradiction дает citation/path, добавление непокрытого поведения нет. Rnd/bug находят точным listing, не меняют. |
| Bug feature: .SPEC закрепил reported behavior | Root cause feature/path, без ticket, `/dev-rnd <root-cause path>`; он пишет соседний spec.md, диагноз прежний. |

## Настройка

Старый dev-setup, не текущий каталог. Greeting fixture без ignore .scratch; закрепи instructions/.gitignore/exclude/index/HEAD.

| Случай и вход | Нужное наблюдение |
| --- | --- |
| Makefile test/lint, AGENTS с чужой секцией, нет typecheck, approve | Audit tests/lint source, missing typecheck, unignored; один diff nxs+default branches/make test/make lint и private exclude, .gitignore альтернатива. Только одобренное, check-ignore=0, index/HEAD прежние. Вариант *.log без newline в обоих ignore: отдельно approve exclude и на свежей fixture .gitignore; строки раздельные, другой файл прежний. |
| Package без Makefile, pnpm lock, lint=eslint src, CI pnpm test/npx eslint ., decline | Audit test/package и оба lint sources. Предложены pnpm test/pnpm lint, не npm/yarn. Все captured bytes прежние. |
| Нет instructions, approve; затем только CLAUDE | Создает AGENTS+nxs и CLAUDE import; вариант меняет только CLAUDE, без AGENTS. |
| AGENTS и symlink CLAUDE -> AGENTS, два вызова | Первый добавляет секцию реальному файлу, повтор already set up без duplicate/write/diff. Symlink прежний, один nxs. |
| CLAUDE regular import @AGENTS | Меняет AGENTS, CLAUDE bytes прежние. |
| Два независимых файла без import | AGENTS target, CLAUDE назван альтернативой, после approval прежний. |
| Оба со своим nxs | До question/diff стоп с обоими paths/lines, все bytes прежние. |
| Repeat, затем новый typecheck target | Первый no-op; второй только Typecheck line, один nxs, вне него bytes прежние. |
| Decline Makefile | Файлы/index/HEAD прежние, ничего не записано. |
| Без аргумента внутри/вне Git, decline; foo внутри | Внутри спрашивает project/global до audit, снаружи global disposable HOME без вопроса. Foo называет допустимое/стоп без audit/question/write. |

Global: клиент под disposable HOME лишь с candidate/auth; до каждого bytes/ls -la ~/.agents (docs/skills/.skill-lock.json), ~/.claude/CLAUDE.md/skills, ~/.codex/AGENTS.md, ~/.config/opencode/AGENTS.md.

| Случай и вход | Нужное наблюдение |
| --- | --- |
| Empty HOME: accept Communication, edit Git rule, decline прочее/bundles, approve | Одна group question до diff. Все clients/nxs missing. Создает source Communication/Git с правкой/nxs last, Claude import @~/.agents/AGENTS.md, два symlinks с realpath source; declined отсутствует. |
| Regular Codex с двумя rules, один equivalent template; decline groups/bundles, approve | Source получает Codex verbatim, Codex заменен link, equivalent не предложен. Вариант Claude без import: import первым, прочее bytes прежние. |
| Source symlink -> regular Codex | Codex wired без merge/link; остается regular со старыми rules+nxs, source печатает то же, без symlink loop. |
| Еще OpenCode link -> ~/notes/rules.md | Каждый real file merge раз под своим Merged from, оба client paths links/source; former target прежний/его строки сохранены. |
| Broken Codex -> ~/gone.md | Заменен link без merge, target source, gone отсутствует. |
| Codex identical copy source+nxs | Без duplicate stop/merge heading/новых source lines, только link, source прежний/один nxs. |
| Codex и source со своим nxs | Стоп до question/diff с paths/lines, все bytes прежние. |
| Global repeat; затем старое Branches | Первый не предлагает accepted/covered, re-offers declined, после decline no-op. Второй меняет только эту строку, один nxs/без дублей/вне секции bytes прежние. |
| Repeat merge двух bullets без heading после source ending nxs | Под Merged from после nxs, links Codex. Повтор не удаляет bullets/no-op, они вне nxs/template. |
| Все declined на прежнем/пустом HOME | Прежний no-op/bytes. Пустой показывает wiring/nxs без rules; отказ оставляет HOME пустым. |
| Только Core, нет mattpocock | Upstream list без missing, вопрос Core recommended, Wayfinding/Architecture Needs Core, Sessions со смыслом/skills; setup-matt-pocock-skills нигде. Один add -g mattpocock/skills -s шесть Core без required by, diff Engineering skill defaults до nxs/три docs. Lock лишь шесть, docs=templates. Нет install network - команда человеку, source/docs все равно пишутся. |
| Upstream listing failed через PATH npx shim/log/exit1 | Ошибка не missing skill; четыре bundles предложены. Log лишь listing, не add. Exact six Core command человеку, source/docs пишутся без install. |
| Только Wayfinding | Required grilling/domain-modeling, add wayfinder/research/prototype/grilling/domain-modeling, не grill-me/grill-with-docs/to-spec/to-tickets. Уже grilling через add -g mattpocock/skills -s grilling -a claude-code -y - не повторяется/required line отсутствует. Чужой research/SKILL без lock - unverified/collision, wayfinder blocked, install лишь prototype/grilling/domain, чужое прежнее. |
| Sessions с handoff-missing в candidate bundles.md | Назван missing upstream, исключен из offer/install; другие три установлены, без похожей замены. |
| Installed to-spec от mattpocock | Mark/lock сохранены, не overlap dev-rnd, install другие пять Core. Modified triage docs + decline bundles - inplace diff, отказ bytes. Installed setup-matt-pocock-skills - audit installed, не offer/install/remove, directory/lock прежние. |
| Core repeat | Предлагает остальные три, не Core, без duplicate headings; decline no-op. |
| Covered nxs reading/branches вне owned section | Covered с цитатой, без пустого nxs/source changes. Иное `<name>-<ticket>` branch rule конфликтует/не пишется; spec rule по-прежнему covered. |
| Source Style reasoning-first, Git explicit commit/push/PR, Checks все verification; accept Communication/Git | Answer-first conflict с line, verification covered. Communication без конфликтующего, Git только branch rule. Старый Git на месте до Checks, новый Communication после Checks до nxs, все original lines прежние/без дублей. |

## Клиент OpenCode

Это discovery старого каталога. Disposable install: `HOME=<temporary dir> npx skills add <checkout> -g -a opencode`, запуск `OPENCODE_CONFIG_DIR=<temporary dir>/.config/opencode opencode --standalone`. Вызов `@dev-<name>`, tool calls из `opencode session export <id>` с child sessions.

| Случай | Нужное наблюдение |
| --- | --- |
| Discovery server, два listing (первый мог быть до load) | Dev-rnd/dev-bug/dev-review/dev-spec/dev-setup с auto off, dev-commit; нет dev/* commands/dev/review-* agents. |
| Invocation prompts через `@dev-<name>` | Поведение секции вызова, загружается installed copy. |
| Review step 1 | Три finder launches/full roles/packets/no parent chat в одном response, verifier после результатов. |
| Missing role | Переименуй candidate roles/review-quality.md; step 5 останавливается до launch/report bytes прежние. |
| Role tools/write probe | Prompt запреты сохранены; без enforced allowlist child еще может писать, review сообщает это. |
| Plan -> Build (Shift+Tab), ticket path/execute | Plan без edits/branch change, Build resolved/suite pass/HEAD прежний/без commit. |

Проверено для 0.40.0 в OpenCode 2.1.2 plugin installer: discovery, четыре invocation prompts, первый bug ticket, clear request (вопрос, затем /plan без записи), review 1/one-ticket/review launch/missing roles, tools, Plan handoff. Skills distribution 0.44.0 и generic launch в OpenCode не проверены.

## Отчетность

### Промежуточные коммиты и готовность

Candidate instructions передаются явно как task files с hashes, не считаются installed registration. Нужны consumer runs/actions, не prose assertions. Global setup проверяется virtual path/content map и read-only action/diff proposals без HOME redirect/config writes. Write-capable fixture требует точной цели/bounded packet, проверенных controller до запуска, внутри разрешенного fixture directory; не personal config.

| Случай/запрос | Нужное наблюдение |
| --- | --- |
| Два tickets A/B, checkpoint каждый, fixture code/checks/plan approval/explicit scopes; finding в review A | Dev-exec проверяет каждый блок, dev-commit в своей сессии до следующего; отдельное review после A, выбранный fix проверен до приемки. Lead проверяет commit IDs/scope/checks/preservation. Dev-spec отдельно при нужде; без push/PR/неявной стадии. |
| Research/no-op, без implementation, затем empty commit group | Evidence/journal handoff либо успешный no-op, не empty commit. |
| A/B committed, остается task change, закончить всю feature | Review включает оба tickets/остаток, затем final checks/spec/commit reconciliation. Прежние ticket reports сами не закрывают feature. |
| Потерять successful commit response после durable intent, restart; варианты HEAD unchanged/unrelated prior/later, index/files/branch changed/missing evidence | Реальные Git objects/intent, без replay/duplicate. Только exact current evidence доказывает effect, сомнение явно; checkpoint/status cache восстановлен без коммита. |
| Чужой staged README/целый свой file, commit только его; затем mixed hunks | Разрешенный --only сохраняет чужие bytes. Generic reconcile может быть uncertain, проверяй selected diff/parent/tree/preservation. Mixed - до index mutation стоп без alternate-index/stash/rewrite/whole-file. |
| Пустой index, separable hunks, commit лишь task fix | Только task hunk, все working bytes/чужой unstaged сохранены. |
| Оба readiness, complete observations/missing/current/custom inputs | Timestamp/cwd/executable, Git/native subagents/CLI/individual skills/models с evidence/limits. Нет setup audit/diff/questions/install/upstream/hooks/UI/workers/instructions/ignore/index/HEAD/journal/status. Повтор та же граница. |
| Readiness без Git/CLI/subagent capability/с restricted model catalog | Разные причины/советы, unavailable не absent client; независимое продолжается, dependent unknown. Без remediation/fallback, normal/manual usable. |
| Native skills/models: absent/disabled/partial/error/unconfirmed path/wrong cwd/timeout/empty models/no effort | Missing лишь successful complete discovery; errors/unknown отдельно. Только реальные metadata в report, без model choice/default. Native paths/hashes/pinned-context limitations явны. |
| Global virtual: custom вне sections, symlink identities, no bundles; proposal-only/repeat/decline correction | Preserve bytes/targets/approval. Current repeat без writes, correction лишь owned lines, decline без effects/install. Это virtual consumer, не live HOME writes. |
| Root-authorized disposable project: first approve/repeat/new check target/decline | Точный section/ignore diff, без дублей, custom/newline прежние. Repeat no-op, target меняет лишь owned line, decline preserves files/index/HEAD. Нет personal/installed writes. |

Оценка по tools/reports/input hashes и before/after files/links/modes/directories/index/HEAD: passed/failed/unverified на ожидание. Catalog probe не доказывает workers/enforcement. Global HOME writes не входят. Source/installation не behavioral pass; missing auth/tools не заменяется simulation. Prompt restrictions отдельно от host allowlist.

## Сценарии native lead

Прежний dev-lead, не current candidates ниже. Disposable repo/selected client, approvals лишь fixture. Raw evidence локально research/dev-lead/, публично выводы/пределы.

| Случай | Ожидание |
| --- | --- |
| Discovery | Tools/model/effort/точные paths/hashes, failed не missing. |
| Research | Dev-rnd --decision-only subagent пишет вывод/факты/вопросы без tickets; normal slicing остается. |
| Вопрос | Needs_input сохраняется, fixture answer продолжает документированную session, иначе новый bounded approved run. |
| Approval | Пользователь закрепляет feature plan/scope, lead ticket plan до правок, journal path не разрешение. |
| Sequential | Одна ветка, реальные blocker results, executor проверяет/не коммитит. |
| Review | Explicit task-only staged, три finders/verifier native, отчет только orchestrator, reproduced in-scope fix. |
| Spec/commit | Specs лишь dev-spec, dev-commit atomic без source changes/push. |
| Recovery | Второй lead не запускает writers, lost launch/commit не replay, stale не completion. |
| Standalone | R&D/decision-only/ticket/review/spec/commit сохраняют диалог/вход/status и журнал значимого. |

## Кандидаты обсуждения и сохранения

Ticket 11 добавляет rnd-grill/to-decision рядом со старыми маршрутами. Это протокол, не live pass; registration/checker/model раздельны. Task-local stage-02 reports хранят per-client/raw; unavailable непроверен.

Disposable repos/homes, только selected candidate/resources. Запиши exact path/hashes/version/native-vs-pinned/permissions/session ID. Source/index/domain/feedback - sentinels, bytes/modes после turn. Approvals лишь fixture, не production install/source edits.

| ID/вход | Ожидание |
| --- | --- |
| DS-01 rnd-grill: две разные retention policy, приоритеты неизвестны | Evidence/варианты/recommendation, ждать выбора, без artifacts/code/index/install. |
| DS-02 clear decision, discussion-only/no save | Вывод без интервью, без decision/spec/ticket/domain writes. |
| DS-03 to-decision save agreed discussion, нет content approval | Показать текст/путь, ждать до записи. |
| DS-04 decline DS-03 | Без files/index/install и нового taskless journal. |
| DS-05 save unfinished: agreed limit/proposed strategy/feedback/open priority, approve shown | Четыре состояния отдельно с reason/alternatives/links, без spec/tickets. |
| DS-06 resume без нового противоречия/reconsider | Limit/feedback сохранены, лишь open/newly contradicted reopened. |
| DS-07 exact approved glossary, ADR declined | Лишь термин существующего формата, остальное прежнее, без decision wrapper/feature dir. |
| DS-08 repeat с manual feedback, затем другая revision без approval | Identical no-op, manual/history survives, changed ждут. |
| DS-09 HTML approval без save request | Нет save/next stage/unseen Markdown/domain. |
| DS-10 authorized lead handoff/exact save/final HTML path | Defense существует и linked; missing blocks claimed handoff, coordinator сам не стартует. |
| DS-11 exact prior content/path approval | Reuse/verify bytes/source, без повторного вопроса. |
| DS-12 каждый отдельно без другого/companions | Свои resources, missing next skill назван без чужого install/import/substitution. |

Codex: exact registered path или явно pinned text. Claude: native selection при доступности с evidence. OpenCode: @rnd-grill/@to-decision и resource identity. Slash string не registration. Declined/failed/timed-out evidence сохрани; incomplete generation не passed no-write.

2026-10-31: Codex 0.166.0 зарегистрировал каждый отдельно по exact isolated path с hashes; оба model runs timeout после DNS/connection до discussion/proposal. Claude Code отсутствовал PATH. OpenCode 2.2.5 discovery permission failure, оба runs exit1/EPERM при ps. Source/index/candidate bytes сохранены, DS-01..11 не пройдены; DS-12 только links/install structure. Compatibility/dependent switches непроверены.

## Кандидат описания функции

To-spec пишет только local spec/нужный journal. Disposable/exact isolated candidate, старое/установки сохраняются. Минимальные observation inputs, не обязательная client matrix/гарантия повторов.

- Saved decision: approved default/answered question/exclusion/rationale link/testing requirement; `to-spec <decision-path>` с save approval. Проверить spec/source ID/hash/приемку, исходные решения/project specs/code/index прежние, tickets нет.
- Clear request без material alternatives с разрешенным spec: полезный spec без forced interview/slicing.
- При нужде readiness stop: один authorized draft с unknown или missing parent/blocker; конкретный вопрос/нет ready handoff. Source inspection покрывает identical reuse/revision approval/preservation; новый model run лишь для конкретного сомнения.

Запиши версию/pins/registration-vs-text/permissions/input/artifacts/results отдельно от checks, unavailable оставь. Same-name не выбирает источник. Нет разрешения full route switch/install replacement.

## Кандидат деления описания на tickets

Явно выбранный pinned to-tickets в disposable repo с полным approved spec, малой observable requirement и mixed records. Наблюдай предложение/одобренный новый ticket, зависимости, точную controlled branch где нужна, сохранность старого/dev-exec handoff. Same-session repeat может проверить reuse; без матриц/дублей model runs.

2026-11-01 Codex native subagent получил to-tickets SKILL SHA-256 `5c5eb35057a77346d9f4f7a3ee634e88ab353283e74353b3b55993fd7303ae52`. Fixture approval: предложил/сохранил ticket с точным Done when, предложил /dev-exec. Ticket не выполнялся, observation отдельно от executor, не end-to-end. Mixed records в fixture не было, случай непроверен. Evidence: `.scratch/dev-exec-cutover/live-evidence.md`, `.scratch/ticket-cutover-fixture/decision.log`.

Source review: material questions/drafts, missing sources/remote blockers, graph revisions, plain/bold Type, open/resolved/wontfix. Разделяй наблюдаемое/прочитанное, exact hashes/version/delivery/permissions/artifacts храни в отдельных structural/live evidence функции. Shell checker - packaging/shared/policies/tracker text, не семантика. Прежние failures сохрани; одна проверка/observation не разрешает route/cutover, unavailable остается.

## Кандидат самостоятельного исполнителя

Dev-exec принимает ticket/clear request в текущей session. Проверь plan-before-edit, material reapproval, branch-before-prerequisites, missing-result Comments/stop, human roundtrip, controlled saved-plan approval, native limits/same-session checkpoints. Review/spec отдельно, старые /plan/Do not commit остаются, удаленные producers не доступны. Source/fixtures не live execution/write denial.

Ticket требует full suite/linter: disposable с двумя командами, их реальные результаты до resolved. Missing/failing linter - Comments/unresolved и при focused/syntax pass. Clear request сообщает фактические checks без выдуманного ticket.

Для route switch: маленький disposable repo, existing checks, exact candidate/resources. Concrete plan/approval до edits, проверенный итог/preservation чужого HEAD/index; разрешенный checkpoint может менять HEAD. Выбирай нужный ticket/clear вход; другой наблюдай лишь для его switch/конкретного сомнения. Без matrices/дублей/prose assertions. Controlled: plan hash/approval event/documented continuation или fresh bounded run. Реальные mode/permissions/version/invocation/registration-vs-text/artifacts/stops. Plan Mode при нужде наблюдается отдельно, ordinary run его не доказывает.

Controlled ticket-plan: fixture approvals, два host cases. Documented continuation возобновляет saved session; undocumented - fresh run лишь после reconciliation с approved answer/plan/artifacts/hash/approval/границами. Оба проверяют текущий plan до edits. Uncertain prior effect без evidence останавливает действие, не replay. Это сценарии, не observations.

Ticket fixture из финального template с exact delivered hashes (включая template). Изменился ресурс - повторить affected observations либо оставить непроверенным; прежнее сохранить как свою версию. Live results только recorded cases, unavailable/modes/routes отдельно unverified. Самому candidate не нужен model run; packaging не закрывает switch gates. Automated evidence отдельно/старое сохраняется.

2026-11-01 Codex native subagent получил dev-exec SHA-256 `0fb5eb96a7f77c43270d3c01ee2c644b4172df2e1044a91082550145809c239a` с fixture approval до реализации. Один ticket: suite/linter pass/resolved/HEAD-index прежние; отдельный failing-linter unresolved. CLI codex-cli 0.166.0, host runtime version неизвестна. Не доказывает registration/другие клиенты/Plan Mode/full route; evidence отдельно .scratch/dev-exec-cutover/.

Отдельный Codex run: dev-exec SHA-256 `6302b122fb022bce7b9f63c7bb956623da017281650f43e232e04b8b261e5903`, template `3ee8b0f950b3577f82a6fe340a102210f0eca18004f190193520a224faca9187`. После fixture plan approval suite/linter pass/resolved/HEAD-index прежние. Отдельно от to-tickets, не end-to-end, registration/другие/enforcement не проверены; поздний template не покрыт.

## Дополнительный кандидат диагностики

Rnd-debug на reproduced failure сохраняет discriminating probe/class/cleanup/regression без patch/ticket. Отдельный to-tickets с eligible confirmed cause/approval создает один fix/repeat unchanged. Невоспроизведение/competing hypothesis pending, без ready; feature в discussion, silent/wrong без intent agreement не ready. Open другой причины требует revision decision. Это сценарии, не live claims.

## Дополнительный кандидат выбора замечаний

Dev-review --to-tickets в disposable с subset/grouping: report/selection pin scope/requirements без tickets. To-tickets получает оба, создает выбранные группы, report меняет лишь selected ticket links, covered open bytes прежние/repeat без дублей. Stale/changed requirement/unknown number/incomplete блокируют. Plausible сохраняет reproduce-first/partial handling. Отдельно ordinary ticket route: подходящие created/covered предлагаются dev-exec, blocked/unclear нет, execution не стартует. Не live observations.

## Кандидат независимого исследования

Disposable, не live evidence. Client/version/path/hashes/delivery/permissions/artifacts/source-index, product/result sentinels.

| Случай | Ожидание |
| --- | --- |
| Вопрос по primary sources | Durable attributed findings, contracts отдельно от observations; без decision/spec/ticket/implementation. |
| Source fetch failure/conflict | Предел/несогласие/следующая проверка, не verified negative. |
| Неизвестные приоритеты | Material choice открыт, дальнейшее лишь по покрывающему разрешению. |
| Private config input | Нет value/raw transcript в result/journal и unauthorized disclosure. |
| Research затем явно discussion | Передача evidence в этих пределах, research сам не запускает discussion. |

## Кандидат независимого прототипа

Disposable protocol, не observations. Candidate/client pins/delivery/permissions/artifacts/source-index, product/existing prototype bytes sentinels.

| Случай | Ожидание |
| --- | --- |
| Дешевая проверяемая гипотеза | Runnable experiment/verdict с вопросом/setup/observation/limits без product/ticket. |
| Опровержение | Rejected/observation, прототип сохранен. |
| Нет различения/tool | Inconclusive/missing/next check, не success/failure. |
| Успех без transfer/reuse approval | Source/prototype прежние, product не начинается. |
| Нет deletion approval, включая failure | Файлы/вывод остаются. |
| Не выбран visual/costly/irreversible | Вопрос до dependent action, исходное сохранено. |
| Research/design вне запроса | Предложить, не начать без полномочий. |

## Кандидат дизайна выбранного модуля

Disposable protocol, не live. Candidate/client/delivery/permissions, code/tests/index sentinels.

| Случай | Ожидание |
| --- | --- |
| Два реальных responsibility choices выбранного модуля/callers | Consequences/material choice/content approval, затем interface/evidence/alternatives/verification implications. |
| Missing caller | Предел/без выдуманных потребностей, выбор открыт. |
| Два владельца | Tradeoff/ждать, без ready ticket/неодобренного вывода. |
| Broad architecture без модуля | Спросить selection/предложить отдельный audit, не выбрать молча. |
| Approved design без implementation/test deletion | Source/tests прежние, нет ticket/implementation. |
| Поздняя замена тестов | Явное подходящее согласие и passing new-interface checks до удаления. |

## Кандидат архитектурного обзора

Disposable protocol/pins/delivery/permissions, не live; source/tests/index sentinels.

| Случай | Ожидание |
| --- | --- |
| Разное change pressure границ | Callers survey/ranked evidence/reason/consequences/cost/confidence, без фиксированного числа. |
| Ничего улучшать по evidence | Обоснованный no-change в inspected scope. |
| Недоступная область/caller | Пробел coverage/влияние на confidence, не complete. |
| Первый рейтинг без selection/implementation | Survey/next suggestion, source/tests/index прежние, нет ready tickets/design. |

## Кандидат карты решений

Graph protocol, не live/доказательство любого graph. Disposable/pins/client/delivery/permissions/artifacts, старые answers/code/index sentinels.

| Случай | Ожидание |
| --- | --- |
| Broad unresolved scope | Спросить destination до dependent mapping, не выдумывать. |
| 01 open, 02 зависит от 01, 03 open/unblocked | Frontier 01/03, предложить 01, 02 не работать до resolution. |
| 04 с отсутствующим 02 | Missing prerequisite, не claim 04/не считать resolved. |
| 01/03 unblocked, разрешен лишь 01 | Claim/work лишь 01, 03 прежний, стоп до него. |
| 01 resolved/answer, 02 claimed, 03 open | 01/answer/index прежние; 02 reconcile, не reset; предложить 03. |
| Явный research/prototype | Linked retained evidence/verdict, transfer/deletion отдельно разрешаются. |
| Map completed без implementation, затем отдельный запрос | Mapping без code/ready ticket, поздняя разрешенная задача сохраняет решения/ответы. |

## Кандидат опросника участника

Протокол, не live. Candidate/client/invocation/permissions/artifacts/delivery, external messages/чужое sentinels.

| Случай | Ожидание |
| --- | --- |
| Missing facts для решения, адресат известен | Посильные вопросы/context/consequence/source, без answers/send. |
| Неизвестный адресат | Спросить до персонального документа. |
| Один answer блокирует, прочее независимо | Block лишь dependent, разрешенная подготовка идет. |
| Частичный ответ | Авторство и оставшиеся questions/blockers сохранены. |
| Только approve/open document | Нет contact/submission без отдельного явного запроса. |

## Кандидат передачи контекста

Disposable protocol, не live: source hashes/client invocation/permissions/artifacts.

| Случай | Ожидание |
| --- | --- |
| Journal claim + current evidence | Link journal, claim отдельно от independent verification. |
| Без journal/задача однозначна | Контекст без выдуманного журнала. |
| Fresh session лишь handoff/links | Установлены task/authority/questions/next. |
| Две функции одной ветки | Спросить identity, не выбрать по ветке. |
| Неизвестный commit/launch | Сомнение и нужные evidence сохранены, без replay. |
| Private transcript/secret | Нет secrets/ненужных transcripts. |

## Кандидат ретроспективы одной сессии

Протокол, не live: candidate/session pins/invocation/permissions/artifacts/access limits, постороннее/private сохранены.

| Случай | Ожидание |
| --- | --- |
| Текущий доступный чат | Только он с evidence. |
| Несколько разных доказанных проблем | В report/ответе простая проблема, пустая строка, конкретное решение (место/нужное согласие), без допзапроса ради решения. |
| Проблема без обоснованного fix | Missing evidence, не выдумка; no-change допустим. |
| Явно выбранная session | Только она, без period scan/index. |
| Успешная session | Полезные практики/улучшения либо no-change. |
| Нет transcript/source | Access limit/попросить источник, без выдумки. |
| Передан prior retrospective | Учесть/назвать discovery неполным. |
| Новое личное правило без approval | Только proposal, instructions прежние. |
| Точное разрешенное улучшение | Только его apply/verify/report. |

## Кандидат обычного координатора

Source scenarios, не live. Disposable/task/client/permissions/input pins, bounded native delegation и независимые artifacts/checks/Git. Missing capability останавливает шаг, scope change к пользователю. Техническое plan approval до edits, нет empty commit/push, standalone команды независимы. Enforcement/совместимость отдельно.

| Случай | Ожидание |
| --- | --- |
| Clear request | Проверить goal/facts/decisions, записать вывод/почему без вопросов, не придумывать interview. |
| Material choice | Rnd-grill, передача/ожидание ответа до зависимого. |
| Broad goal | Rnd-map с per-question permission, не implementation approval. |
| Missing stage/permission | Предел и стоп affected, не ложное completed. |
| Multiple blocks standalone/controlled | Approved plan содержит commit scopes; executor checks/dev-commit same-session/identities/safety до следующего, report; lead independently accepts. Review после ticket, spec отдельно; без empty/unapproved push/PR. |
| Indivisible | Один блок для неразделимого, поздний может зависеть от checkpoint. |
| Чужое | Staged/tree сохранены, commit stops соблюдены. |
| Сомнительный commit | Reconcile/evidence/unknown, не replay. |

### Случаи checkpoint исполнителя

Будущие live cases, не результаты. Disposable/pinned candidate/resources, два independently checkable A/B, approvals/actions/checks/HEAD/index/tree. Controlled packet/user/lead approval, standalone human plan approval. Dev-commit доступен в той же session, кроме вариации отсутствия. Client/version/missing capability, source не заменяет native.

| Fixture/вариант | Ожидание |
| --- | --- |
| Новый template, A/B коммитопригодны, commits не запрошены, standalone/controlled | До edits предложить checkpoint/scopes, спросить. Lead проверяет/передает при missing. Нет scope approval - нет commit, affected checkpoint stop. Сохранить plan/question/approval/HEAD. |
| A -> B, оба scope approved, оба режима | Checks до checkpoints, verified A commit до B, реальные paths/preservation; checkpoint может включать несколько atomic commits. Lead independently verifies, standalone сообщает. |
| Неразделимое A/B | Один checkable block/commit лишь когда безопасно, без partial intermediate. |
| Чужой staged file/working edit, затем mixed | Сохранить оба, применить index case, неясное останавливает до mutation/без bypass. |
| Нет/отказ scope, failing check, no permission или dev-commit | Без unauthorized/successful checkpoint, точный blocker, stop affected. |
| Явно без commits, оба режима/без dev-commit | Implementation/checks без checkpoint stops, не commit, передать незакоммиченное. |
| Lost reply/insufficient Git | Reconcile objects/HEAD/index/scope, не replay/не успех при unknown. |
| Старый Do not commit/исторический /plan | Plan без checkpoints, execution/checks продолжаются, no commit, старый execution/history прежние; запрет правится отдельно, template не мигрирует. |
| Обязательное ticket review/два блока | Checks до commit, review после ticket, commit не resolved/lead acceptance, spec отдельно. |

### Регрессии передачи checkpoint

Source-level contract cases, не observations/live-test instructions. Предполагают установленную задачу/handoff, taskless scope не меняется.

| Состояние | Ожидание |
| --- | --- |
| Feature branch с двумя checkpoint, index/остаток пусты | Handoff pin pre-checkpoint HEAD/parents/commits/scope/paths. Review лишь после доказательства обоих в net branch diff, spec сам проверяет вход. |
| Checkpoint при чужом staged | Index сохранен. Staged review пропускает checkpoint, стоп до report; controlled lead передает те же evidence. |
| Checkpoint на base + чужое staged/unstaged | Review/spec стоп и при непустом default input, не complete/no durable change, чужое прежнее. |
| Base/empty index, checkpoint на base по handoff, чужой unstaged/untracked | Прочитать/проверить handoff до no-scope stop, назвать пропуск/неясность. Нет report/голого nothing to review/staging suggestion чужого/расширения, HEAD/index/tree прежние. Missing handoff - unknown/stop. Без identified checkpointed task обычные no-scope/git add suggestion сохраняются. |
| Revert/replacement части checkpoint или unstaged остаток | Ancestry/paths мало. Review стоп при omitted intended net, spec учитывает working остаток/останавливается при unknown. |
| Missing parent/task scope/commit evidence | Unknown/stop affected без completed handoff/partial success, не выдумывать authority/Git. |
| Новый ticket/старый no-commit | Новый копирует current dev-exec/checkpoint дословно, старый prohibition/execution прежние. Checker отклоняет старый both-executor/no-commit template. |

## Кандидат продолжения координатора

Ненаблюдавшиеся cases. После uncertain launch/commit сверить artifacts/host/index/HEAD, не replay из-за одного missing reply. Не хватает evidence - affected action stop, независимое разрешенное продолжается. Открытый вопрос/согласие на changed content не дают полномочий. Native continuation лишь при поддержке active client/known identity, иначе reconcile до fresh bounded worker. Старое сохранить, source отдельно от live.

## Кандидат защищенного auto

Source scenarios, не live. Явно auto, участники/порядок согласия, включая пользователя одного. Critical unanswered participant question блокирует dependent. Standalone HTML открыть с disk без сети/server; проверить comparisons/evidence/assumptions/alternatives/risks/next. Revision требует нового точного approval, dismiss/timeout/probes его не дают. Approval defense не сохраняет decision/не запускает стадию. Implementation отдельно разрешается с lead plan approval/native permissions/scope stops. Behavior/HTML rendering до опыта непроверены.

## Доказательства перехода этапа 6

Native observations выше - единичные случаи, не route/enforcement verification. 2026-11-01 Claude Code отсутствовал PATH: version/invocation/result недоступны, native route/cutover unverified, установки не было. Версии/результаты Codex/OpenCode записаны выше. Shell guard проверяет active tree после runtime removal, история сохраняет evidence. Nxs-lead auto/full coordination не испытаны live. Source legacy удален, callers/installations не мигрированы; cutover требует отдельных evidence/approval.

## Кандидат точечной настройки

Ожидания, не live. Disposable/sentinel files/symlink targets: новый/старый project, current repeat, narrow goal, duplicate/conflicting sections, declined/private content. Exact approved diff/final newline, readiness без writes/доказательства совместимости.

## Кандидат независимой глобальной настройки

Source cases, не live. Disposable HOME: clean/existing instructions, symlink targets, private content/conflicts/duplicates/current repeat/decline. Package полный, пишется лишь approved. Same-name skills/modified installations sentinels, setup не устанавливает/заменяет их. Source capability map не registration.

## Граница перехода настройки

19-command catalog/map проверены как source. Clean install/upgrade/collision preservation/native registration candidate не проверены у всех клиентов; Claude отсутствовал на прошлом native observation. Source removal не закрывает пробелы/не меняет установку. Source checks не live setup/registration.
