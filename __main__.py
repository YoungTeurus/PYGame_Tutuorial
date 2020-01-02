import pygame
pygame.init()

def main():
    # Инициализация PyGame и констант
    pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    FPS = 60

    game_playing = True  # Запущена ли игра

    while game_playing:

        clock.tick(FPS)  # Требуемый FPS и соответствующая задержка

        # Обработка событий:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_playing = False

        # Изменение объектов

        # 



if __name__ == "__main__":
    main()
