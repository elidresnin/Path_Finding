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
green_count = 255


# A Spot is a location or box on the grid. Each spot will keep track of its color and neighboring Spots among other things.
class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []
        self.parent = None
        self.visited = False
        self.h_score = float('inf')
        self.g_score = float('inf')

    def __lt__(self, other):
        if self.h_score + self.g_score == other.g_score + other.h_score:
            return self.h_score < other.h_score
        else:
            return self.h_score + self.g_score < other.h_score + other.g_score

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
        if not self.is_start() and not self.is_end() and not self.is_barrier():
            self.color = WHITE
            self.visited = False
            self.parent = None
        elif self.is_end():
            self.visited = False
            self.parent = None

    def make_checked(self):
        global green_count
        self.color = (0, green_count, 0)
        #green_count -= 1
        #green_count %= 255

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        if not self.is_start() and not self.is_end():
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
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


# manhattan distance - l distance - the quickest l - taxi cab distance
def h(p1, p2):
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)


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

def reconstruct_path(grid, end):
    end.make_path()
    draw(grid)
    if end.parent is not None:
        return 1 + reconstruct_path(grid, end.parent)
    else:
        return 0
def a_star(grid, start, end):
    # q = PriorityQueue()
    q = [start]
    start.h_score = h(start, end)
    start.g_score = 0
    visited_count = 2

    while q:
        visited_count += 1
        q.sort()
        node = q.pop(0)
        if not node.is_start() and not node.is_end():
            node.make_checked()

        if node is end:
            print("a star path = " + str(reconstruct_path(grid, node.parent)))
            print("a star visited " + str(visited_count) + " nodes.")
            return
        else:
            for n in node.neighbors:
                if n.g_score > node.g_score + 1:
                    n.parent = node
                    n.h_score = h(n, end)
                    n.g_score = node.g_score + 1
                    if n not in q:
                        q.append(n)

        draw(grid)


def greedy_search(grid, start, end):
    q = PriorityQueue()
    q.put(start)
    start.h_score = h(start, end)
    start.visited = True
    visited_count = 2
    while q:
        visited_count += 1
        node = q.get()
        if not node.is_start() and not node.is_end():
            node.make_checked()

        if node is end:
            print("greedy path = " + str(reconstruct_path(grid, node.parent)))
            print("greedy visited " + str(visited_count) + " nodes.")
            return
        else:
            for n in node.neighbors:
                if not n.visited:
                    n.parent = node
                    n.visited = True
                    n.h_score = h(n, end)
                    q.put(n)
        draw(grid)

def bfs_search(grid, start, end):
    q = PriorityQueue()
    q.put(start)
    start.h_score = 0
    start.visited = True
    count = 1
    visited_count = 2
    # keep looking at nodes until we've either run out of nodes or have reached the end.
    while q:
        visited_count += 1
        node = q.get()  # gets the first node from the queue
        if not node.is_start() and not node.is_end():
            node.make_checked()

        if node is end:
            print("bfs path = " + str(reconstruct_path(grid, node.parent)))
            print("bfs visited " + str(visited_count) + " nodes.")
            return
        else:
            for n in node.neighbors:
                if not n.visited:
                    n.parent = node
                    n.visited = True
                    n.h_score = count
                    q.put(n)
                    count += 1

        draw(grid)

def main():
    # main loop
    grid = make_grid()
    draw(grid)
    start = None
    end = None

    run = True
    started = False
    search_count = 0
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
                if event.key == pygame.K_SPACE and not started and search_count == 0:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bfs_search(grid, start, end)
                    search_count += 1
                elif event.key == pygame.K_SPACE and not started and search_count == 1:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    greedy_search(grid, start, end)
                    search_count += 1
                elif event.key == pygame.K_SPACE and not started and search_count == 2:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    a_star(grid, start, end)
                    search_count = 0

                elif event.key == pygame.K_r:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    draw(grid)

    pygame.quit()


main()
