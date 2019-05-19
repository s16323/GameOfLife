import sys, pygame, random, time

# TODO add docstrings
# TODO add keybinds
# TODO add README


"""CONSTANTS"""
BOARD_SIZE = WIDTH, HEIGHT = 320*2, 240*2
CELL_SIZE = 10
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
custom_color = 150, 50, 150
ALIVE_COLOR = custom_color
DEAD_COLOR = black
FPS = 5
WALLS_PRESENT = 0       # 1 - walls present, 0 - no walls
SHAPE = 'circle'      # circle/rectangle


class LifeGame:

    def __init__(self):
        # TODO take these as constructor args:
        # BOARD_SIZE = WIDTH, HEIGHT = 320 * 2, 240 * 2
        # CELL_SIZE = 10
        # organism_color = 150, 250, 150
        # environment_color = 0, 0, 0
        # ALIVE_COLOR = organism_color
        # DEAD_COLOR = environment_color
        # FPS = 5
        # WALLS_PRESENT = 1  # 1 - walls present, 0 - no walls
        # SHAPE = 'circle'  # circle/rectangle


        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.clear_screen()
        pygame.display.flip()
        # self.last_update_completed = pygame.time.get_ticks()
        self.last_update_completed = 0      # time elapsed since pygame.init() - not actually '0' but close enough
        self.desired_milliseconds_between_updates = (1.0 / FPS) * 1000.0

        self.active_grid = 0

        self.num_cols = int(WIDTH / CELL_SIZE)
        self.num_rows = int(HEIGHT / CELL_SIZE)
        self.grids = []
        self.init_grids()
        self.set_grid()
        self.paused = False
        self.game_over = False

    def init_grids(self):

        print("Columns: %d\nRows: %d" % (self.num_cols, self.num_rows))       # debug - print out how many rows and columns

        def create_grid():
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows

        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def set_grid(self, value=None, grid=0):
        '''
        Examples:
        set_grid() or set_grid(None) - randomize grid
        set_grid(0) - zero out the grid - all dead
        set_grid(1) - fill the grid - all alive
        '''
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.choice([0, 1])
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def clear_screen(self):
        self.screen.fill(DEAD_COLOR)

    def draw_grid(self):
        self.clear_screen()
        # circle = pygame.draw.circle(self.screen, ALIVE_COLOR, (50, 50), 5, 0)    # circle(Surface, color, pos, radius, width=0)   -->   <class 'pygame.Rect'>
        # rect = pygame.draw.rect(self.screen, ALIVE_COLOR, [50, 50, 10, 10], 0)      # rect(Surface, color, Rect, width=0)   ->   <class 'pygame.Rect'>   (rect = [X_coord, y_coord, length, height])

        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.grids[self.active_grid][r][c] == 1:
                    color = ALIVE_COLOR
                else:
                    color = DEAD_COLOR
                if SHAPE == 'rectangle':
                    pygame.draw.rect(self.screen, color, [int(c * CELL_SIZE), int(r * CELL_SIZE), CELL_SIZE, CELL_SIZE], 0)
                elif SHAPE == 'circle':
                    pygame.draw.circle(self.screen, color, (int(c * CELL_SIZE + (CELL_SIZE / 2)), int(r * CELL_SIZE + (CELL_SIZE / 2))), int(CELL_SIZE / 2), 0)
        pygame.display.flip()

    def check_cell_neighbors(self, row_index, col_index):
        # get number of alive cells surrounding current cell:
        # self.grids[self.active_grid][r][c]  # current cell

        # check all 8 neighbors, add up alive count:
        def get_cell(r, c):
            try:
                cell_value = int(self.grids[self.active_grid][r][c]) # Check if a cell is alive, cells outsde of boundries are of type 'None' - they can't be cast to int
            except:
                cell_value = WALLS_PRESENT  # walls are solid or transparent WALLS_PRESENT = 0 or 1
            return cell_value

        num_alive_neighbors = 0
        num_alive_neighbors += get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += get_cell(row_index - 1, col_index)
        num_alive_neighbors += get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += get_cell(row_index, col_index - 1)
        num_alive_neighbors += get_cell(row_index, col_index + 1)
        num_alive_neighbors += get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += get_cell(row_index + 1, col_index)
        num_alive_neighbors += get_cell(row_index + 1, col_index + 1)

        # RULES:
        if self.grids[self.active_grid][row_index][col_index] == 1:     # living cell
            if num_alive_neighbors > 3:  # overpopulation - dies
                return 0
            if num_alive_neighbors < 2:  # underpopulation - dies
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:  # survives
                return 1

        elif self.grids[self.active_grid][row_index][col_index] == 0:     # dead cell
            if num_alive_neighbors == 3:  # comes to life
                return 1

        return self.grids[self.active_grid][row_index][col_index]


    def update_generation(self):
        '''
        inspect current active generation,
        prepare next generation
        '''
        self.set_grid(0, self.inactive_grid())      # clear inactive grid before updating to new state
        # inspect the current active generation:
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                next_gen_state = self.check_cell_neighbors(r, c)
                # set inactive grid future cell state:
                self.grids[self.inactive_grid()][r][c] = next_gen_state     # update cell to next state

        #swaping between grids:
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        return (self.active_grid + 1) % 2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # if key "s" is pressed toggle pause game
                if event.unicode == 's':
                    print("Toggling Pause")
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                # if key "r" is pressed randomise grid
                elif event.unicode == 'r':
                    print("Randomizing grid")
                    self.active_grid = 0                    # purge active grid
                    self.set_grid(None, self.active_grid)   # randomize active grid
                    self.set_grid(0, self.inactive_grid())  # set inactive grid to 0
                    self.draw_grid()                        # redraw new grid even if paused
                # if key "q" quit
                elif event.unicode == 'q':
                    print("Exiting.")
                    self.game_over = True
                # if key "k" kill all
                elif event.unicode == 'k':
                    print("Killing all")
                    self.set_grid(0, self.active_grid)          # set active grid to 0
                    self.set_grid(0, self.inactive_grid())      # set inactive grid to 0
                    self.draw_grid()                            # redraw empty grid even if paused

            # draw and remove creatures with L/R mouse
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                # when left mouse is down draw a creature
                while state == (1, 0, 0):
                    self.paused = True
                    print("mouse state: ", state)
                    print(event)
                    pos = pygame.mouse.get_pos()
                    # print("mouse position:  ", pos)
                    x = int(pos[0] / CELL_SIZE)
                    y = int(pos[1] / CELL_SIZE)
                    # print("coordinates: ", x, y)

                    self.grids[self.active_grid][y][x] = 1
                    self.draw_grid()
                    state = pygame.mouse.get_rel()

                # when right mouse is down remove a creature
                while state == (0, 0, 1):
                    self.paused = True
                    print("mouse state: ", state)
                    print(event)
                    pos = pygame.mouse.get_pos()
                    x = int(pos[0] / CELL_SIZE)
                    y = int(pos[1] / CELL_SIZE)
                    self.grids[self.active_grid][y][x] = 0
                    self.draw_grid()
                    state = pygame.mouse.get_rel()

            # print(event)

            if event.type == pygame.QUIT:
                sys.exit()

    def cap_framerate(self):

        # hard cap at a 60fps:
        # time.sleep(1 / 60)

        # if time since last frame < 1/60 s sleep for remaining time:
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update

        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now

    def run(self):
        print("Controlls: s - pause  r - randomize  k - kill all  q - quit")

        while True:
            if self.game_over:
                return
            self.handle_events()
            if self.paused:
                continue        # when paused just shortcut the loop, but keep handle_events() going
            self.update_generation()
            self.draw_grid()
            self.cap_framerate()



if __name__ == '__main__':          # in other words: if you run this file directly you run the game, if you import this file you don't run it (obviously)

    game = LifeGame()
    game.run()

