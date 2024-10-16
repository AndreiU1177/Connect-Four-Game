import random
import unittest
from copy import deepcopy

from domain import Board
from exceptions import FullColumn, InvalidColumn
import numpy as np


class Service:
    def __init__(self, height, width):
        """
        Creates board with desired dimensions, which are saved in MAXROW and MAXCOLUMN
        :param height: number of rows
        :param width: number of columns
        """
        self.__board = Board(height, width)
        self.MAXROW = self.__board.height
        self.MAXCOLUMN = self.__board.width

    def place(self, symbol, column):
        """
        Validates spot, if valid, places piece at the corresponding position
        :param symbol: the symbol for the player or computer
        :param column: column to place
        :return: piece placed
        """
        self.validate_column(column)
        gameBoard = self.__board.board
        rowToPlace = -1
        for i in range(1, self.MAXROW + 1):
            if gameBoard[i][column] == ' ':
                rowToPlace = i
        self.__board.place(symbol, rowToPlace, column)
        return rowToPlace, column

    def validate_column(self, column):
        """
        Validating column to exist and to not be fully populated
        :param column: column to validate
        :return: raises errors if column not valid
        """
        gameBoard = self.__board.board
        if column > self.MAXCOLUMN or column < 1:
            raise InvalidColumn("Invalid column")
        if gameBoard[1][column] != ' ':
            raise FullColumn("Column is fully populated")

    def getBoardObj(self):
        """
        :return: board object
        """
        return self.__board

    def getBoard(self):
        """
        :return: board represented as a matrix
        """
        return self.__board.board

    def getColumn(self, col, board):
        """
        :param col: column to fetch
        :param board: source of the column
        :return: the desired column, as a list
        """
        column = []
        for i in range(1, self.MAXROW + 1):
            column.append(board[i][col])
        return column

    def getRow(self, row, board):
        """
        :param row: row to fetch
        :param board: source of the row
        :return: the desired row, as a list
        """
        return board[row]

    def getDiagonals(self, row, col, board):
        """
        Fetch the main and the secondary diagonal that cross a certain point
        :param row: 1st coordinate of the point
        :param col: 2nd coordinate of the point
        :param board: source of the point
        :return: the 2 diagonals, as lists
        """
        lst = np.array(board)

        i, j = row, col  # position of element
        main = np.diagonal(lst, offset=(j - i))

        secondary = np.diagonal(np.rot90(lst), offset=-lst.shape[1] + (j + i) + 1)
        return main, secondary

    def checkWin(self, row, col, symbol, board):
        """
        Checks for win horizontally, vertically and diagonally
        :param row: 1st coordinate of the point
        :param col: 2nd coordinate of the point
        :param symbol: symbol, either player's or computer's
        :param board: source of the point and where to check
        :return: True if won, False otherwise
        """
        if self.checkHorizontal(row, symbol, board):
            return True
        if self.checkVertical(col, symbol, board):
            return True
        if self.checkDiagonal(row, col, symbol, board):
            return True
        return False

    def checkHorizontal(self, row, symbol, board):
        """
        Checks for win horizontally
        :param row: row to check
        :param symbol: symbol to look up
        :param board: board to check
        :return: True if won, False otherwise
        """
        lst = self.getRow(row, board)
        for i in range(1, self.MAXCOLUMN - 2):
            if lst[i] == lst[i+1] == lst[i+2] == lst[i+3] == symbol:
                return True
        return False

    def checkVertical(self, col, symbol, board):
        """
        Checks for win vertically
        :param col: column to check
        :param symbol: symbol to look up
        :param board: board to check
        :return: True if won, False otherwise
        """
        lst = self.getColumn(col, board)
        for i in range(0, self.MAXROW - 3):
            if lst[i] == lst[i + 1] == lst[i + 2] == lst[i + 3] == symbol:
                return True
        return False

    def checkDiagonal(self, row, col, symbol, board):
        """
        :param row: 1st coordinate of point
        :param col: 2nd coordinate of point
        :param symbol: symbol to look up
        :param board: board to check
        :return: True if won, False otherwise
        """
        main, secondary = self.getDiagonals(row, col, board)
        for i in range(1, len(main) - 4):
            if main[i] == main[i+1] == main[i+2] == main[i+3] == symbol:
                return True
        for i in range(1, len(secondary) - 4):
            if secondary[i] == secondary[i+1] == secondary[i+2] == secondary[i+3] == symbol:
                return True
        return False

    def computerMove(self):
        """
        Manages the computer's turn
        It checks firstly for all available moves
        Prioritizes win, then blocking player's win
        Tries to place pieces somewhere near other pieces of his
        :return: coordinates of the point he placed, or -1, -1 if couldn't place (it will result in a draw)
        """
        gameBoard = self.getBoard()
        available_moves = []
        for column in range(1, self.MAXCOLUMN + 1):
            rowToPlace = -1
            for i in range(1, self.MAXROW + 1):
                if gameBoard[i][column] == ' ':
                    rowToPlace = i
            if rowToPlace != -1:
                available_moves.append((rowToPlace, column))
        # try to win or block player's win
        colToMove = self.checkPotentialWin(available_moves)
        if colToMove != -1:
            return self.place('O', colToMove)
        # try to place a piece adjacent to another
        colToMove = self.checkAdjacent(available_moves)
        if colToMove != -1:
            return self.place('O', colToMove)
        randomMove = available_moves[random.randint(0, len(available_moves)-1)]
        if len(available_moves) != 0:
            return self.place('O', randomMove[1])
        return -1, -1

    def checkPotentialWin(self, available_moves):
        """
        Iterates through available moves and checks if 1 move can win the game
        :param available_moves: available moves
        :return: column to place piece to win, or -1 if can't win
        """
        # check computer win
        for move in available_moves:
            temp_board = deepcopy(self.getBoard())
            temp_board[move[0]][move[1]] = 'O'
            if self.checkWin(move[0], move[1], 'O', temp_board):
                return move[1]

        # check player win
        for move in available_moves:
            temp_board = deepcopy(self.getBoard())
            temp_board[move[0]][move[1]] = 'X'
            if self.checkWin(move[0], move[1], 'X', temp_board):
                return move[1]
        return -1

    def checkAdjacent(self, available_moves):
        """
        Iterates through available moves and looks for the move where are the most pieces around of the same type
        :param available_moves: available move
        :return: column to place piece
        """
        board = self.getBoard()
        colToPlace = -1
        maxAdjacent = -1
        for move in available_moves:
            row, col = move
            adjacent_pieces = self.adjacentCount(row, col)
            if adjacent_pieces > maxAdjacent and adjacent_pieces != 0:
                maxAdjacent = adjacent_pieces
                colToPlace = col
        return colToPlace

    def adjacentCount(self, row, col):
        """
        Counts adjacent pieces around a certain point
        :param row: 1st coordinate of the point
        :param col: 2nd coordinate of the point
        :return: count of adjacent pieces
        """
        board = self.getBoard()
        count = 0
        elems = [(row-1, col), (row-1, col+1), (row, col+1), (row+1, col+1), (row+1, col), (row+1, col-1), (row, col-1), (row-1, col-1)]
        for elem in elems:
            if board[elem[0]][elem[1]] == 'O':
                count += 1
        return count

    def checkDraw(self):
        """
        Checks if game is draw by checking the top row
        :return: True if game is draw, False otherwise
        """
        count = 0
        board = self.getBoard()
        for i in range(1, self.MAXCOLUMN+1):
            if board[1][i] == ' ':
                count += 1
        return count == 0
