import sys, pygame

"""CONSTANTS"""
BOARD_SIZE = WIDTH, HEIGHT = 320*2, 240*2
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
ALIVE_COLOR = white
DEAD_COLOR = black



class LifeGame:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)

    def run(self):

        pygame.draw.rect(self.screen, ALIVE_COLOR, 4, width=0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            self.screen.fill(DEAD_COLOR)




            # screen.blit(ball, ballrect)       # draw to the screen
            pygame.display.flip()             # push into video memory



if __name__ == '__main__':          # in other words: if you run this file directly you run the game, if you import this file you don't run it (obviously)

    game = LifeGame()
    game.run()
