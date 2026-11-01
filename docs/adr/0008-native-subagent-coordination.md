# Встроенные subagents без собственного runtime

`dev-lead` передает каждый ограниченный writing/review шаг native subagents выбранного клиента. Нужны fresh context, полный prompt, результат/ожидание и permissions самого host. Lead решает процесс, пишет намерение в журнал и независимо проверяет результат. Нехватка/запрет возможности останавливает шаг; вложенные Claude Code/Codex/OpenCode не запускаются.

Заменяет [ADR 0001](0001-dev-lead-boundaries.md) в требовании видимого терминала и [ADR 0005](0005-bounded-runs-and-recovery-first.md) в deterministic helpers для inventory, launch, outcome validation, журнала и worktree. Прежнее остается историей.

Репозиторий не содержит Python runtime, bundled scripts и Python suite. Координация - обычные append-only `decision.log`, читаемый `status.md`, feature plan, context packets, ответы subagents. Целостность проверяет shell, active docs защищены от возврата Python helpers/terminal-app coupling. Прежние CHANGELOG/ADR сохраняют историческое содержание.

Отклонено: terminal compatibility layer оставляет удаляемую зависимость; перенос controller/recovery в нового координатора - тот же workflow engine; единый cross-client API обещал бы несуществующую совместимость. Наблюдения записываются по конкретным случаям, не обобщаются в гарантию.
