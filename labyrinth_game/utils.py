"""
Вспомогательные функции.
"""

import math
from .constants import (
    COMMANDS, ROOMS, EVENT_PROBABILITY_MODULO,
    RANDOM_EVENT_TYPES, TRAP_DANGER_MODULO, TRAP_DEATH_THRESHOLD
)


def describe_current_room(game_state: dict) -> None:
    """Вывод описания текущей комнаты."""
    room_id = game_state['current_room']
    room = ROOMS[room_id]

    print(f"\n== {room_id.upper()} ==")
    print(room['description'])

    items = room.get('items', [])
    if items:
        print("Заметные предметы:", ", ".join(items))

    exits = room.get('exits', {})
    print("Выходы:", ", ".join(exits.keys()))

    if room.get('puzzle'):
        print("Кажется, здесь есть загадка (используйте команду solve).")


def show_help(commands: dict = COMMANDS) -> None:
    """Вывод справки по командам (help)."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")


def pseudo_random(seed: int, modulo: int) -> int:
    """Генератор псевдослучайных чисел на основе синуса."""
    if modulo <= 0:
        return 0
    # Математическая формула для разброса значений
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state: dict) -> None:
    """Последствия активации ловушки."""
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']

    if inventory:
        # Потеря случайного предмета
        idx = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы уронили и потеряли: {lost_item}")
    else:
        # Риск гибели при пустом инвентаре
        roll = pseudo_random(game_state['steps_taken'], TRAP_DANGER_MODULO)
        if roll < TRAP_DEATH_THRESHOLD:
            print("Вы попали в глубокую яму. Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вы успели отскочить в сторону. Вы уцелели.")


def random_event(game_state: dict) -> None:
    """Случайные события при перемещении."""
    seed = game_state['steps_taken']
    if pseudo_random(seed, EVENT_PROBABILITY_MODULO) != 0:
        return

    event_id = pseudo_random(seed + 1, RANDOM_EVENT_TYPES)
    room = ROOMS[game_state['current_room']]

    if event_id == 0:
        print("\nВы нашли на полу монетку!")
        room.setdefault('items', []).append('coin')
    elif event_id == 1:
        print("\nВы слышите странный шорох...")
        if 'sword' in game_state['player_inventory']:
            print("Вы крепче сжали меч, и шорох прекратился.")
    elif event_id == 2:
        # Проверка условий ловушки
        if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
            print("\nВ темноте вы не заметили нажимную плиту!")
            trigger_trap(game_state)


def solve_puzzle(game_state: dict) -> None:
    """Решение загадок в комнатах."""
    room_name = game_state['current_room']
    room = ROOMS[room_name]
    puzzle = room.get('puzzle')

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, answer = puzzle
    print(f"\n{question}")
    user_input = input("Ваш ответ: ").strip().lower()

    # Проверка ответа с учетом альтернатив
    is_correct = (user_input == answer) or \
                 (answer == "10" and user_input == "десять")

    if is_correct:
        print("Верно! Вы разгадали загадку.")
        room['puzzle'] = None
        # Награды в зависимости от комнаты
        if room_name == 'hall':
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили награду: treasure_key")
        elif room_name == 'library':
            print("Вы получили награду: древнее знание")
        elif room_name == 'cellar':
            print("Вы получили награду: монетка")
            game_state['player_inventory'].append('coin')
    else:
        print("Неверно. Попробуйте снова.")
        if room_name == 'trap_room':
            trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    """Логика победы в сокровищнице."""
    inventory = game_state['player_inventory']
    room = ROOMS['treasure_room']

    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        print("В сундуке сокровище! Вы победили!")
        room.get('items', []).remove('treasure_chest')
        game_state['game_over'] = True
        return

    print("Сундук заперт. Его можно открыть ключом или попробовать ввести код.")
    if input("Ввести код? (да/нет): ").strip().lower() == "да":
        ans = input("Введите код: ").strip()
        if ans == room['puzzle'][1]:
            print("Код верный! Сундук открыт.")
            print("В сундуке сокровище! Вы победили!")
            room.get('items', []).remove('treasure_chest')
            game_state['game_over'] = True
        else:
            print("Код неверный.")
    else:
        print("Вы отступаете от сундука.")