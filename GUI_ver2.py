from asyncio.windows_events import INFINITE
from multiprocessing.connection import wait
import os 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2 as cv
from matplotlib.pyplot import table
import numpy as np
from math import *
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INCH = 35

class MyWorker(QObject):

    wait_for_input = pyqtSignal()
    done = pyqtSignal()


    @pyqtSlot()
    def firstWork(self):
        print('doing first work')
        time.sleep(2)
        print('first work done')
        self.wait_for_input.emit()

    @pyqtSlot()
    def secondWork(self):
        print('doing second work')
        time.sleep(2)
        print('second work done')
        self.done.emit()

class App(QWidget):
    def __init__(self, p1 = "", p2 = ""):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.initUI()
        self.agent_selected = None
        
        for j in range(0, 4, 1):
            self.p1.ft1.agents[j].pos_x = 100
            self.p1.ft1.agents[j].pos_y = 100 + j * int(self.height() / 5)
            print(self.p1.ft1.agents[j].pos_x, self.p1.ft1.agents[j].pos_y)
            self.location.append(self.p1.ft1.agents[j])
            self.p2.ft1.agents[j].pos_x = 1050
            self.p2.ft1.agents[j].pos_y = 100 + j * int(self.height() / 5)
            self.location.append(self.p2.ft1.agents[j])

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
        self.txtLbl1 = QPushButton("현 차례", self)
        self.txtLbl1.setEnabled(False)

        btnUn1 = QPushButton(self.p1.ft1.agents[0].type, self)		
        btnUn1.resize(150,50)
        btnUn1.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[0], self.p1, btnUn1))

        btnUn2 = QPushButton(self.p1.ft1.agents[1].type, self)	
        btnUn2.resize(150,50)
        btnUn2.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[1], self.p1, btnUn2))

        btnUn3 = QPushButton(self.p1.ft1.agents[2].type, self)	
        btnUn3.resize(150,50)
        btnUn3.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[2], self.p1, btnUn3))

        btnUn4 = QPushButton(self.p1.ft1.agents[3].type, self)	
        btnUn4.resize(150,50)
        btnUn4.clicked.connect(lambda :self.window_open(self.p1.ft1.agents[3], self.p1, btnUn4))

        #2
        self.txtLbl2 = QPushButton("", self)
        self.txtLbl2.setEnabled(False)
        
        btnUn5 = QPushButton(self.p2.ft1.agents[0].type, self)	
        btnUn5.resize(150,50)
        btnUn5.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[0], self.p2, btnUn5))

        btnUn6 = QPushButton(self.p2.ft1.agents[1].type, self)		
        btnUn6.resize(150,50)
        btnUn6.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[1], self.p2, btnUn6))
        
        btnUn7 = QPushButton(self.p2.ft1.agents[2].type, self)	
        btnUn7.resize(150,50)
        btnUn7.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[2], self.p2, btnUn7))	        
        
        btnUn8 = QPushButton(self.p2.ft1.agents[3].type, self)		
        btnUn8.resize(150,50)
        btnUn8.clicked.connect(lambda :self.window_open(self.p2.ft1.agents[3], self.p2, btnUn8))

        self.dialog = QDialog()

        btn_layout_1 = QVBoxLayout()
        btn_layout_1.addWidget(self.txtLbl1)
        btn_layout_1.addWidget(btnUn1)
        btn_layout_1.addWidget(btnUn2)
        btn_layout_1.addWidget(btnUn3)
        btn_layout_1.addWidget(btnUn4)
        

        btn_layout_2 = QVBoxLayout()
        btn_layout_2.addWidget(self.txtLbl2)
        btn_layout_2.addWidget(btnUn5)
        btn_layout_2.addWidget(btnUn6)
        btn_layout_2.addWidget(btnUn7)
        btn_layout_2.addWidget(btnUn8)

        self.location = []

        self.color = [[255, 255, 0], [255, 0, 255]]
        self.img = cv.imread('field.png', cv.IMREAD_COLOR)
        for j in range(4):
            for i in range(100, self.height(), int(self.height() / 5)):
                cv.circle(self.img, (100, i), 5, self.color[0], -1)
            for i in range(100, self.height(), int(self.height() / 5)):
                cv.circle(self.img, (1050, i), 5, self.color[1], -1)
        cv.imwrite('field.png', self.img)

        self.photo_label = QLabel()
        self.photo_label.setPixmap(QPixmap('field.png'))
        self.photo_label.resize(self.img.shape[0], self.img.shape[1])
        # self.photo_label.mousePressEvent = self.click_event

        all_layout = QHBoxLayout()
        all_layout.addLayout(btn_layout_1)
        all_layout.addWidget(self.photo_label)
        all_layout.addLayout(btn_layout_2)

        self.setLayout(all_layout)

    def window_open(self, agent, player, button):
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
            newitem = QTableWidgetItem(str(data[key]))
            tableWidget.setItem(0, n, newitem)
        tableWidget.setHorizontalHeaderLabels(horHeaders)

        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        btn_move = QPushButton("일반 이동(1AP 소모)", self)		
        btn_move.resize(150,50)
        btn_move.clicked.connect(lambda :self.action(agent, 0, dialog, button))

        btn_shoot = QPushButton("사격(1AP 소모)", self)		
        btn_shoot.resize(150,50)
        btn_shoot.clicked.connect(lambda :self.action(agent, 1, dialog, button))	

        btn_fight = QPushButton("전투(1AP 소모)", self)		
        btn_fight.resize(150,50)
        btn_fight.clicked.connect(lambda :self.action(agent, 2, dialog, button))	

        btn_no_action = QPushButton("수행 안함(순서 넘어감)", self)		
        btn_no_action.resize(150,50)
        btn_no_action.clicked.connect(lambda :self.action(agent, 3, dialog, button))	
            
        if self.agent_selected == agent:
            text_lbl = QLabel("액션을 선택하세요")
        elif agent.action_available == False:
            text_lbl = QLabel("액션을 이미 수행하였습니다.")
            btn_move.setEnabled(False)
            btn_shoot.setEnabled(False)
            btn_fight.setEnabled(False)
            btn_no_action.setEnabled(False)
        elif player.turn == True and self.agent_selected == None:
            text_lbl = QLabel("액션을 수행하면 타 요원으로 바꿀 수 없습니다")
        else:
            btn_move.setEnabled(False)
            btn_shoot.setEnabled(False)
            btn_fight.setEnabled(False)
            btn_no_action.setEnabled(False)
            if player.turn == False:
                text_lbl = QLabel("현재 차례가 아닙니다")
            elif self.agent_selected != agent:
                text_lbl = QLabel("선택된 요원이 아닙니다")

        layout = QVBoxLayout()
        dialog.setLayout(layout)
        layout.addWidget(tableWidget)
        layout.addWidget(text_lbl)
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

    def action(self, agent, i, dialog, button):
        if not self.agent_selected:
            self.agent_selected = agent
            button.setStyleSheet("QPushButton{"
                                    "color: rgb(58, 134, 255);"
                                    "background-color: white;"
                                    "border: 2px solid rgb(58, 134, 255);"
                                "}")
            
        
        dialog.close()
            
        if i == 3:
            agent.ap = agent.apl
            self.agent_selected = None
            agent.action_available = False
            button.setStyleSheet("")
            if self.p1.turn == True:
                self.p1.turn = False
                self.p2.turn = True
                self.txtLbl1.setText("")
                self.txtLbl2.setText("현 차례")
            else:
                self.p1.turn = True
                self.p2.turn = False
                self.txtLbl2.setText("")
                self.txtLbl1.setText("현 차례")
        else:      
            if i == 0:
                self.flag = "move"
            elif i == 1:
                self.flag = "shoot"
            else:
                self.flag = "fight"

            if agent.ap == 1:
                agent.ap = agent.apl
                self.agent_selected = None
                agent.action_available = False
                button.setStyleSheet("")
                if self.p1.turn == True:
                    self.p1.turn = False
                    self.p2.turn = True
                    self.txtLbl1.setText("")
                    self.txtLbl2.setText("현 차례")
                else:
                    self.p1.turn = True
                    self.p2.turn = False
                    self.txtLbl2.setText("")
                    self.txtLbl1.setText("현 차례") 
            else:
                agent.ap -= 1
            

    
    """def CloseEvent(self, event):
        for i in reversed(range(dialog.layout().count())): 
            dialog.layout().itemAt(i).widget().setParent(None)

    def window_close(self):
        dialog.close()"""

    def click_event_test(self, event):
        self.x1 = event.pos().x()
        self.y1 = event.pos().y() - 62

        # print("Hello, x: %3d, y: %3d" %(self.x1, self.y1))

    def click_event(self, event):
        if self.count % 2 == 0:
            self.x1 = event.pos().x()
            self.y1 = event.pos().y() - 62

            i = self.color_check(self.x1, self.y1)
            self.unit_num = None
            if i != None:
                self.unit_num = i[0]
                self.unit_color = i[1]
                self.draw_circle(agent = self.location[self.unit_num])
            if self.unit_num == None:
                self.count -= 1

            print("Hello, x: %3d, y: %3d" %(self.x1, self.y1))

        else:
            x2 = event.pos().x()
            y2 = event.pos().y() - 62

            print("Hello, x: %3d, y: %3d" %(x2, y2))

            self.target_range(self.x1, self.y1, x2, y2, 3)
        
        self.count += 1

    def draw_circle(self, dis = 3*INCH, agent=''):
        cv.circle(self.img, (agent.pos_x, agent.pos_y), dis * INCH, (255, 255, 255))
        cv.imwrite('field.png', self.img)
        self.photo_label.setPixmap(QPixmap('field.png'))

    def color_check(self, x1, y1):
        result = 0
        j = 0
        distance = INFINITE
        if (self.img[y1][x1] == [0, 0, 0]).all():
            return None
        else:
            for i in range(len(self.location)):
                print(self.location[i].pos_x, self.location[i].pos_y)
                if (self.img[y1][x1] == self.color[0]).all():
                    j = 0
                else:
                    j = 1
                if dist((x1, y1), (self.location[i].pos_x, self.location[i].pos_y)) < distance:
                    distance = dist((x1, y1), (self.location[i].pos_x, self.location[i].pos_y))
                    print(self.location[i].pos_x, self.location[i].pos_y)
                    result = i
            return [result, j]

    def target_range_test(self, range = 3, agent = ''):
        self.draw_circle(agent.m, agent)
        self.photo_label.mousePressEvent = self.click_event_test
        print(self.x1, self.y1)
        if dist((agent.pos_x, agent.pos_y), (self.x1, self.y1)) > range*INCH:
            cv.circle(self.img, (agent.pos_x, agent.pos_y), range*INCH, (0, 0, 0))
            cv.imwrite('field.png', self.img)
            self.photo_label.setPixmap(QPixmap('field.png'))
        else:
            station = [agent.pos_x, agent.pos_y]
            agent.pos_x = self.x1
            agent.pos_y = self.y1
            cv.circle(self.img, (station[0], station[1]), 5, (0, 0, 0), -1)
            cv.circle(self.img, (station[0], station[1]), range*INCH, (0, 0, 0))
            cv.circle(self.img, (self.x1, self.y1), 5, (255, 255, 0), -1)
            cv.imwrite('field.png', self.img)
            self.photo_label.setPixmap(QPixmap('field.png'))

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
            station = self.location[self.unit_num]
            cv.circle(self.img, (station[0], station[1]), 3*INCH, (0, 0, 0))
            cv.imwrite('field.png', self.img)
            self.photo_label.setPixmap(QPixmap('field.png'))
            print("넘음")
        else:
            station = [self.location[self.unit_num].pos_x, self.location[self.unit_num].pos_y]
            self.location[self.unit_num].pos_x = x2
            self.location[self.unit_num].pos_y = y2
            cv.circle(self.img, (station[0], station[1]), 5, (0, 0, 0), -1)
            cv.circle(self.img, (station[0], station[1]), 3*INCH, (0, 0, 0))
            cv.circle(self.img, (x2, y2), 5, self.color[self.unit_color], -1)
            cv.imwrite('field.png', self.img)
            self.photo_label.setPixmap(QPixmap('field.png'))
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

