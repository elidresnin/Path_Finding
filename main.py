import pygame
from queue import PriorityQueue, Queue
import sys
sys.setrecursionlimit(10**6)

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
            return self.g_score < other.g_score
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

def default_board(grid, start, end, started):
    spot = grid[20][20]
    spot.make_start()
    start = spot

    spot = grid[40][40]
    spot.make_end()
    end = spot

    barriers = [(16,30), (17,30), (18,30), (19,30), (20,30), (21,30), (22,30), (23,30), (24,30), (24,29), (25,29), (25,28), \
                (26,28), (26,27), (27,27), (27,26), (28,26), (29,26), (29,25), (29,24), (30,24), (31,23), (32,23), (32,22), \
                (33,22), (34,22), (35,22), (35,23), (36,23), (37,23), (38,23), (39,23), (41,29), (40,29), (40,30), (39,30), \
                (38,30), (38,31), (37,31), (36,31), (36,32), (35,32), (34,33), (33,34), (32,35), (31,35), (31,36), (30,36), \
                (30,37), (30,38), (29,38), (39,34), (40,34), (41,34), (42,34), (43,34), (44,34), (44,33), (45,33), (45,32), \
                (46,32), (46,31), (46,30), (47,30), (47,29), (47,28), (27,34), (26,34), (26,35), (26,36), (25,36), (25,37), \
                (25,38), (24,38), (24,39), (24,40), (23,40), (23,41), (23,42), (23,43), (23,44), (23,45), (24,45), (24,46), \
                (25,46), (26,46), (27,46), (28,46), (42,35), (42,36), (42,37), (42,38), (42,39), (43,39), (43,40), (44,40), \
                (45,40), (45,41), (46,41), (46,42), (47,42), (47,43), (47,44), (47,45), (46,45), (46,18), (46,19), (46,20), \
                (46,21), (46,22), (46,23), (45,23), (45,24), (44,24), (43,24), (42,24), (42,25), (41,25), (48,44), (49,44), \
                (20,31), (20,32), (20,33), (20,34), (20,35), (20,36), (20,37), (20,38), (20,39), (20,42), (20,43), (20,44), \
                (20,45), (20,46), (20,47), (21,47), (22,47), (22,48), (23,48), (23,49), (28,42), (29,42), (30,42), (31,42), \
                (32,42), (33,42), (34,42), (34,41), (35,41), (35,40), (35,39), (35,38)]

    for v in barriers:
        grid[v[0]][v[1]].make_barrier()

    started = True
    return (start, end)

def a_star(grid, start, end):
    q = PriorityQueue()
    start.g_score = 0
    start.h_score = h(start, end)
    q.put(start)  # sets start spot
    start.visited = True
    visited_count = 1  # will be used to determine how many spots are algorith visits before finding the end node.

    # keep looking at spots until we've either run out of spots to look at or we've reached the end.
    while q:  # shorthand way of saying if there's anything still in priority queue.
        visited_count += 1
        current_spot = q.get()  # Dequeue the node based on priority -> fscore
        if not current_spot.is_start() and not current_spot.is_end():
            current_spot.make_checked()  # changes color to green

        if current_spot.is_end():
            print("a star path = " + str(reconstruct_path(grid, current_spot.parent)))  # reconstruct path
            print("star visited " + str(visited_count))
            return

        else:
            for s in current_spot.neighbors:  # put neighbor in priority queue.
                if not s.visited:
                    s.parent = current_spot  # setting s's parent to the sport that we just visited. Will be used when we reconstruct the path.
                    s.g_score = current_spot.g_score + 1
                    s.h_score = h(s, end)
                    s.visited = True  # set visited to true so we don't revisit later.
                    q.put(s)  # add s to the priority queue

        draw(grid)  # update grid any time we're done looking at a node.


def greedy_search(grid, start, end):
    q = PriorityQueue()
    start.g_score = 0
    start.h_score = h(start, end)
    q.put(start)  # sets start spot
    start.visited = True
    visited_count = 1  # will be used to determine how many spots are algorith visits before finding the end node.

    # keep looking at spots until we've either run out of spots to look at or we've reached the end.
    while q:  # shorthand way of saying if there's anything still in priority queue.
        visited_count += 1
        current_spot = q.get()  # Dequeue the node based on priority -> fscore
        if not current_spot.is_start() and not current_spot.is_end():
            current_spot.make_checked()  # changes color to green

        if current_spot.is_end():
            print("a star path = " + str(reconstruct_path(grid, current_spot.parent)))  # reconstruct path
            print("star visited " + str(visited_count))
            return

        else:
            for s in current_spot.neighbors:  # put neighbor in priority queue.
                if not s.visited:
                    s.parent = current_spot  # setting s's parent to the sport that we just visited. Will be used when we reconstruct the path.
      #              s.g_score = current_spot.g_score + 1
                    s.h_score = h(s, end)
                    s.visited = True  # set visited to true so we don't revisit later.
                    q.put(s)  # add s to the priority queue

        draw(grid)  # update grid any time we're done looking at a node.


def bfs_search(grid, start, end):
    q = Queue()
    q.put(start) # sets start spot
    start.visited = True
    visited_count = 1 # will be used to determine how many spots are algorith visits before finding the end node.

    # keep looking at spots until we've either run out of spots to look at or we've reached the end.
    while q: # shorthand way of saying if there's anything still in priority queue.
        visited_count += 1
        current_spot = q.get() # gets the first spot from the queue based on priority.
        if not current_spot.is_start() and not current_spot.is_end():
            current_spot.make_checked() # changes color to green

        if current_spot.is_end():
            print("bfs path = " + str(reconstruct_path(grid, current_spot.parent))) #reconstruct path
            print("bfs visited " + str(visited_count))
            return

        else:
            for s in current_spot.neighbors: # put neighbor in priority queue.
                if not s.visited:
                    s.parent = current_spot   # setting s's parent to the sport that we just visited. Will be used when we reconstruct the path.
                    s.visited = True    # set visited to true so we don't revisit later.
                    q.put(s)        # add s to the priority queue

        draw(grid) # update grid any time we're done looking at a node.



def dfs_search(grid, start, end):
    stack = []
    stack.append(start)     # sets start spot
    start.visited = True
    visited_count = 1   # will be used to determine how many spots are algorith visits before finding the end node.

    # keep looking at spots until we've either run out of spots to look at or we've reached the end.
    while stack: # shorthand way of saying if there's anything still in priority queue.
        visited_count += 1
        current_spot = stack.pop()  # first in last out. pops the last spot from the stack

        if not current_spot.is_start() and not current_spot.is_end():
            current_spot.make_checked() # changes color to green

        if current_spot.is_end():
            print("dfs path = " + str(reconstruct_path(grid, current_spot.parent))) # reconstruct path
            print("dfs visited " + str(visited_count))
            return

        else:
            for s in current_spot.neighbors: # put neighbor in priority queue.
                if not s.visited:
                    s.parent = current_spot   # setting s's parent to the sport that we just visited. Will be used when we reconstruct the path.
                    s.visited = True    # set visited to true so we don't revisit later.
                    stack.append(s)        # add s to the stack

        draw(grid) # up



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
                if event.key == pygame.K_d:
                    start, end = default_board(grid, start, end, started)
                if event.key == pygame.K_SPACE and not started and search_count == 0:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bfs_search(grid, start, end)
                    search_count += 1
                elif event.key == pygame.K_SPACE and not started and search_count == 1:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    dfs_search(grid, start, end)
                    search_count += 1
                elif event.key == pygame.K_SPACE and not started and search_count == 2:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    a_star(grid, start, end)
                    search_count = 0

                elif event.key == pygame.K_r:
                    for row in grid:
                        for spot in row:
                            spot.reset()
                    draw(grid)

    pygame.quit()


main()
