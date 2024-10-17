import unittest

from src.utils.exceptions import FullColumn, InvalidColumn

from src.service.service import Service


class TestService(unittest.TestCase):
    def testPlace(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('X', 1)
        self.assertEqual(board[6][1], 'X', 'not placed')
        service.place('X', 1)
        self.assertEqual(board[5][1], 'X', 'not placed')
        service.place('X', 1)
        service.place('X', 1)
        service.place('X', 1)
        service.place('X', 1)
        with self.assertRaises(FullColumn):
            service.place('X', 1)
        with self.assertRaises(InvalidColumn):
            service.place('X', 99)

    def testGetColumn(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('X', 1)
        col = service.getColumn(1, board)
        self.assertEqual(col, [' ', ' ', ' ', ' ', ' ', 'X'])

    def testGetRow(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('X', 1)
        row = service.getRow(6, board)
        self.assertEqual(row, [' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    def testGetDiagonals(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('X', 1)
        main, secondary = service.getDiagonals(6, 1, board)
        main = main.tolist()
        secondary = secondary.tolist()
        self.assertEqual(main, [' ', 'X', ' '])
        self.assertEqual(secondary, [' ', ' ', ' ', ' ', ' ', ' ', 'X', ' '])

    def testCheckHorizontal(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('X', 1)
        service.place('X', 2)
        service.place('X', 3)
        service.place('X', 4)
        self.assertEqual(service.checkHorizontal(6, 'X', board), True)

    def testCheckVertical(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('X', 1)
        service.place('X', 1)
        service.place('X', 1)
        service.place('X', 1)
        self.assertEqual(service.checkVertical(1, 'X', board), True)

    def testCheckDiagonal(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('X', 1)
        service.place('X', 2)
        service.place('X', 2)
        service.place('X', 3)
        service.place('X', 3)
        service.place('X', 3)
        service.place('X', 4)
        service.place('X', 4)
        service.place('X', 4)
        service.place('X', 4)
        self.assertEqual(service.checkDiagonal(6, 1, 'X', board), True)

    def testComputerWinVertical(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('O', 1)
        service.place('O', 1)
        service.place('O', 1)
        self.assertEqual(service.computerMove(), (3, 1))

    def testComputerWinHorizontal(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('O', 1)
        service.place('O', 2)
        service.place('O', 3)
        self.assertEqual(service.computerMove(), (6, 4))

    def testComputerWinDiagonal(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('O', 1)
        service.place('O', 2)
        service.place('O', 2)
        service.place('O', 3)
        service.place('O', 3)
        service.place('O', 3)
        service.place('X', 3)
        service.place('X', 4)
        service.place('X', 4)
        service.place('X', 4)
        self.assertEqual(service.computerMove(), (3, 4))

    def testComputerAdjacent(self):
        service = Service(6, 7)
        board = service.getBoard()
        service.place('O', 1)
        service.place('O', 2)
        service.place('O', 3)
        service.place('X', 4)
        self.assertEqual(service.computerMove(), (5, 2))

    def testDraw(self):
        service = Service(2, 2)
        service.place('X', 1)
        service.place('X', 1)
        service.place('X', 2)
        self.assertEqual(service.checkDraw(), False)
        service.place('X', 2)
        self.assertEqual(service.checkDraw(), True)


if __name__ == '__main__':
    unittest.main()
