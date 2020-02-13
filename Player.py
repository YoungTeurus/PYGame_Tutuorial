from Objects import AnimatedObject
from __main__ import window_w, window_h

# Настройки
percent_of_running_animation = 0.5  # На сколько процентов от максимальной скорости
# должен двигаться игрок, чтобы ускорить анимацию


# Класс игрока, хранящий камеру
class Player(AnimatedObject):
    max_speed = 4
    current_speed = 0
    float_current_speed = 0
    float_acceleration = 0
    is_moving = False

    def __init__(self, surface, x, y, camera, image_list, size=None):
        super().__init__(surface, x, y, image_list, size)
        self.camera = camera

    def player_move(self, direction):
        if self.is_moving is not True:  # Если игрок только начал двигаться
            self.float_acceleration = 0.1  # Придаём начальное ускорение
        else:
            self.float_acceleration *= 1.005
        if self.float_acceleration > self.max_speed:  # Ограничиваем макс. скорость
            self.float_acceleration = self.max_speed
        self.is_moving = True

        # Собственно движение
        if direction == 'up':
            self.move(0, -self.current_speed)
            if self.y + self.camera.y < 10 + self.h:  # Расстояние до края окна - 10 пикселей
                self.camera.move(0, self.current_speed)
        if direction == 'down':
            self.move(0, self.current_speed)
            if self.y + self.camera.y > window_h - 10 - self.h:  # Расстояние до края окна - 10 пикселей
                self.camera.move(0, -self.current_speed)
        if direction == 'left':
            self.looking_left = True
            self.move(-self.current_speed, 0)
            if self.x + self.camera.x < 10 + self.w:  # Расстояние до края окна - 10 пикселей
                self.camera.move(self.current_speed, 0)
        if direction == 'right':
            self.looking_left = False
            self.move(self.current_speed, 0)
            if self.x + self.camera.x > window_w - 10 - self.w:  # Расстояние до края окна - 10 пикселей
                self.camera.move(-self.current_speed, 0)

    def tick(self):
        super().tick()
        if self.is_moving is not True:  # Торможение игрока
            self.float_acceleration = 0
            self.float_current_speed = 0
            self.current_speed = 0
            return

        self.float_current_speed += self.float_acceleration  # Добавляем к скорсти текущее ускорение
        if self.float_current_speed > self.max_speed:  # Ограничиваем макс. скорость
            self.float_current_speed = self.max_speed
        if self.float_current_speed < 0:
            self.float_current_speed = 0

        # Пропускаем кадры анимации, если скорость достаточно большая
        if self.float_current_speed > self.max_speed * percent_of_running_animation:
            self.skip_frame(1)

        self.current_speed = int(self.float_current_speed)

    def stop_moving(self):
        self.is_moving = False

