import pygame 
import os

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tame")

WHITE = (255,255,255)
FPS = 60

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))

Update = lambda: pygame.display.update()

def drawGame():
    WIN.fill(WHITE)
    WIN.blit(YELLOW_SPACESHIP_IMAGE,(200,75))
    Update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        drawGame()
    pygame.quit()

if __name__ == "__main__":
    main()
