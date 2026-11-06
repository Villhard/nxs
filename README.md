# nxs

Восемь самостоятельных skills для основного flow разработки с coding agents. Инструкции задают цель и этапы; способ выполнения выбирает модель.

## Установка и обновление

```bash
npx skills@latest add -g Villhard/nxs
```

В меню выбираются skills и клиент. Устанавливается опубликованная версия. Обновление выбранного skill:

```bash
npx skills@latest update -g dev-exec
```

Источник и предлагаемый diff показывают, какая установка изменится. Локальная разработка описана в [CONTRIBUTING](CONTRIBUTING.md#local-development-and-release).

## Какой скилл выбрать

| Скилл | Назначение |
| --- | --- |
| [rnd-grill](skills/rnd-grill/SKILL.md) | Обсудить задачу и согласовать решения. |
| [to-spec](skills/to-spec/SKILL.md) | Сохранить проблему, решение и приемку. |
| [to-tickets](skills/to-tickets/SKILL.md) | Подготовить самостоятельные результаты, зависимости и ветки. |
| [dev-exec](skills/dev-exec/SKILL.md) | Выполнить ticket в отдельном worktree с проверками и коммитами. |
| [dev-review](skills/dev-review/SKILL.md) | Проверить результат по стандартам и требованиям. |
| [sync-spec](skills/sync-spec/SKILL.md) | Обновить project specs по реализованному. |
| [rnd-debug](skills/rnd-debug/SKILL.md) | Исследовать сбой и сохранить диагноз. |
| [dev-commit](skills/dev-commit/SKILL.md) | Закоммитить выбранные существующие изменения. |

## Порядок работы

Обсуждение → task spec при необходимости → tickets → исполнение → review → исправления и повторная проверка → sync реализованного. Диагностика дает дополнительный вход в подготовку; commit доступен отдельно.

Skills вызываются независимо, подходящие этапы выбираются по задаче. Синтаксис `/` или `@` зависит от клиента.

По умолчанию records лежат в `.scratch/<feature-slug>/`: `spec.md`, `branch.md`, `issues/<NN>-<slug>.md`, `root-cause.md`. Предварительная настройка не требуется.

[SPEC](SPEC.md) описывает контракты; [CONTRIBUTING](CONTRIBUTING.md) - структуру и проверки. Проверки исходников сами по себе не доказывают совместимость всех клиентов.
