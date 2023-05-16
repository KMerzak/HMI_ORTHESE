from Logic import *
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Acc()
    ui.show()
    sys.exit(app.exec())
