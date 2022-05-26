import os 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2 as cv
from matplotlib.pyplot import table
import numpy as np
from math import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INCH = 35

class App(QWidget):
    def __init__(self, p1 = "", p2 = ""):
        super().__init__()
        self.initUI()
        self.p1 = p1
        self.p2 = p2

        self.count = 0
        self.x1 = 0
        self.y1 = 0

        #print("m: %2d, apl: %2d, ga: %2d, df: %2d, sv: %2d, w: %2d" %(self.p1.ft1.agents[0].m, self.p1.ft1.agents[0].apl, self.p1.ft1.agents[0].ga, self.p1.ft1.agents[0].df, self.p1.ft1.agents[0].sv, self.p1.ft1.agents[0].w))

    def initUI(self):
        # 화면
        self.setWindowTitle('pyqt5 demo')
        # self.center()
        self.resize(1500, 800)   

         # 1
        btnUn1 = QPushButton("unit1", self)		
        btnUn1.resize(150,50)
        btnUn1.clicked.connect(lambda :self.window_open(0))	

        btnUn2 = QPushButton("unit2", self)	
        btnUn2.resize(150,50)
        btnUn2.clicked.connect(lambda :self.window_open(1))

        btnUn3 = QPushButton("unit3", self)	
        btnUn3.resize(150,50)
        btnUn3.clicked.connect(lambda :self.window_open(2))

        btnUn4 = QPushButton("unit4", self)	
        btnUn4.resize(150,50)
        btnUn4.clicked.connect(lambda :self.window_open(3))

        #2
        btnUn5 = QPushButton("unit5", self)	
        btnUn5.resize(150,50)
        btnUn5.clicked.connect(lambda :self.window_open(4))

        btnUn6 = QPushButton("unit6", self)		
        btnUn6.resize(150,50)
        btnUn6.clicked.connect(lambda :self.window_open(5))
        
        btnUn7 = QPushButton("unit7", self)	
        btnUn7.resize(150,50)
        btnUn7.clicked.connect(lambda :self.window_open(6))	        
        
        btnUn8 = QPushButton("unit8", self)		
        btnUn8.resize(150,50)
        btnUn8.clicked.connect(lambda :self.window_open(7))

        self.dialog = QDialog()

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

        self.location = []

        self.img = cv.imread('field.png', cv.IMREAD_COLOR)
        for i in range(100, self.height(), int(self.height() / 5)):
            self.location.append([100, i])
            cv.circle(self.img, (100, i), 5, (255, 255, 0), -1)
        for i in range(100, self.height(), int(self.height() / 5)):
            self.location.append([1050, i])
            cv.circle(self.img, (1050, i), 5, (255, 0, 255), -1)
        cv.imwrite('field.png', self.img)

        photo_label = QLabel()
        photo_label.setPixmap(QPixmap('field.png'))
        photo_label.mousePressEvent = self.click_event

        all_layout = QHBoxLayout()
        all_layout.addLayout(btn_layout_1)
        all_layout.addWidget(photo_label)
        all_layout.addLayout(btn_layout_2)

        self.setLayout(all_layout)

    def window_open(self, i):
        dialog = QDialog()
        #btnDialog = QPushButton("Close", dialog)
        #btnDialog.move(200,400)
        #btnDialog.clicked.connect(self.window_close)
        

        # 테이블
        data = {'m': self.p1.ft1.agents[i].m,'apl': self.p1.ft1.agents[i].apl,'ga': self.p1.ft1.agents[i].ga,'df': self.p1.ft1.agents[i].df
        ,'df': self.p1.ft1.agents[i].df, 'sv': self.p1.ft1.agents[i].sv,'w': self.p1.ft1.agents[i].w}

        tableWidget = QTableWidget()
        tableWidget.setRowCount(1)
        tableWidget.setColumnCount(6)

        tableWidget.setVerticalHeaderLabels([self.p1.ft1.agents[i].type])
        
        horHeaders = []
        for n, key in enumerate(data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(str(data[key])):
                newitem = QTableWidgetItem(item)
                tableWidget.setItem(m, n, newitem)
        tableWidget.setHorizontalHeaderLabels(horHeaders)
        print(horHeaders)

        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #버튼
        btnMove = QPushButton("이동", dialog)		
        btnMove.resize(150,50)

        btnShoot = QPushButton("사격", dialog)		
        btnShoot.resize(150,50)

        btnBattle = QPushButton("전투", dialog)		
        btnBattle.resize(150,50)

        btnNon = QPushButton("수행하지않음", dialog)		
        btnNon.resize(150,50)

        btn_unit_layout = QHBoxLayout()
  
        btn_unit_layout.addLayout(btnMove)
        btn_unit_layout.addLayout(btnShoot)
        btn_unit_layout.addLayout(btnBattle)
        btn_unit_layout.addLayout(btnNon)
        dialog.setLayout(layout)


        layout = QVBoxLayout()
        dialog.setLayout(layout)
        layout.addWidget(tableWidget)

        """self.setWindowTitle('QTableWidget')
        self.setWindowModality(Qt.ApplicationModal)
        self.setGeometry(300, 100, 600, 400)
        self.show()"""

        dialog.setWindowTitle("Second window")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(500, 500)
        #dialog.closeEvent = self.CloseEvent
        dialog.exec()
        #dialog.show(("1: %2d, 2: %2d, 3: %2d, 4: %2d, 5: %2d, 6: %2d" %(self.p1.ft1.agents[0].m, self.p1.ft1.agents[0].apl, self.p1.ft1.agents[0].ga, self.p1.ft1.agents[0].df, self.p1.ft1.agents[0].sv, self.p1.ft1.agents[0].w)))
    
    """def CloseEvent(self, event):
        for i in reversed(range(dialog.layout().count())): 
            dialog.layout().itemAt(i).widget().setParent(None)

    def window_close(self):
        dialog.close()"""

    def click_event(self, event):
        if self.count % 2 == 0:
            self.x1 = event.pos().x()
            self.y1 = event.pos().y()

            i = self.color_check(self.x1, self.y1)
            if i == None:
                count -= 1

            print("Hello, x: %3d, y: %3d" %(self.x1, self.y1))
            print(i)

        else:
            x2 = event.pos().x()
            y2 = event.pos().y() 

            print("Hello, x: %3d, y: %3d" %(x2, y2))

            self.target_range(self.x1, self.y1, x2, y2, 3)
        
        self.count += 1

    def color_check(self, x1, y1):
        result = 0
        distance = 0
        print(x1, y1)
        print(self.img[x1][y1])
        if self.img[x1][y1] == (0, 0, 0):
            return None
        else:
            for i in len(self.location):
                if dist((x1, y1), (self.location[i])) > distance:
                    result = i
            return result

    def target_range(self, x1, y1, x2, y2, range):
        '''dy = y2 - y1
        dx = x2 - x1
        angle = atan(dy/dx) * (180.0/pi)
        
        if dx < 0:
            angle += 180.0
        else:
            if(dy<0.0): angle += 360.0

        angle = radians(angle)'''
        if dist((x1, y1), (x2, y2)) > range*INCH:
            print("넘음")
        else:
            print("통과")      
        

    def agent_select_test(self, x, y):
        '''for agent in self.p1.ft1.agents:
            if agent.'''
        pass

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
    img = cv.imread('field.png', cv.IMREAD_COLOR)
    img = np.zeros((img.shape))
    cv.imwrite('field.png', img)