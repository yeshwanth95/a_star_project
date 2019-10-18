import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))


class Spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def Show(self, color, state):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), state)
            pygame.display.update()

    def Path(self, color, state):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), state)
        pygame.display.update()

    def addNeighbours(self, n_grid):
        i = self.i
        jj = self.j

        if i < cols - 1 and n_grid[self.i + 1][jj].obs == False:
            self.neighbours.append(n_grid[self.i + 1][jj])
        if i > 0 and n_grid[self.i - 1][jj].obs == False:
            self.neighbours.append(n_grid[self.i - 1][jj])
        if jj < rows - 1 and n_grid[self.i][jj + 1].obs == False:
            self.neighbours.append(n_grid[self.i][jj + 1])
        if jj > 0 and n_grid[self.i][jj - 1].obs == False:
            self.neighbours.append(n_grid[self.i][jj - 1])

        # Adding diagonals.
        if jj > 0 and i > 0 and n_grid[self.i - 1][jj - 1].obs == False:
            self.neighbours.append(n_grid[self.i - 1][jj - 1])
            idx = self.neighbours.index(n_grid[self.i - 1][jj - 1])
            self.neighbours[idx].value = math.sqrt(2)

        if jj - 1 > 0 and jj + 1 < rows and i < cols - 1 and n_grid[self.i - 1][jj + 1].obs == False:
            self.neighbours.append(n_grid[self.i - 1][jj + 1])
            idx = self.neighbours.index(n_grid[self.i - 1][jj + 1])
            self.neighbours[idx].value = math.sqrt(2)

        if jj - 1 < rows and i < cols - 1 and n_grid[self.i + 1][jj - 1].obs == False:
            self.neighbours.append(n_grid[self.i + 1][jj - 1])
            idx = self.neighbours.index(n_grid[self.i + 1][jj - 1])
            self.neighbours[idx].value = math.sqrt(2)

        if jj < rows - 1 and i < cols - 1 and n_grid[self.i + 1][jj + 1].obs == False:
            self.neighbours.append(n_grid[self.i + 1][jj + 1])
            idx = self.neighbours.index(n_grid[self.i + 1][jj + 1])
            self.neighbours[idx].value = math.sqrt(2)


cols = 60
grid = [0 for i in range(cols)]
rows = 60
openSet = []
closedSet = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
w = screen_width / cols
h = screen_height / rows
cameFrom = []

# Create a 2D array.
for i in range(cols):
    grid[i] = [0 for i in range(rows)]

# Create Spots.
for i in range(cols):
    for j in range(rows):
        grid[i][j] = Spot(i, j)

# Define start and end nodes.
start = grid[12][5]
end = grid[3][6]

# Show Rectangle.
for i in range(cols):
    for j in range(rows):
        grid[i][j].Show((255, 255, 255), 1)

for i in range(0, rows):
    grid[0][i].Show(grey, 0)
    grid[0][i].obs = True
    grid[cols - 1][i].obs = True
    grid[cols - 1][i].Show(grey, 0)
    grid[i][rows - 1].Show(grey, 0)
    grid[i][0].Show(grey, 0)
    grid[i][0].obs = True
    grid[i][rows - 1].obs = True


def onSubmit():
    global start
    global end
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()


window = Tk()
label = Label(window, text='Start(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y): ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show steps :', onvalue=1, offvalue=0, variable=var)

submit = Button(window, text='Submit', command=onSubmit)

showPath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()
openSet.append(start)


def mouseClick(x):
    t = x[0]
    ww = x[1]
    g1 = t // (screen_width // cols)
    g2 = ww // (screen_height // rows)
    access = grid[g1][g2]
    if access != start and access != end:
        if access.obs == False:
            access.obs = True
            access.Show((255, 255, 255), 0)


end.Show((255, 8, 127), 0)
start.Show((255, 8, 127), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for evt in ev:
        if evt.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mouseClick(pos)
            except AttributeError:
                pass

        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_SPACE:
                loop = False
                break

for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbours(grid)


def heuristic(n, e):
    d = math.sqrt((n.i - e.i) ** 2 + (n.j - e.j) ** 2)
    return d


def main():
    end.Show((255, 8, 127), 0)
    start.Show((255, 8, 127), 0)
    if len(openSet) > 0:
        lowest_index = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowest_index].f:
                lowest_index = i

        current = openSet[lowest_index]

        if current == end:
            print('done', current.f)
            start.Show((255, 8, 127), 0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.Show((0, 0, 255), 0)
                current = current.previous
            end.Show((255, 8, 127), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program finished. The shortest distance \n to '
                                                                 'the path is ' + str(temp) + ' blocks away, '
                                                                                              '\n do you want to '
                                                                                              'rerun the program?'))
            if result:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    evts = pygame.event.get()
                    for evnt in evts:
                        if evnt.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        openSet.pop(lowest_index)
        closedSet.append(current)

        neighbours = current.neighbours
        for i in range(len(neighbours)):
            neighbour = neighbours[i]
            if neighbour not in closedSet:
                temp_g = current.g + current.value
                if neighbour in openSet:
                    if neighbour.g > temp_g:
                        neighbour.g = temp_g
                else:
                    neighbour.g = temp_g
                    openSet.append(neighbour)

            neighbour.h = heuristic(neighbour, end)
            neighbour.f = neighbour.g + neighbour.h

            if neighbour.previous is None:
                neighbour.previous = current

    if var.get():
        for i in range(len(openSet)):
            openSet[i].Show(green, 0)

        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].Show(red, 0)

    current.closed = True


while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
