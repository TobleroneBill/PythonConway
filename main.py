import random
import sys

import pygame

# Settings
WIDTH, HEIGHT = 800, 800
GRIDSIZE = 10  # in px
x = int(WIDTH / GRIDSIZE)  # needs to be an int to convert into a list
y = int(HEIGHT / GRIDSIZE)  # need x and y values incase grid is fucked (like size 23x723)
Running = False  # Gamestate - True = playing, False = Deciding
# Pygame stuff
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 6
CLOCK = pygame.time.Clock()
# Colors
Colors = ((96, 108, 56),  # Bright Muddy Green
          (40, 54, 24),  # Dark Muddy Green
          (254, 250, 224),  # Almost White
          (221, 161, 94),  # Mid Beige
          (188, 108, 37))  # Dark Beige
BorderSize = 1


# Inidiviual Cell
class Cell:
    def __init__(self, alive, coordinate):
        self.alive = alive
        self.coord = coordinate
        self.pos = coordinate[0] * GRIDSIZE, coordinate[1] * GRIDSIZE

    def PrtCoord(self):
        print(self.pos)

    def Draw(self):
        cellRect = pygame.Rect(self.pos, (GRIDSIZE, GRIDSIZE))
        # Draw with Corrosponding Color
        if self.alive:
            pygame.draw.rect(SCREEN, Colors[4], cellRect)
        else:
            pygame.draw.rect(SCREEN, Colors[1], cellRect)
        pygame.draw.rect(SCREEN, Colors[0], cellRect, BorderSize)


# To handle what Cell is alive
class CellChecker:

    def __init__(self, cellSizeX, cellSizeY):
        self.cellGrid = self.GenerateGrid(cellSizeX, cellSizeY)  # Creates Grid when generating
        self.cellList = self.PopualteGrid(self.cellGrid)  # Makes a seperate list for each cell

    def GenerateGrid(self, cellSizeX, cellSizeY):  # make a grid based on the cell sizes
        cellList = []
        for cell in range(0, cellSizeX + 1):  # X value
            x = cell
            for cell in range(0, cellSizeY + 1):  # Y value
                y = cell
                cellList.append((x, y))
        return cellList

    def PopualteGrid(self, grid):  # for each gridspace, Insert a Cell
        cells = []
        for item in grid:
            cells.append(Cell(False, item))
        return cells

    def PGrid(self):  # debug stuff
        print(self.cellList)

    def Randomize(self, upperLimit):
        for item in self.cellList:
            rng = random.randint(0, upperLimit)
            if rng != 0:
                item.alive = False
            else:
                item.alive = True

    def Draw(self):
        for item in self.cellList:  # Calls each cell's draw function
            item.Draw()

    def Running(self):
        for item in self.cellList:  # Check neighbours
            liveNeighbor = 0
            print('loop start')
            print(f'itempos = {item.pos}')
            minx = item.pos[0] - GRIDSIZE  # x+1,y+1
            if minx < 0:  # if at edges, just set the value to edge
                minx = 0
            maxx = item.pos[0] + GRIDSIZE  # x-1,y-1
            if maxx > WIDTH:
                maxx = WIDTH
            miny = item.pos[1] - GRIDSIZE
            if miny < 0:
                miny = 0
            maxy = item.pos[1] + GRIDSIZE
            if maxy > HEIGHT:
                maxy = HEIGHT
            neighborCoords = []
            # Range function doesn't include the number at its upper bound for some reason so have to add grid
            for i in range(minx, maxx + GRIDSIZE, GRIDSIZE):  # for min to max x values
                for j in range(miny, maxy + GRIDSIZE, GRIDSIZE):  # for min to max y values
                    index = (i, j)
                    if index != item.pos:
                        neighborCoords.append(index)

            for coords in neighborCoords:
                for cell in self.cellList:
                    if cell.pos == coords and cell.alive:
                        liveNeighbor += 1
            print(neighborCoords)
            print(f'Live neigbors: {liveNeighbor}')

            # If alive cell meets neigbors
            if liveNeighbor < 2 and item.alive:
                item.alive = False
            if liveNeighbor < 3 and item:
                item.alive = False

            # If dead cell meets neigbors
            if liveNeighbor > 3 and not item.alive:
                item.alive = True

            print('loop end')


# Handle General Stuff
grid = CellChecker(x, y)


# Checks for events, quitting and deciding
def EventCheck():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # If user presses space, it changes to running
            if event.key == pygame.K_SPACE:
                global Running
                Running = not Running
            if event.key == pygame.K_t:
                grid.Running()


# Update Screen
def update():
    SCREEN.fill(Colors[1])  # Bg
    EventCheck()  # Check User Quits + other events
    grid.Draw()  # Draw Grid
    pygame.display.update()  # Update Screen
    CLOCK.tick(FPS)


# Make the grid bigger or smaller
def SizeUpDown(positive):
    global GRIDSIZE, x, y
    if positive:
        GRIDSIZE += 10
    else:
        GRIDSIZE -= 10
    x = int(WIDTH / GRIDSIZE)  # needs to recalculate the grid
    y = int(HEIGHT / GRIDSIZE)
    grid.__init__(x, y)


# On player click - left = on, right = off. Checks between grid array and player choice coordinate
def DifferenceArray(leftClick):
    arr = []  # Makes a new array, to be populated with the difference between mouse pos, and each cell pos
    newx = pygame.mouse.get_pos()[0]  # Rounding to 10 for now, but will change when changable
    newy = pygame.mouse.get_pos()[1]  # grid size is implemented
    for item in grid.cellList:
        arr.append((abs(item.pos[0] - newx), abs(item.pos[1] - newy)))
    cellIndex = arr.index(min(arr))  # Get the index of the smallest value in the array of differenced shit
    if leftClick:
        grid.cellList[cellIndex].alive = True  # Chosen cell = alive
    else:
        grid.cellList[cellIndex].alive = False  # cell IS DEAD-DEAD-DEAD-D-D-D-DEADAROONI

    # print(cellIndex)

while True:
    if not Running:
        pygame.display.set_caption('Deciding')
        if pygame.mouse.get_pressed()[0]:
            DifferenceArray(True)
        if pygame.mouse.get_pressed()[2]:
            DifferenceArray(False)

        if pygame.key.get_pressed()[pygame.K_r]:
            grid.Randomize(3)

        '''
        if pygame.key.get_pressed()[pygame.K_a] and GRIDSIZE > 100:
            SizeUpDown(False)
        if pygame.key.get_pressed()[pygame.K_d] and GRIDSIZE < 1000:
            SizeUpDown(True)
        '''
    else:
        pygame.display.set_caption('Running')
        grid.Running()

    update()
    print(CLOCK.get_fps())
