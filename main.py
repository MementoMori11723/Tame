import pygame 

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tame")

RED = (255,255,255)

Update = lambda: pygame.display.update()

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        WIN.fill(RED)
        Update()
    pygame.quit()

if __name__ == "__main__":
    main()
