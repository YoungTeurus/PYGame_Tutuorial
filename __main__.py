import pygame
import random
import inspect
import os
import sys

# Размеры окошка
window_w = 600
window_h = 400

from Objects import Camera, SpritedObject, AnimatedObject, TextObject
from Player import Player


# Возвращает путь до папки скрипта
def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):  # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


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

    # Предзагрузка картинок
    directory_to_load = get_script_dir()
    enemy_1_animation = [
        pygame.image.load(directory_to_load + "\\sprites\\big_zombie_idle_anim_f0.png").convert_alpha(),
        pygame.image.load(directory_to_load + "\\sprites\\big_zombie_idle_anim_f1.png").convert_alpha(),
        pygame.image.load(directory_to_load + "\\sprites\\big_zombie_idle_anim_f2.png").convert_alpha(),
        pygame.image.load(directory_to_load + "\\sprites\\big_zombie_idle_anim_f3.png").convert_alpha(),
    ]
    player_animation = [
        pygame.image.load(directory_to_load + "\\sprites\\knight_f_idle_anim_f0.png").convert_alpha(),
        pygame.image.load(directory_to_load + "\\sprites\\knight_f_idle_anim_f1.png").convert_alpha(),
        pygame.image.load(directory_to_load + "\\sprites\\knight_f_idle_anim_f2.png").convert_alpha(),
        pygame.image.load(directory_to_load + "\\sprites\\knight_f_idle_anim_f3.png").convert_alpha(),
    ]
    floor_img = pygame.image.load(directory_to_load + "\\sprites\\floor.png").convert_alpha()

    # Объявление карты и массива объектов
    map_tiles = []  # Карта, представляющая собой "пол"
    objects = []  # Все объекты, отрисовываемые на карте

    game_playing = True  # Запущена ли игра
    object_placed = False  # Флаг для установки объекта

    # Игрок
    player = Player(window, window_w / 2, window_h / 2, Camera(), player_animation, (16, 28))
    objects.append(player)

    # Заполнение карты
    for i in range(50):
        for j in range(50):
            map_tiles.append(SpritedObject(window,
                                           i * 16, j * 16, floor_img, (16, 16)
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
                                              enemy_1_animation, (32, 34)
                                              )
                               )
                object_placed = True  # Запрещаем создавать новые объекты до отжатия ЛКМ
        else:
            object_placed = False

        is_move_button_pressed = False  # Была ли нажата клавиша двжиения
        # Обработка событий клавиатуры
        # Сперва обрабатываются конфликтующие случаи, если они наступают, нажатия на клавиши игнорируются
        if not(keyboard_pressed[pygame.K_a] and keyboard_pressed[pygame.K_d]):
            if keyboard_pressed[pygame.K_a]:
                player.player_move('left')
                is_move_button_pressed = True
            if keyboard_pressed[pygame.K_d]:
                player.player_move('right')
                is_move_button_pressed = True
        if not(keyboard_pressed[pygame.K_w] and keyboard_pressed[pygame.K_s]):
            if keyboard_pressed[pygame.K_w]:
                player.player_move('up')
                is_move_button_pressed = True
            if keyboard_pressed[pygame.K_s]:
                player.player_move('down')
                is_move_button_pressed = True
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

        # Изменение показаний дебаг-информации
        debug_text_player_position.set_text("Player position: ({},{})".format(
            player.x, player.y))
        debug_text_player_speed.set_text("Player speed: {}".format(
            player.current_speed))

        # Обновление экрана
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
