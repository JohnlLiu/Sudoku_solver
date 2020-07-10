import pygame
from main import solve, is_valid, is_empty
pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]


    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1): #draw thicker lines every third row and column
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def solve_gui(self):
        find = is_empty(self.model) #finds position of empty grids
        if not find:
            return True #board is solved
        else:
            row, col = find #assign grid index

        for i in range(1, 10):
            if is_valid(self.model, i, (row, col)): #check for valid number at grid
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0 #set grid value back to 0 for backtrack
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap


        if not(self.value == 0): # draw in values to grids if not supposed to be empty
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2))) #centers number

    
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if g: #highlight correct values with green
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else: #highlight incorrect values with red
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


class button():
    def __init__(self, colour, x, y, width, height, text=''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text 

    def draw(self, win, outline = None):
        if outline: #creates an outline around button
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4),0)
        
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            fnt = pygame.font.SysFont("comicsans", 40)
            text = fnt.render(self.text, 1, (0,0,0)) #renders text
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))) #centers text

    def hover(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

            return False

def redraw_window(win, board, solve_button):
    win.fill((255,255,255))
    solve_button.draw(win, (0,0,0))
    board.draw(win)


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    solve_button = button((177,224,217), 230, 550, 80, 40, 'Solve')
    key = None
    run = True

    while run:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                run = False


            #for button interaction
            pos = pygame.mouse.get_pos()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if solve_button.hover(pos):
                    board.solve_gui()
            
            if ev.type == pygame.MOUSEMOTION:
                    if solve_button.hover(pos):
                        solve_button.colour = (52, 89, 168)
                    else:
                        solve_button.colour = (177, 224, 217)

        redraw_window(win, board, solve_button)
        pygame.display.update()


main()
pygame.quit()