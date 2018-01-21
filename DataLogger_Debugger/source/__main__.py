import os
import sys
import source.gui.mainwindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    mainwindow = source.gui.mainwindow.Ui_MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
    return 0


if __name__ == '__main__':
    main()