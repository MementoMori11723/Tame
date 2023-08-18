import pygame 
import os
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tame")
BORDER = pygame.Rect(WIDTH//2,0,8,HEIGHT)
HEALTH_FONTS = pygame.font.SysFont('comicsans',40)
WINNER_FONTS = pygame.font.SysFont('comicsans',100)
RED,YELLOW,BLACK,WHITE,FPS,VELOCITY,SPACESHIP_SIZE,BULLET_VEL,MAX_BULLETS  = (255,0,0),(255,255,0),(0,0,255),(255,255,255),60,3,(55,40),7,5
YELLOW_HIT,RED_HIT = pygame.USEREVENT + 1, pygame.USEREVENT + 2
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_yellow.png')),SPACESHIP_SIZE), 90)

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_red.png')),SPACESHIP_SIZE),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

def drawGame(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    red_health_text = HEALTH_FONTS.render("Health: "+str(red_health),True,WHITE)
    yellow_health_text = HEALTH_FONTS.render("Health: "+str(yellow_health),True,WHITE)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()
def move_yellow(keys_pressed,yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #left
            yellow.x -= VELOCITY
        if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: #right
            yellow.x += VELOCITY
        if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #up
            yellow.y -= VELOCITY
        if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15: #down
            yellow.y += VELOCITY
def move_red(keys_pressed,red):
        if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: #left
            red.x -= VELOCITY
        if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH: #right
            red.x += VELOCITY
        if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: #up
            red.y -= VELOCITY
        if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15: #down
            red.y += VELOCITY
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONTS.render(text,True,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2,HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)
def main():
    red = pygame.Rect(700,300,SPACESHIP_SIZE[0],SPACESHIP_SIZE[1])
    yellow = pygame.Rect(100,300,SPACESHIP_SIZE[0],SPACESHIP_SIZE[1])
    red_bullets = [] 
    yellow_bullets = []
    red_health = 10 
    yellow_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2,10,5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2,10,5)
                    red_bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        winner_text = ""
        if red_health <= 0:   
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        move_yellow(keys_pressed,yellow)
        move_red(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        drawGame(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
    main()

if __name__ == "__main__":
    main()
