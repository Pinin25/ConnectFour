from tkinter import *
import random

#Blue background #1F5FD5
#Yellow player #F4E332
#Red player #C0222A

YELLOW = "#F4E332"
RED = "#9E050E"
NAVY = "#3483F0"
WHITE = "white"
PLAYER_COLOR = RED

ROW = 7
COLUMN = 7
SIZE = 40

WIDTH = COLUMN * SIZE + 10
HEIGHT = ROW * SIZE + 10

MAX_TURNS = (ROW - 1) * COLUMN
NUMBER_TO_WIN = 4

class connectFour:
    def __init__(self):
        window = Tk()
        window.title("Connect Four")

        self.canvas = Canvas(window, width = WIDTH, height = HEIGHT,
                             bg = NAVY)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.processMouseEvent)

        self.displayText = ["Red is the best", "Sorry Red! Good luck next time",
                            "Not lucky huh, Yellow?", "Yellow is awesome"]
        self.winnerLabel = Label(window, text = "")
        self.winnerLabel.pack(side = LEFT)
        btReset = Button(window, text = "Reset", command = self.resetGame)
        btReset.pack(side = RIGHT, padx = 10)
        
        #Draw ROW x COLUMN empty space with unused first row to show selection
        self.grid = []
        for i in range(ROW):
            self.grid.append([])
            for j in range(COLUMN):
                self.grid[i].append(4 * [0])

        for i in range(ROW):
            for j in range(COLUMN):
                self.grid[i][j][0] = SIZE * j + 10
                self.grid[i][j][1] = SIZE * i + 10
                self.grid[i][j][2] = SIZE * j + SIZE
                self.grid[i][j][3] = SIZE * i + SIZE
        
        for j in range(COLUMN):
            self.canvas.create_oval(self.grid[0][j][0], self.grid[0][j][1],
                                    self.grid[0][j][2], self.grid[0][j][3],
                                    activefill = RED, tags = "thinking")
        for i in range(1, ROW):
            for j in range(COLUMN):
                self.canvas.create_oval(self.grid[i][j][0], self.grid[i][j][1],
                                        self.grid[i][j][2], self.grid[i][j][3],
                                        outline = "blue", fill = WHITE)
        
        #Initialize board with first row to store current occupied disc position
        #for each column
        self.space = []
        for i in range(ROW):
            self.space.append([])
            for j in range(COLUMN):
                self.space[i].append(0)

        self.resetGame()
        
        window.mainloop()

    def processMouseEvent(self, event):
        #Only activate when click on circles in first row
        if 10 < event.y < SIZE and event.x - (event.x // 40) * 40 > 10:
            column = event.x // 40

            if self.endGame == 0:
                if self.space[0][column] < ROW - 1:
                    self.space[0][column] += 1        #Occupy one space
                    row = ROW - self.space[0][column]
                    self.space[row][column] = 1 if self.player else 2
                    self.playerColor = RED if self.player else YELLOW
                    self.turns += 1

                    #Drop a disc with color matching player
                    self.canvas.create_oval(self.grid[row][column][0], self.grid[row][column][1],
                                            self.grid[row][column][2], self.grid[row][column][3],
                                            fill = self.playerColor, tags = "play")

                    self.endGame = self.getStatus(row, column)
                    
                    #Switch player
                    self.player = not self.player

                    #Redraw active space for selection
                    self.canvas.delete("thinking")
                    self.playerColor = RED if self.player else YELLOW
                    for j in range(COLUMN):
                        self.canvas.create_oval(self.grid[0][j][0], self.grid[0][j][1],
                                                self.grid[0][j][2], self.grid[0][j][3],
                                                activefill = self.playerColor, tags = "thinking")
            if self.endGame == 2:
                self.winnerLabel["text"] = "Draw"
            elif self.endGame == 1:
                #Randomly display result
                self.winnerLabel["text"] = self.displayText[random.randint(0, 1) * 2 + 1]\
                        if self.player else self.displayText[random.randint(0, 1) * 2]
 
    def resetGame(self):
        for i in range(ROW):
            for j in range(COLUMN):
                self.space[i][j] = 0
        self.canvas.delete("play")
        self.player = True
        self.turns = 0
        self.endGame = 0
        self.winnerLabel["text"] = ""

    def countMarks(self, r, c, dr, dc):
        marks = self.space[r][c]
        count = 0
        
        while True:
            if r < 1 or r > ROW - 1 or \
               c < 0 or c > COLUMN - 1 or \
               self.space[r][c] != marks:
                return count
            else:
                count += 1
                r += dr
                c += dc

    def getStatus(self, r, c):
        if self.turns <= MAX_TURNS:
            #Count vertical
            marks = self.countMarks(r, c, 1, 0)
            if marks > NUMBER_TO_WIN - 1:
                return 1

            #Count horizontal
            marks = self.countMarks(r, c, 0, -1) + self.countMarks(r, c, 0, 1)
            if marks > NUMBER_TO_WIN:
                return 1
            
            #Count diagonal /
            marks = self.countMarks(r, c, 1, -1) + self.countMarks(r, c, -1, 1)
            if marks > NUMBER_TO_WIN:
                return 1

            #Count diagonal \
            marks = self.countMarks(r, c, 1, 1) + self.countMarks(r, c, -1, -1)
            if marks > NUMBER_TO_WIN:
                return 1

        if self.turns == MAX_TURNS:
            return 2        #Draw
        
        return 0
        
connectFour()
