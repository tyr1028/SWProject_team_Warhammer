import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 화면
        self.setWindowTitle('pyqt5 demo')
        self.center() 
        self.resize(1500, 800)   

        # 1
        btnUn1 = QPushButton("unit1", self)	
        btnUn1.move(80, 100)	
        btnUn1.resize(150,50)
        btnUn1.clicked.connect(self.btnRun_clicked)	

        btnUn2 = QPushButton("unit2", self)	
        btnUn2.move(80, 200)	
        btnUn2.resize(150,50)
        btnUn2.clicked.connect(self.btnRun_clicked)

        btnUn3 = QPushButton("unit3", self)	
        btnUn3.move(80, 300)	
        btnUn3.resize(150,50)
        btnUn3.clicked.connect(self.btnRun_clicked)

        btnUn4 = QPushButton("unit4", self)	
        btnUn4.move(80, 400)	
        btnUn4.resize(150,50)
        btnUn4.clicked.connect(self.btnRun_clicked)

        #2
        btnUn5 = QPushButton("unit5", self)	
        btnUn5.move(1250, 100)	
        btnUn5.resize(150,50)
        btnUn5.clicked.connect(self.btnRun_clicked)

        btnUn6 = QPushButton("unit6", self)	
        btnUn6.move(1250, 200)	
        btnUn6.resize(150,50)
        btnUn6.clicked.connect(self.btnRun_clicked)
        
        btnUn7 = QPushButton("unit7", self)	
        btnUn7.move(1250, 300)	
        btnUn7.resize(150,50)
        btnUn7.clicked.connect(self.btnRun_clicked)	        
        
        btnUn8 = QPushButton("unit8", self)	
        btnUn8.move(1250, 400)	
        btnUn8.resize(150,50)
        btnUn8.clicked.connect(self.btnRun_clicked)	

    def btnRun_clicked(self):
        QMessageBox.about(self, "message", "Faction: Imperial Guard")

    '''
    화면의 가운데로 띄우기
    '''
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   app.exec_()