## nxs

- Проектные спецификации: до правки перечисли корень и каждый родительский каталог файла (`ls -a <dir>`), найди точные `SPEC.md`/`.SPEC.md` и прочитай от корня. Ищи только списками: content search пропускает исключенный из Git `.SPEC.md`, а регистронезависимая ФС открывает `spec.md` вместо `SPEC.md`. В обычной задаче меняет их только `/sync-spec`.
- Ветки: `<type>/<short-description>`, type - `feat`, `fix`, `refactor`, `chore`, `docs`. Правило project instructions важнее.
- Трекер: <Необязательно: путь к Markdown-инструкции; global setup по умолчанию `~/.agents/docs/issue-tracker.md`.>
- Коммиты: <Необязательно: формат сообщений и ограничения; project instructions имеют приоритет.>
