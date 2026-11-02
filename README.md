# nxs

Девять самостоятельных skills для обсуждения, подготовки и выполнения задач coding agents.

## Установка

```bash
npx skills@latest add -g Villhard/nxs
```

Выбери skills и клиента в меню. Устанавливается опубликованная версия; локальный candidate - по [CONTRIBUTING](CONTRIBUTING.md#локальная-разработка-и-публикация).

## Какой скилл выбрать

| Скилл | Назначение |
| --- | --- |
| [rnd-grill](skills/rnd-grill/SKILL.md) | Обсудить решение без записи. |
| [to-spec](skills/to-spec/SKILL.md) | Сохранить согласованную спеку задачи. |
| [to-tickets](skills/to-tickets/SKILL.md) | Подготовить самодостаточные проверяемые tickets. |
| [dev-exec](skills/dev-exec/SKILL.md) | Выполнить один ticket с проверками и коммитами. |
| [dev-review](skills/dev-review/SKILL.md) | Независимые Standards/Spec reviewers, без правок. |
| [rnd-debug](skills/rnd-debug/SKILL.md) | Подтвердить причину сбоя без исправления кода. |
| [sync-spec](skills/sync-spec/SKILL.md) | Обновить проектную спецификацию по реализованному. |
| [dev-commit](skills/dev-commit/SKILL.md) | Закоммитить выбранные существующие правки. |
| [nxs-setup](skills/nxs-setup/SKILL.md) | Настроить по одобренному diff или сообщить readiness. |

## Порядок работы

```text
/rnd-grill Как лучше ограничить число запросов к API?
/to-spec Сохрани согласованное в .scratch/rate-limit/spec.md
/to-tickets .scratch/rate-limit/spec.md
/dev-exec .scratch/rate-limit/issues/01-limit.md
```

Синтаксис `/` или `@` зависит от клиента. Вызовы явные; `dev-commit` также принимает прямую просьбу закоммитить. Для бага начни с `rnd-debug`; малой согласованной задаче достаточно `to-tickets`. `dev-review` и `sync-spec` вызываются отдельно: автоматической цепочки нет.

`dev-exec` коммитит проверенные шаги. Неизвестный выбор ветки согласуется до реализации и сохраняется в ticket. `Do not commit` останавливает исполнение; автоматического push нет.

## Где хранятся записи

По умолчанию: `.scratch/<feature>/spec.md` и `.scratch/<feature>/issues/<NN>-<slug>.md`. Спека задачи хранит намерение; проектная SPEC - реализованное.

Другой tracker настраивается через `nxs-setup`. Недоступный настроенный tracker останавливает операцию, а не переключает ее на локальное хранилище.

## Обновление и настройка

```bash
npx skills@latest update -g dev-exec
```

Проверь source и весь предлагаемый diff: фильтр имени не ограничивает источник. Не подтверждай незапланированное удаление или замену чужого skill. `nxs-setup` не устанавливает tools или skills.

Файлы и установка не доказывают совместимость клиента. [SPEC](SPEC.md) - контракты и ограничения; [CONTRIBUTING](CONTRIBUTING.md) - изменение и проверки; [GLOSSARY](GLOSSARY.md) - термины.
