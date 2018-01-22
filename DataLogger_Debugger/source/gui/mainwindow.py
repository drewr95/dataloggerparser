# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QColor
import os
import time


class Ui_MainWindow(QtWidgets.QMainWindow):
    """
    Main application window
    """

    filenames = []
    colors = {
        'red': QColor('red'), 'green': QColor('green'),
        'yellow': QColor('yellow'), 'orange': QColor('orange'),
        'black': QColor('black')
    }

    def __init__(self):
        """
        Initialize components of the MainWindow then set them up
        """
        super(Ui_MainWindow, self).__init__()

        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.mainVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.textEditVerticalLayout = QtWidgets.QVBoxLayout()
        self.outputBox = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.totalProgressLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.progressBarTotal = QtWidgets.QProgressBar(self.verticalLayoutWidget_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.browseButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.parseButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)


        self.setupUi(MainWindow=self)
        self.browseButton.clicked.connect(self.browseFileSystem)
        self.parseButton.clicked.connect(self.openFiles)
        self.cancelButton.clicked.connect(self.resetAllFields)
        self.cancelButton.setEnabled(False)
        self.parseButton.setEnabled(False)
        self.writeToOutputBox(message="'Browse Files' to select log files")


    def setupUi(self, MainWindow):
        """
        sets up UI_MainWindow
        :param MainWindow: self
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(487, 378)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 9, 461, 361))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.mainVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainVerticalLayout.setObjectName("mainVerticalLayout")
        self.textEditVerticalLayout.setObjectName("textEditVerticalLayout")
        self.outputBox.setReadOnly(True)
        self.outputBox.setObjectName("outputBox")
        self.textEditVerticalLayout.addWidget(self.outputBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.totalProgressLabel.setObjectName("totalProgressLabel")
        self.verticalLayout_2.addWidget(self.totalProgressLabel)
        self.progressBarTotal.setProperty("value", 0)
        self.progressBarTotal.setObjectName("progressBarTotal")
        self.verticalLayout_2.addWidget(self.progressBarTotal)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.browseButton.setObjectName("browseButton")
        self.horizontalLayout.addWidget(self.browseButton)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Cancel")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.parseButton.setObjectName("parseButton")
        self.horizontalLayout.addWidget(self.parseButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.textEditVerticalLayout.addLayout(self.verticalLayout_2)
        self.mainVerticalLayout.addLayout(self.textEditVerticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        """
        auto-generated code
        :param MainWindow:
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Logger Parser"))
        self.totalProgressLabel.setText(_translate("MainWindow", "Total Progress :"))
        self.browseButton.setText(_translate("MainWindow", "Browse Files"))
        self.parseButton.setText(_translate("MainWindow", "Parse Files"))

    def browseFileSystem(self):
        """
        open a new window to browse the file file system for log files
        """
        self.filenames = list(QFileDialog.getOpenFileNames(parent=None, caption='Test Dialog',
                                                      directory=os.getcwd(), filter="Text files (*.log)"))

        # only save the file name info
        self.filenames = self.filenames[0]

        if len(self.filenames) > 0:
            for file in self.filenames:
                self.writeToOutputBox(message=file, color='green')
            self.parseButton.setEnabled(True)
            self.cancelButton.setEnabled(True)
        else:
            self.writeToOutputBox(message='No files selected', color='red')

    def openFiles(self):
        """
        parses log files and writes them to a csv file
        """
        count = 0
        totalCount = len(self.filenames)
        oldPercentage = 0
        currentPercentage = 0
        for file in self.filenames:
            (prefix, sep, suffix) = str(file).rpartition('.')
            csvFile = prefix + '.csv'
            self.writeToOutputBox(message='\nReading file :')
            self.writeToOutputBox(message=file, color='orange')
            self.writeToOutputBox(message='Writing to :')
            self.writeToOutputBox(message=csvFile, color='orange')

            with open(file, 'r') as inFile, open(csvFile, 'w') as outFile:
                self.parseFiles(inFile=inFile, outFile=outFile)

            count += 1
            currentPercentage = int(count / totalCount * 100)
            if oldPercentage + 1 < currentPercentage:
                oldPercentage = currentPercentage
                self.updateProgressBar(percentage=currentPercentage)

        self.parseButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        self.writeToOutputBox(message='\nDone', color='green')

    def parseFiles(self, inFile, outFile):
        """
        parses the data in the log file and writes to the csv file
        :param inFile: log file
        :param outFile: csv file
        """
        outFile.write('date, name, value\n')
        inFile.readline()

        for line in inFile:
            line = line.replace('"', '')
            line = line.replace(' ', '')
            data = line.split(',')
            outFile.write(data[0] + ',' + data[1] + ',' + data[2] + '\n')

    def updateProgressBar(self, percentage:int):
        """
        sets the value of the progress bar
        :param percentage: percentage completed of the current task
        """
        self.progressBarTotal.setValue(percentage)

    def resetAllFields(self):
        """
        reset the window's settings
        """
        self.filenames = []
        self.outputBox.clear()
        self.cancelButton.setEnabled(False)
        self.parseButton.setEnabled(False)
        self.writeToOutputBox(message="'Browse Files' to select log files")

    def writeToOutputBox(self, message:str, color:str = 'black'):
        """
        writes to the outputBox
        :param message: message to print
        :param color: color of the text
        """
        self.outputBox.setTextColor(self.colors.get(color))
        self.outputBox.append(message)