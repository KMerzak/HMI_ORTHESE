from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys
acc,_ = loadUiType(os.path.join('mainwindow.ui'))
sea,_ = loadUiType(os.path.join('seance.ui'))

class Acc(QMainWindow,acc):
    def __init__(self,parent=None):
        super(Acc, self).__init__(parent)
        self.setupUi(self)
        self.w=None
        self.buttSeance.clicked.connect(self.onClicked)

    def onClicked(self):
        if self.w== None:
            self.w=Seance()
            self.w.show()
        else :
            self.w=None 


class Seance(QWidget,sea):
    def __init__(self,parent=None):
        super(Seance, self).__init__(parent)
        self.setupUi(self)











def show_new_window(self):
        if self.w==None :
            self.w=AnotherWindow()
            self.w.show()





