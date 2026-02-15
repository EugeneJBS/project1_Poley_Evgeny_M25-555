"""
Действия игрока.
"""

from .constants import DIRECTIONS, ROOMS
from .utils import describe_current_room, random_event


def get_input(prompt: str = "> ") -> str:
    """Запрос ввода с обработкой прерываний."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state: dict) -> None:
    """Отображение инвентаря."""
    inventory = game_state['player_inventory']
    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("В вашем инвентаре:")
        for item in inventory:
            print(f" - {item}")


def move_player(game_state: dict, direction: str) -> None:
    """Перемещение игрока между комнатами."""
    direction = direction.lower()

    # Теперь DIRECTIONS используется для валидации ввода
    if direction not in DIRECTIONS:
        print("Я не знаю такого направления.")
        return

    room = ROOMS[game_state['current_room']]
    exits = room.get('exits', {})

    if direction not in exits:
        print("Там глухая стена. Нельзя пойти в этом направлении.")
        return

    target_room = exits[direction]

    # Проверка ключа для входа в сокровищницу
    if target_room == "treasure_room":
        if "rusty_key" not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

    # Обновление состояния
    game_state['current_room'] = target_room
    game_state['steps_taken'] += 1

    # Обработка событий после хода
    random_event(game_state)
    if not game_state['game_over']:
        describe_current_room(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    """Поднятие предмета."""
    room = ROOMS[game_state['current_room']]
    items = room.get('items', [])

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in items:
        items.remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    """Использование предметов из инвентаря."""
    inventory = game_state['player_inventory']
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    # Логика конкретных предметов
    if item_name == 'torch':
        print("Вы зажигаете факел. Становится светлее.")
    elif item_name == 'sword':
        print("Вы обнажаете меч. Вы чувствуете себя увереннее.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in inventory:
            print("Вы открыли шкатулку и нашли ржавый ключ!")
            inventory.append('rusty_key')
        else:
            print("Шкатулка пуста.")
    else:
        print("Вы не знаете, как это использовать.")