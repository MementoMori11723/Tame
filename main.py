import pygame 
import os

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tame")

BORDER = pygame.Rect(WIDTH//2,0,8,HEIGHT)

BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 60
VELOCITY = 2
SPACESHIP_SIZE = (55,40)

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_yellow.png')),SPACESHIP_SIZE), 90)

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_red.png')),SPACESHIP_SIZE),270)

def drawGame(red,yellow):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN,BLACK,BORDER)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    pygame.display.update()
    
def move_yellow(keys_pressed,yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #left
            yellow.x -= VELOCITY
        if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: #right
            yellow.x += VELOCITY
        if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #up
            yellow.y -= VELOCITY
        if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT: #down
            yellow.y += VELOCITY

def move_red(keys_pressed,red):
        if keys_pressed[pygame.K_LEFT]: #left
            red.x -= VELOCITY
        if keys_pressed[pygame.K_RIGHT]: #right
            red.x += VELOCITY
        if keys_pressed[pygame.K_UP]: #up
            red.y -= VELOCITY
        if keys_pressed[pygame.K_DOWN]: #down
            red.y += VELOCITY

def main():

    red = pygame.Rect(700,300,SPACESHIP_SIZE[0],SPACESHIP_SIZE[1])
    yellow = pygame.Rect(100,300,SPACESHIP_SIZE[0],SPACESHIP_SIZE[1])

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        move_yellow(keys_pressed,yellow)
        move_red(keys_pressed,red)
        drawGame(red,yellow)
    pygame.quit()

if __name__ == "__main__":
    main()
