import pygame


def main():
    # Инициализация PyGame и констант
    pygame.init()
    source_surface = pygame.display.set_mode((600, 400))  # Основная поверхность
    pygame.display.set_caption("My game")
    clock = pygame.time.Clock()
    FPS = 30

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (125, 125, 125)
    LIGHT_BLUE = (64, 128, 255)
    GREEN = (0, 200, 64)
    YELLOW = (225, 225, 0)
    PINK = (230, 50, 230)
    RED = (255, 0, 0)
    # Конец цветов

    # Коды клавиш
    KEY_W = 119
    KEY_A = 97
    KEY_S = 115
    KEY_D = 100
    # Конец кодов клавиш
    '''
    pygame.draw.rect(source_surface, RED, (10, 10, 100, 100))  # Где, каким цветом и что рисуем

    rect_1 = pygame.Rect((150, 10, 250, 100))
    pygame.draw.rect(source_surface, WHITE, rect_1, 2)
    long_line = [[0, 0], [600, 400], [550, 50]]
    pygame.draw.polygon(source_surface, GREEN, long_line)
    pygame.draw.aalines(source_surface, GREEN, True, long_line)
    '''
    PI = 3.14
    angle = 0
    angle_in_radians = 0
    speed = 30
    max_speed = 180
    x = 50
    y = 50
    w = 100
    h = 100

    pressed_buttons = []

    game_playing = True  # Запущена ли игра

    while game_playing:

        clock.tick(FPS)  # Требуемый FPS и соответствующая задержка

        # Обработка событий:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_playing = False
            if event.type == pygame.KEYDOWN:
                pressed_buttons.append(event.key)
            if event.type == pygame.KEYUP:
                pressed_buttons.remove(event.key)

        if KEY_W in pressed_buttons:
            y -= 5
        if KEY_S in pressed_buttons:
            y += 5
        if KEY_A in pressed_buttons:
            if speed > -max_speed:
                speed -= 10
            x -= 5
        if KEY_D in pressed_buttons:
            if speed < max_speed:
                speed += 10
            x += 5

        # Изменение объектов
        source_surface.fill(BLACK)
        circle = (x, y, w, h)
        pygame.draw.ellipse(source_surface, YELLOW, circle)
        pygame.draw.arc(source_surface, GRAY, circle, 0 + angle_in_radians, PI + angle_in_radians, 5)
        pygame.draw.arc(source_surface, GRAY, circle, PI / 2 + angle_in_radians, PI + angle_in_radians, 10)

        angle += speed
        angle_in_radians = angle * PI / 180

        # Обновление экрана
        pygame.display.update()
        print(pressed_buttons)

    pygame.quit()


if __name__ == "__main__":
    main()
