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
    speed = 33.3
    circle = (50, 50, 150, 150)

    game_playing = True  # Запущена ли игра

    while game_playing:

        clock.tick(FPS)  # Требуемый FPS и соответствующая задержка

        # Обработка событий:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_playing = False

        # Изменение объектов
        source_surface.fill(BLACK)
        pygame.draw.ellipse(source_surface, YELLOW, circle)
        pygame.draw.arc(source_surface, GRAY, circle, 0 + angle_in_radians, PI + angle_in_radians, 5)
        pygame.draw.arc(source_surface, GRAY, circle, PI / 2 + angle_in_radians, PI + angle_in_radians, 10)

        angle += speed
        angle_in_radians = angle * PI / 180

        # Обновление экрана
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
