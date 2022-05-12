import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


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
        btnUn1.resize(150,50)
        btnUn1.clicked.connect(self.btnRun_clicked)	

        btnUn2 = QPushButton("unit2", self)
        btnUn2.resize(150,50)
        btnUn2.clicked.connect(self.btnRun_clicked)

        btnUn3 = QPushButton("unit3", self)
        btnUn3.resize(150,50)
        btnUn3.clicked.connect(self.btnRun_clicked)

        btnUn4 = QPushButton("unit4", self)
        btnUn4.resize(150,50)
        btnUn4.clicked.connect(self.btnRun_clicked)

        #2
        btnUn5 = QPushButton("unit5", self)
        btnUn5.resize(150,50)
        btnUn5.clicked.connect(self.btnRun_clicked)

        btnUn6 = QPushButton("unit6", self)
        btnUn6.resize(150,50)
        btnUn6.clicked.connect(self.btnRun_clicked)
        
        btnUn7 = QPushButton("unit7", self)
        btnUn7.resize(150,50)
        btnUn7.clicked.connect(self.btnRun_clicked)	        
        
        btnUn8 = QPushButton("unit8", self)
        btnUn8.resize(150,50)
        btnUn8.clicked.connect(self.btnRun_clicked)	

        btn_layout_1 = QVBoxLayout()
        btn_layout_1.addWidget(btnUn1)
        btn_layout_1.addWidget(btnUn2)
        btn_layout_1.addWidget(btnUn3)
        btn_layout_1.addWidget(btnUn4)

        btn_layout_2 = QVBoxLayout()
        btn_layout_2.addWidget(btnUn5)
        btn_layout_2.addWidget(btnUn6)
        btn_layout_2.addWidget(btnUn7)
        btn_layout_2.addWidget(btnUn8)
        
        photo_label = QLabel()
        photo_label.setPixmap(QPixmap('KakaoTalk_20220405_180751959.jpg'))

        all_layout = QHBoxLayout()
        all_layout.addLayout(btn_layout_1)
        all_layout.addWidget(photo_label)
        all_layout.addLayout(btn_layout_2)

        self.setLayout(all_layout)

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