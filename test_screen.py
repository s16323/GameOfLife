import sys, pygame
pygame.init()

"""CONSTANTS"""
BOARD_SIZE = WIDTH, HEIGHT = 320*2, 240*2
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0

screen = pygame.display.set_mode(BOARD_SIZE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(red)
    pygame.display.flip()

