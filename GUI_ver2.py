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
        self.agent_selected = None

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
        btnUn1.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[0]))

        btnUn2 = QPushButton("unit2", self)	
        btnUn2.resize(150,50)
        btnUn2.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[1]))

        btnUn3 = QPushButton("unit3", self)	
        btnUn3.resize(150,50)
        btnUn3.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[2]))

        btnUn4 = QPushButton("unit4", self)	
        btnUn4.resize(150,50)
        btnUn4.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[3]))

        #2
        btnUn5 = QPushButton("unit5", self)	
        btnUn5.resize(150,50)
        btnUn5.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[0]))

        btnUn6 = QPushButton("unit6", self)		
        btnUn6.resize(150,50)
        btnUn6.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[1]))
        
        btnUn7 = QPushButton("unit7", self)	
        btnUn7.resize(150,50)
        btnUn7.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[2]))	        
        
        btnUn8 = QPushButton("unit8", self)		
        btnUn8.resize(150,50)
        btnUn8.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[3]))

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

    def window_open(self, agent):
        dialog = QDialog()
        #btnDialog = QPushButton("Close", dialog)
        #btnDialog.move(200,400)
        #btnDialog.clicked.connect(self.window_close)
        

        # 테이블
        data = {'m': agent.m,'ap': agent.ap,'ga': agent.ga,'df': agent.df
        ,'df': agent.df, 'sv': agent.sv,'w': agent.w}

        tableWidget = QTableWidget()
        tableWidget.setRowCount(1)
        tableWidget.setColumnCount(6)

        tableWidget.setVerticalHeaderLabels([agent.type])
        
        horHeaders = []
        for n, key in enumerate(data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(str(data[key])):
                newitem = QTableWidgetItem(item)
                tableWidget.setItem(m, n, newitem)
        tableWidget.setHorizontalHeaderLabels(horHeaders)

        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        btn_move = QPushButton("move", self)		
        btn_move.resize(150,50)
        btn_move.clicked.connect(lambda :self.action(agent, 0))

        btn_shoot = QPushButton("shoot", self)		
        btn_shoot.resize(150,50)
        btn_shoot.clicked.connect(lambda :self.action(agent, 1))	

        btn_fight = QPushButton("fight", self)		
        btn_fight.resize(150,50)
        btn_fight.clicked.connect(lambda :self.action(agent, 2))	

        btn_no_action = QPushButton("No Action", self)		
        btn_no_action.resize(150,50)
        btn_no_action.clicked.connect(lambda :self.action(agent, 3))	

        layout = QVBoxLayout()
        dialog.setLayout(layout)
        layout.addWidget(tableWidget)
        layout.addWidget(btn_move)
        layout.addWidget(btn_shoot)
        layout.addWidget(btn_fight)
        layout.addWidget(btn_no_action)

        """self.setWindowTitle('QTableWidget')
        self.setWindowModality(Qt.ApplicationModal)
        self.setGeometry(300, 100, 600, 400)
        self.show()"""

        dialog.setWindowTitle("Second window")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(500, 500)
        #dialog.closeEvent = self.CloseEvent
        dialog.exec()

    def action(self, agent, i):
        if self.agent_selected == False:
            self.agent_selected = True
            
        if i == 3:
            agent.ap = agent.apl
            self.agent_selected = False
            if self.p1.turn == True:
                self.p1.turn = False
                self.p2.turn = True
            else:
                self.p1.turn = True
                self.p2.turn = False
        else:
            if agent.ap == 1:
                agent.ap = agent.apl
                self.agent_selected = False
                if self.p1.turn == True:
                    self.p1.turn = False
                    self.p2.turn = True
                else:
                    self.p1.turn = True
                    self.p2.turn = False
            else:
                agent.ap -= 1
                if i == 0:
                    pos_x, pos_y = self.select_point()
                    agent.move(pos_x, pos_y)
                elif i == 1:
                    pos_x, pos_y = self.select_point()
                    target = self.select_agent()
                    agent.shoot(target)
                else:
                    pos_x, pos_y = self.select_point()
                    target = self.select_agent()
                    agent.fight(target)

            

    
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