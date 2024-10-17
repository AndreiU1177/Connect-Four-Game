from tkinter import messagebox

import pygame
import sys
import math
import tkinter as tk
from src.utils.exceptions import InvalidInput, FullColumn, InvalidColumn
from src.service.service import Service

ROW_COUNT = 6  # Use 6 rows
COLUMN_COUNT = 7  # Use 7 columns
SQUARESIZE = 80
RADIUS = int(SQUARESIZE / 2 - 5)

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()

# Dimensions
width = (COLUMN_COUNT + 2) * SQUARESIZE  # All columns + borders
height = (ROW_COUNT + 1) * SQUARESIZE  # Extra row for the top display
size = (width, height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")


class ConnectFourGUI:
    def __init__(self):
        self.__service = Service(ROW_COUNT, COLUMN_COUNT)
        self.turn = self.whoStarts()  # True for player, False for computer
        self.draw_board()
        if not self.turn:
            self.computer_move()

    def whoStarts(self):
        root = tk.Tk()

        root.withdraw()

        # Ask the player if they want to start
        result = messagebox.askyesno("Start game!", "Do you want to start?")

        # Destroy the tkinter root window after the messagebox is closed
        root.destroy()

        return result

    def draw_board(self):
        for c in range(1, COLUMN_COUNT+1):
            for r in range(0, ROW_COUNT):
                # blue board background
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                # black circles for empty spots
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE)), RADIUS)

        board = self.__service.getBoard()
        for c in range(1, COLUMN_COUNT+1):  # columns 1-7
            for r in range(1, ROW_COUNT+1):  # rows 1-6
                piece = board[r][c]
                if piece == 'X':
                    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int((r-1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif piece == 'O':
                    pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int((r-1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

    def player_move(self, col):
        try:
            row, col = self.__service.place('X', col)
            self.draw_board()
            if self.__service.checkWin(row, col, 'X', self.__service.getBoard()):
                self.show_winner("You won!")
            elif self.__service.checkDraw():
                self.show_winner("It's a draw!")
            else:
                self.turn = False
                self.computer_move()
        except (InvalidInput, InvalidColumn, FullColumn) as ve:
            print(ve)

    def computer_move(self):
        pygame.time.wait(1000)  # computer thinking -_-
        row, col = self.__service.computerMove()
        self.draw_board()
        if self.__service.checkWin(row, col, 'O', self.__service.getBoard()):
            self.show_winner("Computer won!")
        elif self.__service.checkDraw():
            self.show_winner("It's a draw!")
        else:
            self.turn = True

    def show_winner(self, message):
        font = pygame.font.SysFont("monospace", 75)
        label = font.render(message, 1, RED if message == "You won!" else YELLOW)
        screen.blit(label, (40, 10))
        pygame.display.update()
        root = tk.Tk()

        root.withdraw()

        # Ask the player if they want to play again
        result = messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?")

        # Destroy the tkinter root window after the messagebox is closed
        root.destroy()

        # If the player chooses yes, reset the game, otherwise quit
        if result:
            self.reset_game()
        else:
            pygame.quit()
            sys.exit()

    def reset_game(self):
        self.__service.resetBoard()
        self.draw_board()
        self.turn = True


def main():
    game = ConnectFourGUI()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]

                if SQUARESIZE <= posx <= SQUARESIZE * (COLUMN_COUNT+1) and game.turn:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # Player's move
                if game.turn:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE)) # Column 1 to 6
                    game.player_move(col)


main()
