import pygame

#parameters
WIDTH = 540
HEIGHT = 540
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():

    global win

    pygame.init()
    win =  pygame.display.set_mode((WIDTH, HEIGHT))
    win.fill(WHITE)

    running = True 

    while running:
        
        draw_grids()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        

def draw_grids():
    blockSize = WIDTH/9
    for x in range(WIDTH):
        for y in range(HEIGHT):
            rect = pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pygame.draw.rect(win, BLACK, rect, 1)


main()