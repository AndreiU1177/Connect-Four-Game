import importlib
import sys
import os

# Add the src folder to sys.path to make it importable if running directly
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    print("1. Play in console")
    print("2. Play with graphical user interface")
    choice = input(">>>")
    if choice == '2':
        module = importlib.import_module('src.ui.gui')
        module.main()
    elif choice == '1':
        module = importlib.import_module('src.ui.ui')
    else:
        print("No such choice! Your options are either 1 or 2, nothing else!")
