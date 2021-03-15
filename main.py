from PyQt5.QtWidgets import QApplication

import sys
import os


sys._excepthook = sys.excepthook

# needed to catch exceptions from the UI
def my_exception_hook(exctype, value, trace6back):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = my_exception_hook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
