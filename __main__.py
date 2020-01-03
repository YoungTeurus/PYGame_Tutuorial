import pygame
import random

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


# Класс камеры для отрисовки мира?
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


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


class SpritedObject(WorldObject, pygame.sprite.Sprite):
    w = None
    h = None
    need_to_scale = False

    def __init__(self, surface, x, y, image, size=None):
        WorldObject.__init__(self, surface, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x += self.x
        self.rect.y += self.y
        if size is not None:
            self.w = size[0]
            self.h = size[1]
            self.rect.x -= int(self.w/2)
            self.rect.y -= int(self.h/2)
            self.need_to_scale = True

    def draw(self, camera=None):
        scaled_surface = None
        if self.need_to_scale:
            scaled_surface = pygame.transform.scale(self.image, (self.w, self.h))
        dx, dy = 0, 0
        if camera is not None:
            rect_to_draw = pygame.Rect.copy(self.rect)
            rect_to_draw.x += camera.x
            rect_to_draw.y += camera.y
            if self.need_to_scale:
                self.surface.blit(scaled_surface, rect_to_draw)
                return
            self.surface.blit(self.image, rect_to_draw)
            return
        if self.need_to_scale:
            self.surface.blit(scaled_surface, self.rect)
            return
        self.surface.blit(self.image, self.rect)


# Класс игрока, хранящий камеру
class Player(WorldObject):
    speed = 5

    def __init__(self, surface, x, y, camera):
        super().__init__(surface, x, y)
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
            self.move(-self.speed, 0)
            if self.x + self.camera.x < 10 + self.w:  # Расстояние до края окна - 10 пикселей
                self.camera.move(self.speed, 0)
        if direction == 'right':
            self.move(self.speed, 0)
            if self.x + self.camera.x > window_w - 10 - self.w:  # Расстояние до края окна - 10 пикселей
                self.camera.move(-self.speed, 0)


def main():
    # Инициализация PyGame и констант
    pygame.init()

    window = pygame.display.set_mode((window_w, window_h))  # Основная поверхность
    pygame.display.set_caption("My game")
    clock = pygame.time.Clock()
    FPS = 30

    # Предзагрузка картинок
    img_1 = pygame.image.load("C:\\Users\\s_aza\\PycharmProjects\\PYGame_Tutuorial\\test.png").convert_alpha()

    objects = []

    game_playing = True  # Запущена ли игра
    object_placed = False  # Флаг для установки объекта

    # Игрок
    player = Player(window, window_w / 2, window_h / 2, Camera())
    objects.append(player)

    while game_playing:

        clock.tick(FPS)  # Требуемый FPS и соответствующая задержка

        # Обработка событий:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_playing = False
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        keyboard_pressed = pygame.key.get_pressed()

        if mouse_pressed[0]:
            if not object_placed:
                # objects.append(WorldObject(window, mouse_pos[0] - player.camera.x, mouse_pos[1] - player.camera.y))
                objects.append(SpritedObject(window,
                                             mouse_pos[0] - player.camera.x,
                                             mouse_pos[1] - player.camera.y,
                                             img_1, (32, 32)
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

        # Отрисовка объектов
        window.fill(BLACK)
        objects.sort()
        for obj in objects:
            obj.draw(player.camera)

        # Такт игры
        for obj in objects:
            obj.tick()

        # Обновление экрана
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
