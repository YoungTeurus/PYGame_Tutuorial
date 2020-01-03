import pygame
import random

random.seed()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 64)
RED = (255, 0, 0)


# Конец цветов


class WorldObject:
    w = 25
    h = 25

    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self):
        pygame.draw.rect(self.surface, self.color,
                         (int(self.x - (self.w / 2)),
                          int(self.y - (self.h / 2)),
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


def main():
    # Инициализация PyGame и констант
    pygame.init()
    window_w = 600
    window_h = 400
    window = pygame.display.set_mode((window_w, window_h))  # Основная поверхность
    pygame.display.set_caption("My game")
    clock = pygame.time.Clock()
    FPS = 30

    objects = []

    game_playing = True  # Запущена ли игра
    object_placed = False  # Флаг для установки объекта

    # Игрок
    Player = WorldObject(window, window_w / 2, window_h / 2)
    objects.append(Player)

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
                objects.append(WorldObject(window, mouse_pos[0], mouse_pos[1]))
                object_placed = True
        else:
            object_placed = False

        # Обработка событий клавиатуры
        if keyboard_pressed[pygame.K_a]:
            Player.move(-1, 0)
        if keyboard_pressed[pygame.K_d]:
            Player.move(1, 0)
        if keyboard_pressed[pygame.K_w]:
            Player.move(0, -1)
        if keyboard_pressed[pygame.K_s]:
            Player.move(0, 1)

        # Отрисовка объектов
        window.fill(BLACK)
        objects.sort()
        for obj in objects:
            obj.draw()

        # Такт игры
        for obj in objects:
            obj.tick()

        # Обновление экрана
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
