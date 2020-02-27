import pygame
import random

# Размеры окошка
window_w = 600
window_h = 400

# Уникальные ID(?)
PLAYER1_ID = 0

from Objects import Camera, SpritedObject, AnimatedObject, TextObject, parse_object_str, MovingObject
from Player import Player

random.seed()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 64)
RED = (255, 0, 0)
# Конец цветов

FPS = 30


def main():
    # Инициализация PyGame и констант
    pygame.init()

    window = pygame.display.set_mode((window_w, window_h))  # Основная поверхность
    pygame.display.set_caption("My game")
    clock = pygame.time.Clock()

    # Объявление карты и массива объектов
    map_tiles = []  # Карта, представляющая собой "пол"
    objects = []  # Все объекты, отрисовываемые на карте

    game_playing = True  # Запущена ли игра
    object_placed = False  # Флаг для установки объекта

    # Игрок
    player = Player(window, window_w / 2, window_h / 2, Camera(), "\\sprites\\knight_f_idle_anim\\", (16, 28))
    player.set_id(PLAYER1_ID)
    objects.append(player)

    timeout_before_shooting = 100  # Время до стрельбы
    current_timeout_before_shooting = 0  # Текущее время до стрельбы

    # Заполнение карты
    for i in range(50):
        for j in range(50):
            map_tiles.append(SpritedObject(window,
                                           i * 16, j * 16, "\\sprites\\floor.png", (16, 16)
                                           )
                             )
    # Добавление текстовых объектов
    debug_text_player_position = TextObject(window, 0, 0, "Player position: ({},{})".format(
        player.x, player.y))
    debug_text_player_speed = TextObject(window, 0, 25, "Player speed: {}".format(
        player.current_speed))
    objects.append(debug_text_player_position)
    objects.append(debug_text_player_speed)

    while game_playing:

        clock.tick(FPS)  # Требуемый FPS и соответствующая задержка
        window.fill(BLACK)

        # Обработка событий:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_playing = False
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        keyboard_pressed = pygame.key.get_pressed()

        if mouse_pressed[0]:
            if not object_placed:
                objects.append(AnimatedObject(window,
                                              mouse_pos[0] - player.camera.x,
                                              mouse_pos[1] - player.camera.y,
                                              "\\sprites\\big_zombie_idle_anim\\", (32, 34)
                                              )
                               )
                object_placed = True  # Запрещаем создавать новые объекты до отжатия ЛКМ
        else:
            object_placed = False

        is_move_button_pressed = False  # Была ли нажата клавиша двжиения
        # Обработка событий клавиатуры
        # Сперва обрабатываются конфликтующие случаи, если они наступают, нажатия на клавиши игнорируются
        if not (keyboard_pressed[pygame.K_a] and keyboard_pressed[pygame.K_d]):
            if keyboard_pressed[pygame.K_a]:
                player.player_move('left')
                is_move_button_pressed = True
            if keyboard_pressed[pygame.K_d]:
                player.player_move('right')
                is_move_button_pressed = True
        if not (keyboard_pressed[pygame.K_w] and keyboard_pressed[pygame.K_s]):
            if keyboard_pressed[pygame.K_w]:
                player.player_move('up')
                is_move_button_pressed = True
            if keyboard_pressed[pygame.K_s]:
                player.player_move('down')
                is_move_button_pressed = True
        # Стрельба
        if keyboard_pressed[pygame.K_SPACE]:
            if current_timeout_before_shooting == 0:
                bul = MovingObject(window, player.x, player.y, "\\sprites\\bullet.png")
                objects.append(bul)
                if player.looking_left:
                    bul.set_speed(-5, 0)
                else:
                    bul.set_speed(5, 0)
                current_timeout_before_shooting = timeout_before_shooting

        # Отладка парсера
        # if keyboard_pressed[pygame.K_p]:
        #    for obj in objects:
        #        print(obj)
        #    str = input()
        #    objects.append(parse_object_str(window, str))
        if is_move_button_pressed is not True:  # Если отпущены все клавиши движения
            player.stop_moving()  # Прекращаем двигаться

        # Отрисовка карты
        num_of_drawn_objects = 0  # Количество отрисованных объектов
        for tile in map_tiles:
            if tile.draw(player.camera):
                num_of_drawn_objects += 1
        # Отрисовка объектов
        objects.sort()
        for obj in objects:
            if obj.draw(player.camera):  # Если объект был отрисован
                num_of_drawn_objects += 1
        # print(num_of_drawn_objects)

        # Такт игры
        for obj in objects:
            obj.tick()
        if current_timeout_before_shooting > 0:
            current_timeout_before_shooting -= 1

        # Изменение показаний дебаг-информации
        debug_text_player_position.set_text("Player position: ({},{})".format(
            player.x, player.y))
        debug_text_player_speed.set_text("Player speed: {}".format(
            player.current_speed))

        # Обновление экрана
        pygame.display.update()

    #for obj in objects:
    #    # print(obj)
    #    new_obj = parse_object_str(window, str(obj))
    #    print(new_obj)
    pygame.quit()


if __name__ == "__main__":
    main()
