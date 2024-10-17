import time

from src.utils.exceptions import InvalidInput, FullColumn, InvalidColumn
from src.service.service import Service

class Ui:
    def __init__(self):
        try:
            self.__height, self.__width = self.initiateBoard()
            self.__service = Service(self.__height, self.__width)
        except (InvalidInput, InvalidColumn, FullColumn) as ve:
            print(ve)
            print("Program will stop...")
            exit()

    def start(self):
        try:
            turn = bool(self.chooseStart())
            self.printBoard()
            while True:
                try:
                    if self.__service.checkDraw():
                        print("Draw!")
                        break
                    if turn:
                        column = self.chooseColumn()
                        row, col = self.__service.place('X', column)
                    else:
                        print("Computer is placing piece...")
                        time.sleep(1)
                        row, col = self.__service.computerMove()
                    self.printBoard()
                    symbol = 'X' if turn else 'O'
                    if self.__service.checkWin(row, col, symbol, self.__service.getBoard()):
                        if symbol == 'X':
                            print("You won!")
                        else:
                            print("Computer won!")
                        break
                    turn = not turn
                except (InvalidInput, InvalidColumn, FullColumn) as ve:
                    print(ve)
        except (InvalidInput, InvalidColumn, FullColumn) as ve:
            print(ve)

    def initiateBoard(self):
        print("This is a Connect Four game!")
        print("Player plays with 'X', and Computer with 'O'")
        print("1. Play with 6x7 board")
        print("2. Play with custom board")
        option = input(">>>")
        if option == '1':
            return 6, 7
        elif option == '2':
            print("Choose size:")
            height = input("Number of rows ->")
            if not height.isnumeric():
                raise InvalidInput("Invalid size")
            width = input("Number of columns ->")
            if not width.isnumeric():
                raise InvalidInput("Invalid size")
            height = int(height)
            width = int(width)
            if height < 4 and width < 4:
                raise InvalidInput("Sizes are too small, make sure at least 1 dimension is >= 4")
            print("Board created!")
            print("-")
            return height, width
        else:
            raise InvalidInput("Invalid command")

    def chooseStart(self):
        print("Who do you want to start the game?")
        print("1. You")
        print("2. Computer")
        option = input(">>>")
        if option == '1':
            return 1
        elif option == '2':
            return 0
        else:
            raise InvalidInput("Invalid command")

    def printBoard(self):
        print(self.__service.getBoardObj())

    def chooseColumn(self):
        print("Your turn! Enter number of column to place your piece!")
        option = input(">>>")
        if not option.isnumeric():
            raise InvalidInput("Invalid number for column")
        return int(option)


ui = Ui()
ui.start()
