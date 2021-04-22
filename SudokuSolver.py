import pygame
import pygbutton
from random import sample, randint

class Grid:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("lato", 40)
        self.rows = [g * 3 + r for g in self.shuffle(range(3)) for r in self.shuffle(range(3))]
        self.cols = [g * 3 + c for g in self.shuffle(range(3)) for c in self.shuffle(range(3))]
        self.nums = self.shuffle(range(1, 10))
        self.grid = [[self.nums[self.pattern(r, c)] for c in self.cols] for r in self.rows]
        self.grid_solved = [[self.nums[self.pattern(r, c)] for c in self.cols] for r in self.rows]

        self.empties = randint(55, 65) # cases qui deviendront vide (entre 50 et 60)
        for p in sample(range(81), self.empties):
            self.grid[p // 9][p % 9] = 0

        self.drawGrid()

    def shuffle(self, s):
        return sample(s, len(s))

    def pattern(self, r, c):
        return (3 * (r % 3) + r // 3 + c) % 9

    def solveGrid(self, solve):
        for x in range(9):
            for y in range(9):
                if self.grid[y][x] != 0:
                    if self.grid[y][x] != self.grid_solved[y][x]:
                        left = x * 50 + 75 + 2
                        top = y * 50 + 50 + 2
                        size_x = 50 - 2
                        size_y = 50 - 2
                        s = pygame.Surface((size_x, size_y), pygame.SRCALPHA)
                        s.fill((255, 0, 0, 200))
                        self.screen.blit(s, (left, top))
        if solve:
            for x in range(9):
                for y in range(9):
                    self.grid[y][x] = self.grid_solved[y][x]

    def drawGrid(self):
        x, y = 75, 50
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, (80, 80, 80), (x, 50), (x, 10 * 50), 4)
            else:
                pygame.draw.line(self.screen, (80, 80, 80), (x, 50), (x, 10 * 50), 2)
            x += 50
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, (80, 80, 80), (75, y), (10 * 50 + 25, y), 4)
            else:
                pygame.draw.line(self.screen, (80, 80, 80), (75, y), (10 * 50 + 25, y), 2)
            y += 50

    def updateGrid(self, x, y):
        self.grid[y][x] = self.grid[y][x] % 9 + 1

class Solver:

    def __init__(self):

        self.running = True
        self.buttonFont = pygame.font.SysFont('lato', 30)
        self.solveButton = pygbutton.PygButton((25, 550, 150, 50), "Résoudre le sudoku", bgcolor=(230, 230, 230))
        self.clearButton = pygbutton.PygButton((25 + 160, 550, 200, 50), "Générer un autre sudoku", bgcolor=(230, 230, 230))
        self.errorOnButton = pygbutton.PygButton((25 + 370, 550, 180, 50), "Afficher les erreurs", bgcolor=(230, 230, 230))
        self.errorOffButton = pygbutton.PygButton((25 + 370, 550, 180, 50), "Masquer les erreurs", bgcolor=(230, 230, 230))
        self.screen = pygame.display.set_mode((600, 650))
        pygame.display.set_caption("Sudoku solver")
        self.error = False
        self.grid = Grid(self.screen)


    def mainLoop(self):

        while self.running:
            pygame.time.delay(10)

            self.screen.fill((245, 245, 245))
            self.grid.drawGrid()

            if self.error:
                self.grid.solveGrid(False)
                self.errorOnButton.draw(self.screen)
            else:
                self.errorOffButton.draw(self.screen)

            self.solveButton.draw(self.screen)
            self.clearButton.draw(self.screen)

            for x in range(9):
                for y in range(9):
                    if self.grid.grid[y][x] != 0:
                        pos_x = x * 50 + 18 + 75
                        pos_y = y * 50 + 18 + 50
                        text = self.grid.font.render(str(self.grid.grid[y][x]), True, (80, 80, 80))
                        self.screen.blit(text, (pos_x, pos_y))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    exit()

                if "click" in self.solveButton.handleEvent(event):
                    self.grid.solveGrid(True)

                if "click" in self.clearButton.handleEvent(event):
                    self.grid = Grid(self.screen)

                if self.error:
                    if "click" in self.errorOffButton.handleEvent(event):
                        self.error = False
                else:
                    if "click" in self.errorOnButton.handleEvent(event):
                        self.error = True

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if 75 <= x <= 525 and 50 <= y <= 500:
                        pos_x = (x - 75) // 50
                        pos_y = (y - 50) // 50
                        self.grid.updateGrid(pos_x, pos_y)

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    Solver().mainLoop()