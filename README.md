# Лабиринт сокровищ

Небольшая консольная игра на Python. Игрок ходит по комнатам лабиринта, собирает предметы, решает простые загадки и пытается открыть сундук с сокровищем.

Проект сделан для тренировки:
- основ Python (словари, функции, циклы и т.д.);
- работы с Git;
- настройки проекта через poetry;
- проверки стиля кода с помощью ruff (PEP8).

## Установка

Клонировать репозиторий:

```bash
git clone [https://github.com/EugeneJBS/project1_Poley_Evgeny_M25-555.git](https://github.com/EugeneJBS/project1_Poley_Evgeny_M25-555.git)
cd project1_Poley_Evgeny_M25-555
```

Установить зависимости (через poetry или Makefile):

```bash
poetry install
```

или

```bash
make install
```

По умолчанию poetry создаёт виртуальное окружение в папке `.venv` (это настроено через `poetry config virtualenvs.in-project true`).

## Запуск игры

Вариант 1 — через poetry:

```bash
poetry run project
```

Вариант 2 — через Makefile:

```bash
make project
```

После запуска в консоли появится приветствие и описание стартовой комнаты. Дальше вводите команды руками.

## Команды в игре

### Основные действия:
- `go` — перейти в направлении (north / south / east / west)
- `north` / `south` / `east` / `west` — то же самое, но без слова go
- `look` — осмотреть текущую комнату
- `take` — взять предмет
- `use` — использовать предмет из инвентаря
- `inventory` — показать, что у вас в рюкзаке
- `solve` — решить загадку или попробовать открыть сундук
- `help` — подсказка по командам
- `quit` — выйти из игры

### Примеры предметов:
- `torch` — факел
- `sword` — меч
- `bronze_box` — бронзовая шкатулка
- `rusty_key` — ржавый ключ от двери
- `treasure_key` — ключ от сундука
- `treasure_chest` — сундук с сокровищем (его нельзя взять, только открыть)

## Как выиграть

Один из вариантов:

В стартовой комнате:
```text
look
take torch
```

Сходить в комнату с ловушкой и взять ржавый ключ:
```text
go east
look
take rusty_key
go west
```

Пройти в зал и решить загадку, чтобы получить ключ от сундука:
```text
go north
look
solve
```
(ответ: `7`)

Открыть проход в комнату сокровищ:
```text
go north
```
Если есть `rusty_key`, дверь откроется.

В комнате сокровищ:
```text
look
solve
```
Если у вас есть `treasure_key`, он используется и сундук открывается. Игра пишет, что вы победили и завершает цикл.

## Проверка стиля (ruff)

Для проверки стиля используется ruff.

Проверка всего проекта:
```bash
poetry run ruff check .
```
или через Makefile:
```bash
make lint
```
Нужно, чтобы проверка проходила без ошибок.

## Сборка и установка пакета

Сборка:
```bash
poetry build
```
или
```bash
make build
```

Пробная публикация (без отправки на реальный PyPI):
```bash
poetry publish --dry-run
```
или
```bash
make publish
```

Установка собранного пакета:
```bash
python3 -m pip install dist/*.whl
```
или
```bash
make package-install
```

После этого игру можно запускать просто командой:
```bash
project
```

## Структура проекта

Кратко, основные файлы:
- `labyrinth_game/main.py` — запуск игры и основной цикл
- `labyrinth_game/constants.py` — комнаты, команды и константы
- `labyrinth_game/utils.py` — описание комнат, загадки, случайные события
- `labyrinth_game/player_actions.py` — перемещение, инвентарь, использование предметов
- `pyproject.toml` — настройки poetry, скрипт project и ruff
- `Makefile` — короткие команды (install, project, lint, build и т.д.)
- `.gitignore` — игнор для .venv, dist, pycache и прочего мусора

## Запись консоли (asciinema)

https://asciinema.org/a/

## Автор

**ФИО:** Полей Евгений  
**Группа:** M25-555