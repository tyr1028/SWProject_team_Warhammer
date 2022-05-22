import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from Player import m, apl, ga, df, sv, w, ap, weapons, pos_x, pos_y, isAlive

class App(QWidget):

    def __init__(self):
        super().__init__()
        
        # 화면
        self.setWindowTitle('pyqt5 demo')
        self.center() 
        self.resize(1500, 800)   

        # 1
        btnUn1 = QPushButton("unit1", self)	
        btnUn1.move(80, 100)	
        btnUn1.resize(150,50)
        btnUn1.clicked.connect(self.dialog_open)	

        btnUn2 = QPushButton("unit2", self)	
        btnUn2.move(80, 200)	
        btnUn2.resize(150,50)
        btnUn2.clicked.connect(self.dialog_open)

        btnUn3 = QPushButton("unit3", self)	
        btnUn3.move(80, 300)	
        btnUn3.resize(150,50)
        btnUn3.clicked.connect(self.dialog_open)

        btnUn4 = QPushButton("unit4", self)	
        btnUn4.move(80, 400)	
        btnUn4.resize(150,50)
        btnUn4.clicked.connect(self.dialog_open)

        #2
        btnUn5 = QPushButton("unit5", self)	
        btnUn5.move(1250, 100)	
        btnUn5.resize(150,50)
        btnUn5.clicked.connect(self.dialog_open)

        btnUn6 = QPushButton("unit6", self)	
        btnUn6.move(1250, 200)	
        btnUn6.resize(150,50)
        btnUn6.clicked.connect(self.dialog_open)
        
        btnUn7 = QPushButton("unit7", self)	
        btnUn7.move(1250, 300)	
        btnUn7.resize(150,50)
        btnUn7.clicked.connect(self.dialog_open)	        
        
        btnUn8 = QPushButton("unit8", self)	
        btnUn8.move(1250, 400)	
        btnUn8.resize(150,50)
        btnUn8.clicked.connect(self.dialog_open)

        self.dialog = QDialog()


    def dialog_open(self):

        btnDialog = QPushButton("Close", self.dialog)
        btnDialog.move(200,400)
        btnDialog.clicked.connect(self.dialog_close)

        self.dialog.setWindowTitle("Second window")
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(500, 500)
        self.dialog.show()

    def dialog_close(self):
        self.dialog.close()

    #def btn_stats(self):
        #self.m = m

        #self.apl = apl

        #self.ga = ga
        #self.df = df
        #self.sv = sv
        #self.w = w
        #self.ap = ap
        #self.weapons = weapons
        #self.pos_x = pos_x
        #self.pos_y = pos_y
        #self.isAlive = boolean    

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