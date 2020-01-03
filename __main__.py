import pygame
import random
import inspect
import os
import sys


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
# Размеры окошка
window_w = 600
window_h = 400
FPS = 30
ticks_before_change_frame = 5  # Сколько тиков должно пройти перед сменой кадра


# Класс камеры для отрисовки мира?
class Camera:
    x = 0
    y = 0
    w = window_w
    h = window_h
    visible_rect = pygame.Rect(x - 100, y - 100, w + 200, h + 200)

    def __init__(self):
        pass

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.visible_rect.x, self.visible_rect.y = -self.x, -self.y


# Класс объекта игрового мира, содержит методы draw и tick
class WorldObject:
    w = 25
    h = 25

    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, camera=None):
        dx, dy = 0, 0
        if camera is not None:
            dx = camera.x
            dy = camera.y
        pygame.draw.rect(self.surface, self.color,
                         (int(self.x - (self.w / 2) + dx),
                          int(self.y - (self.h / 2) + dy),
                          int(self.w),
                          int(self.h))
                         )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def __lt__(self, other):
        return self.y < other.y

    def tick(self):
        pass


# Класс объекта с текстурами
class SpritedObject(WorldObject, pygame.sprite.Sprite):
    w = None
    h = None
    need_to_scale = False
    looking_left = False

    def __init__(self, surface, x, y, image, size=None):
        WorldObject.__init__(self, surface, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x += int(self.x)
        self.rect.y += int(self.y)
        if size is not None:
            self.w = size[0]
            self.h = size[1]
            self.rect.x -= int(self.w / 2)
            self.rect.y -= int(self.h / 2)
            self.need_to_scale = True

    def draw(self, camera=None):
        # surface_to_draw = None
        # rect_to_draw = None

        need_to_draw = False
        if camera is not None:
            rect_to_draw = pygame.Rect.copy(self.rect)
            rect_to_draw.x += camera.x
            rect_to_draw.y += camera.y
        else:
            rect_to_draw = self.rect

        if self.rect.colliderect(camera.visible_rect):
            need_to_draw = True

        if need_to_draw:
            if self.need_to_scale:
                surface_to_draw = pygame.transform.scale(self.image, (self.w, self.h))
            else:
                surface_to_draw = self.image

            if self.looking_left:
                surface_to_draw = pygame.transform.flip(surface_to_draw, True, False)

            self.surface.blit(surface_to_draw, rect_to_draw)
            return True
        return False


# Класс объекта с анимацией
class AnimatedObject(SpritedObject):
    frame = 0
    timer = 0

    def __init__(self, surface, x, y, image_list, size=None):
        SpritedObject.__init__(self, surface, x, y, image_list[0], size)
        self.image_list = image_list
        self.len_of_image_list = len(self.image_list)

    def move(self, dx, dy):
        super().move(dx, dy)
        self.rect.x = int(self.x - (self.w / 2))
        self.rect.y = int(self.y - (self.h / 2))

    def tick(self):
        self.timer += 1
        if self.timer > ticks_before_change_frame:
            self.timer = 0
            self.frame = (self.frame + 1) % self.len_of_image_list
            self.image = self.image_list[self.frame]


# Класс игрока, хранящий камеру
class Player(AnimatedObject):
    speed = 5

    def __init__(self, surface, x, y, camera, image_list, size=None):
        super().__init__(surface, x, y, image_list, size)
        self.camera = camera

    def player_move(self, direction):
        if direction == 'up':
            self.move(0, -self.speed)
            if self.y + self.camera.y < 10 + self.h:  # Расстояние до края окна - 10 пикселей
                self.camera.move(0, self.speed)
        if direction == 'down':
            self.move(0, self.speed)
            if self.y + self.camera.y > window_h - 10 - self.h:  # Расстояние до края окна - 10 пикселей
                self.camera.move(0, -self.speed)
        if direction == 'left':
            self.looking_left = True
            self.move(-self.speed, 0)
            if self.x + self.camera.x < 10 + self.w:  # Расстояние до края окна - 10 пикселей
                self.camera.move(self.speed, 0)
        if direction == 'right':
            self.looking_left = False
            self.move(self.speed, 0)
            if self.x + self.camera.x > window_w - 10 - self.w:  # Расстояние до края окна - 10 пикселей
                self.camera.move(-self.speed, 0)


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
    floor_img = pygame.image.load(directory_to_load + "\\floor.png").convert_alpha()

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

        # Обработка событий клавиатуры
        if keyboard_pressed[pygame.K_a]:
            player.player_move('left')
        if keyboard_pressed[pygame.K_d]:
            player.player_move('right')
        if keyboard_pressed[pygame.K_w]:
            player.player_move('up')
        if keyboard_pressed[pygame.K_s]:
            player.player_move('down')

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

        # Обновление экрана
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
