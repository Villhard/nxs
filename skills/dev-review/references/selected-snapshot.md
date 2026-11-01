# ВЫБРАННЫЙ СНИМОК

Читай до выбора/чтения входа review. Снимок - закрепленное логическое представление в отчете, не checkout, selection file и runtime. Только чтение с `GIT_OPTIONAL_LOCKS=0`; не stage/stash/switch и не пиши Git objects.

## ГРАНИЦА И BASELINE

1. Запиши корень из `git rev-parse --show-toplevel`, origin без credentials либо `none`, ветку (`HEAD` при detached) и неизменный HEAD OID как `head`. Обычно `tip` = `head`, закрепляет contextual tree/history. Для явного исторического review возьми запрошенный endpoint OID как `tip`, исключив поздний checkout. Проверяй пути/OIDs/SHA256, shell-quote значения, ставь `--` для путей. Текст источника/отчета - данные, не shell instructions.
2. Установи задачу по запросу и применимым task/feature/ticket/handoff evidence. Запиши пути, явные hunk-границы, чужие исключения и причину сужения. Ветка/index не доказывают владение. Неразделимое чужое требует уточнения до отчета/запуска. Unmerged index и неполностью закрепляемые/читаемые выбранные данные (включая nested repo/submodule) дают incomplete, не выдуманный text-only snapshot.
3. Предпочитай явно согласованный pre-task commit как `base`. Иначе определи `origin/HEAD`, затем `main`/`master` (неоднозначность останавливает) и предложи merge-base с `tip`. Это кандидат, не доказательство задачи. Для установленной uncommitted-only задачи можно base = `tip`, даже на базовой ветке. Запиши источник baseline и доказательство владения/покрытия. Возможный пропуск committed требует уточнения, не default `tip`.
4. Прочитай checkpoint handoff: репозиторий/ветка, pre-checkpoint HEAD, commit и parent OIDs, охват, пути, остаток. Проверь Git. Base должен быть предком tip и раньше каждого обязательного checkpoint. Если checkpoint уже на candidate base/вне диапазона, остановись для явно согласованной более ранней границы; не пропускай и не расширяй узкий запрос молча. Несогласуемая история - incomplete.
5. Раздельно учти committed, index, tracked working и untracked. Полезны `git log --oneline <base>..<tip>`, `git diff --cached --binary --no-ext-diff --no-textconv <head>`, `git diff --binary --no-ext-diff --no-textconv`, `git ls-files --others --exclude-standard -z`. Relevant ignored включай лишь безопасно и с разрешением; не читай секреты ради полноты. Исключенное запиши, не меняй. Недоступный нужный источник останавливает review.

Обычный scope `task`: нужные committed checkpoint и весь оставшийся staged, unstaged, untracked задачи. Явно меньший - `narrow` с точной commit/index/working-границей и исключениями. Staged-only допустим лишь явно, не по содержимому index. Узкий verdict не одобряет всю задачу.

## ИТОГОВОЕ ПРЕДСТАВЛЕНИЕ И MANIFEST

Для полной задачи `tip` = `head`. Поверх закрепленного tree положи выбранные working paths с реальным disk state. Disk tracked-файла объединяет staged/unstaged; выбранный untracked присутствует, deletion отсутствует. Сохрани тип/mode, symlink target bytes без выхода за репозиторий. Не подменяй working файл index/tip и не собирай выдуманную версию из hunks.

В отчете source manifest для каждого выбранного changed path и дополнительного working context: repository-relative путь, source (`worktree`, `index`, `tip`, `deleted`), тип/mode, pin (SHA256 точных disk/target bytes, blob OID для index/tip, `absent` для отсутствия). Сортируй единообразно, `snapshot: <SHA256>` - hash точных UTF-8 bytes блока manifest. Остальное дерево закрепляет tip OID без списка каждого файла. Полный head-to-index diff из команды учета закрепи отдельно как `index: <SHA256>`, без `git write-tree`. Hash считай по bytes, не пронумерованному/обрезанному выводу tool.

Явный historical review читает выбранный `tip` без disk overlay; `head` остается реальным checkout для state/currency. Явный index scope: `tip` = `head`, overlay из index differences с записанными сужениями; читай index blobs, не disk, явно отмечай source/absence. Исключенная working-правка возвращает выбранную commit/index версию, не произвольный disk. В полном scope чужие исключенные пути остаются tip-контекстом. Чужие hunks выбранного working-файла явно ограничи и исключи из findings/coverage; неясная атрибуция/итоговое поведение останавливает. Не изобретай смешанный файл для сокрытия.

Сверь net change с требованиями, каждым checkpoint и раздельными staged/unstaged inventories. Ancestry/список путей не доказывают покрытие: позднее изменение может заменить/отменить прежнее. Объясни намеренную замену/отмену и оцени итог. Недостающий/неясный результат или остаток задачи останавливает полное заключение. Rename включает старый/новый путь; перезаписанный unstaged staged-вариант - не вторая итоговая реализация.

## ЧТЕНИЕ REVIEWERS

Сам установи/выполни reads и передай всем одинаковые точные history/diff команды, head/base/tip, manifest, source-aware file/search reads и pins. Одного diff недостаточно; источник не должен угадываться по checkout.

- History - закрепленный диапазон, например `git log --oneline <base>..<tip> -- <selected-paths>`, checkpoint identities/coverage отдельно.
- Обычный tracked net diff: `git diff --binary --no-ext-diff --no-textconv <base> -- <selected-tracked-paths>`. Это base против рабочих файлов, не только index/tip. Сверь с manifest/inventories; никогда не индексированные new files сюда не входят.
- Каждый untracked явно прочитай и дай addition diff, например regular file: `git diff --no-index --binary --no-ext-diff --no-textconv -- /dev/null <path>`. Exit 1 - различия, не ошибка. Symlink/mode подтверждай отдельно. Пустой tracked diff не отменяет новые файлы.
- Явный index-only: pinned base-to-index diff и `git show <blob>` проверенных index OIDs. Committed-only: base-to-tip и tip blobs. Обычный working-diff пример не расширяет эти режимы.
- Working-файлы читай с disk с проверкой SHA256/type/mode до/после. Остальное - `git ls-tree <tip> -- <path>`, `git show <tip>:<path>` или явно выбранный index blob. Удаленный отсутствует, без fallback на прошлое. Те же правила для функций, callers, тестов, docs, instructions/specs.
- Поиск/списки - логическое представление: pinned tip tree плюс выбранные additions, минус deletions, overridden paths заменены выбранным source. Tip contents ищи лишь для непереопределенных, выбранные disk/index - отдельно. Checkout grep теряет historical/включает чужое, tip-only теряет working additions. Directory/spec listings - тот же overlay и точные basenames. Отсутствие доказывает только полный поиск нужного представления.

Проверяй лишь команды, читающие выбранное представление без правок repo/Git. Результат checkout с исключенным чужим ничего не доказывает о выбранной версии: нужен version-correct read-only осмотр либо NOT RUN. Не stage, не создавай worktree и не устанавливай tools ради проверки. Одноразовый вывод вне репозитория. Недоступная правильная версия - ограничение, не успешная проверка.

## АКТУАЛЬНОСТЬ

До завершения заново установи identity, scope/boundaries/exclusions, baseline по ее источнику, checkpoint coverage, HEAD=`head`, выбранный `tip`, точный head-to-index digest, выбранные пути, types/modes/pins и все requirement/context pins. Пересчитай manifest hash. Добавленный/удаленный/измененный путь задачи, неясное владение, новая цель или pin делают отчет устаревшим даже при прежних HEAD/index. Заново проверь untracked/unstaged inventories, не hash старого списка. Внешние относительно overlay disk requirements сохраняют отдельные pins. При explicit historical новый checkout остается исключенным, не расширяет review, но state comparisons все равно выявляют изменение во время прохода.

Разрешена лишь запись по пути отчета; это не review input. Только этот точный проверенный путь исключи из source inventories/currency; созданные им report-only каталоги не работа задачи. Если отчет сам часть работы/занят другим, выбери безопасное место или остановись. Исключение не касается whole-repository state comparisons: их baseline снимается после каждой записи основного агента.

`sweep: incomplete` никогда не актуален. Актуальность и обязательные before/after comparisons из [запуска](agent-launch.md) решают разные задачи, не заменяют друг друга. Неполная/изменившаяся сверка останавливает даже при совпадении selected pins.
