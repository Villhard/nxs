# ОТЧЕТ ГОТОВНОСТИ

Только для `project --readiness`/`global --readiness`: сообщи в диалоге нужные предпосылки и остановись. Пропусти обычную настройку, вопросы пакета, предложения, записи и проверки после них. Не создавай отчет, каталог и журнал; не устанавливай зависимости, не меняй instructions/settings/skills/hooks/ignore/Git, не запускай workers/UI/client/server для discovery.

## ОХВАТ И ДОКАЗАТЕЛЬСТВА

Клиент - явно выбранный, иначе определимый активный. Неясный клиент/процесс - `unknown` с недостающим входом; не подменяй клиент и не предполагай координацию. Project смотрит текущий repo; global - лишь нужные shared/client настройки, repo нужен только операции.

Предпочитай read-only tools, текущие client metadata и читаемые local sources. Короткая version/Git identity проба допустима только по необходимости/разрешению. Не отправляй task prompt, не запускай nested CLI, не меняй permissions, не сканируй постороннее private storage и не эмулируй discovery. Кандидат ФС/lock entry не доказывает enabled registration/исполнение. Если доступны точные registered source paths, назови кандидат/provenance; иначе наблюдаемую регистрацию отдели от неизвестного источника. Hash кандидата лишь для различения при нужде, без раскрытия частного.

## НУЖНЫЕ ПРЕДПОСЫЛКИ

Проверяй независимое отдельно; не требуй все строки/скиллы/клиенты для каждой операции.

| Операция | Доказательства | Неполный результат |
| --- | --- | --- |
| Project setup | cwd/repo, читаемые instructions и realpaths, конфликты секций, источники веток/проверок, ignore локальных артефактов. | Назови доступ/неясного владельца/конфликт. Не init/configure Git и не выдумывай команды. |
| Global/узкая настройка | Цели/полномочия, текст, symlink targets/shared source, приватность, наблюдаемая поддержка wiring. | Назови конфликт/непроверенную возможность; не merge частное, не меняй links/config. |
| Выбранный dev skill | Только его enabled registration и читаемые candidate/resources, если exposed; нужные permission limits. | Раздели missing, disabled, unreadable, ambiguous, undiscoverable. Не требуй все семь ради одной операции. |
| Независимое review с workers | Native fresh-context launch/completion, все роли, capacity, доставка контекста, ограничения. Допустимый trivial direct pass без worker. | Назови пробел, останови лишь этот маршрут. Host-enforced отдельно от prompt-only; здесь никого не запускай. |
| Явно выбранная модель/вариант | Реальный ID каталога клиента и объявленные variant/effort metadata, если exposed. | Нет metadata - unknown support, не выдуманный default. Не выбирай модель и не требуй discovery для обычного setup. |

Обсуждение/обычное исполнение не требуют native subagents. CLI, каталог моделей и посторонние установки не универсальные условия. Знакомое имя tool не доказывает schema, completion semantics и enforced permissions.

## ОТЧЕТ И ОСТАНОВКА

Покажи охват, timestamp, нужный cwd, клиент и по строке на применимую предпосылку: наблюдаемый статус, безопасная команда/источник, точный пробел/ошибка, рекомендуемый шаг. Статусы: `verified`, `missing`, `disabled`, `discovery_failed`, `unknown`, `not applicable`. Невыполненные пробы назови с причиной. Отсутствие заявляй только после успешного полного discovery нужного списка; частичный/неуспешный ответ не доказывает missing member. Credentials, частные файлы и raw session output исключи.

Готовность заявляй лишь для успешно проверенных предпосылок. Пробелы отделяй от наблюденных ошибок. Readiness не доказывает worker execution, write protection, регистрацию лишь по disk, весь workflow и маршрут другого клиента. Средства исправления предлагай без выполнения; остановись без setup proposal/автоматической передачи.
