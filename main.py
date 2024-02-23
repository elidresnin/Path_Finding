import pygame
from queue import PriorityQueue

# constants that will be used to draw the grid.
WIDTH = 800
ROWS = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithms")

RED = (255, 0, 0)
GREEN = (0, 255, 0)  # checked
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)  # default
BLACK = (0, 0, 0)  # barriers
PURPLE = (128, 0, 128)  # path
ORANGE = (255, 165, 0)  # start
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)  # end


# A Spot is a location or box on the grid. Each spot will keep track of its color and neighboring Spots among other things.
class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neightbors = []

    def get_pos(self):
        return self.row, self.col

    def is_checked(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_path(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_checked(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self):
        pygame.draw.rect(WIN, self.color,
                         (self.row * (WIDTH // ROWS), self.col * (WIDTH // ROWS), WIDTH // ROWS, WIDTH // ROWS))

    def update_neighbors(self, grid):
        self.neighbors = []
        # down
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # right
        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # left
        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


# manhattan ditance - l distance - the quickest l - taxy cab distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# make a grid of spots
def make_grid():
    grid = []

    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            spot = Spot(i, j)
            grid[i].append(spot)

    return grid


def draw_grid():
    gap = WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, i * gap), (WIDTH, i * gap))
        pygame.draw.line(WIN, GREY, (i * gap, 0), (i * gap, WIDTH))


def draw(grid):
    WIN.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw()

    draw_grid()
    pygame.display.update()

def get_clicked_pos(pos):
    gap = WIDTH // ROWS
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main():
    # main loop
    grid = make_grid()
    draw(grid)
    start = None
    end = None

    run = True
    started = False

    while run:
        draw(grid)
        for event in pygame.event.get():  # loop through events from pygame

            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # left button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                spot = grid[row][col]

                if not start and spot != end:
                    spot.make_start()
                    start = spot

                elif not end and spot != start:
                    end = spot
                    spot.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
    pygame.quit()


main()
