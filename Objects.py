import random
import pygame

# Настройки
from __main__ import window_w, window_h

ticks_before_change_frame = 5  # Сколько тиков должно пройти перед сменой кадра


# Класс камеры для отрисовки мира
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
        # dx, dy = 0, 0
        # if camera is not None:
        #    dx = camera.x
        #    dy = camera.y
        # pygame.draw.rect(self.surface, self.color,
        #                 (int(self.x - (self.w / 2) + dx),
        #                  int(self.y - (self.h / 2) + dy),
        #                  int(self.w),
        #                  int(self.h))
        #                 )
        pass

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        pass

    def __lt__(self, other):
        return self.y < other.y

    def tick(self):
        pass

    def __str__(self):
        return "(WorldObject,({x},{y}))".format(**{'x': self.x,
                                                   'y': self.y})


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

    # Пропуск кадров (для убыстрения анимации)
    def skip_frame(self, frames=None):
        frames_to_skip = 1
        if frames is not None:
            frames_to_skip = frames
        self.frame = (self.frame + frames_to_skip) % self.len_of_image_list
        self.image = self.image_list[self.frame]


# Класс текстового объекта
class TextObject(WorldObject):
    text = ""

    def __init__(self, surface, x, y, text=None):
        super().__init__(surface, x, y)
        self.font = pygame.font.Font(None, 25)
        if text is not None:
            self.text = text

    def draw(self, camera=None):
        # Создаём "картинку теста"
        text_img = self.font.render(self.text, True, self.color)
        # Накладываем её на поверхность
        self.surface.blit(text_img, [self.x, self.y])

    def set_text(self, text):
        self.text = text
