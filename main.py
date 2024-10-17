import importlib


if __name__ == '__main__':
    print("1. Play in console")
    print("2. Play with graphical user interface")
    choice = input(">>>")
    if choice == '2':
        module = importlib.import_module('src.ui.gui')
    elif choice == '1':
        module = importlib.import_module('src.ui.ui')

