from copy import deepcopy

from texttable import Texttable


class Board:
    def __init__(self, height, width):
        """
        Creates a board, given by a matrix
        :param height: height of board
        :param width: width of board
        Indexing starts from 1
        """
        self.__board = [[' ' for _ in range(width + 2)] for _ in range(height + 2)]
        self.__width = width
        self.__height = height

    @property
    def board(self):
        """
        :return: board matrix
        """
        return self.__board

    @property
    def height(self):
        """
        :return: height of board
        """
        return self.__height

    @property
    def width(self):
        """
        :return: width of board
        """
        return self.__width

    def place(self, symbol, row, column):
        """
        Places piece at coordinates
        :param symbol: symbol to place
        :param row: 1st coordinate
        :param column: 2nd coordinate
        :return: placed piece
        """
        self.__board[row][column] = symbol

    def __str__(self):
        """
        :return: prints the board using texttable
        """
        table = Texttable()
        for row_index, row in enumerate(self.__board):
            rowCopy = deepcopy(row)
            rowCopy.pop(0)
            rowCopy.pop(len(rowCopy) - 1)
            if row_index not in (0, len(self.__board) - 1):
                table.add_row(rowCopy)
        plus_row = []
        for i in range(0, self.__width):
            plus_row.append(i+1)
        table.add_row(plus_row)
        return table.draw()

