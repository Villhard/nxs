# nxs

Восемь самостоятельных skills для обсуждения, подготовки и выполнения задач coding agents.

## Установка

```bash
npx skills@latest add -g Villhard/nxs
```

Выбери skills и клиента в меню. Устанавливается опубликованная версия; подробности - в [инструкции установки и обновления](docs/installation.md).

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

## Пример работы

```text
/rnd-grill Как лучше ограничить число запросов к API?
/to-spec Сохрани согласованное в .scratch/rate-limit/spec.md
/to-tickets .scratch/rate-limit/spec.md
/dev-exec .scratch/rate-limit/issues/01-limit.md
```

Это пример, не обязательная цепочка: skills самостоятельны и вызываются отдельно, следующие автоматически не запускаются. Синтаксис `/` или `@` зависит от клиента.

`dev-exec` коммитит проверенные шаги, но не делает автоматический push.

## Документация

Без настройки tracker записи хранятся в `.scratch`; предварительная настройка не нужна. [Подключение другого tracker и Backlog.md](docs/trackers.md).

[SPEC](SPEC.md) - контракты и ограничения; [CONTRIBUTING](CONTRIBUTING.md) - изменение и проверки.
