from asyncio.windows_events import INFINITE

import os 
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2 as cv

from matplotlib.pyplot import table

import numpy as np
from math import *
from yolo import detect
import time
from tkinter import *
from tkinter import filedialog

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INCH = 35

class App(QWidget):
    def __init__(self, p1 = "", p2 = ""):
        super().__init__()
        file_name = self.file_open()
        self.weapon1 = ""
        self.weapon2 = ""
        self.p1 = p1
        self.p2 = p2
        self.agent_selected = None
        self.flag = None

        rate_x = 1152/4032
        rate_y = 648/3024

        self.location_file = open('exp/labels/' + file_name.replace('.jpg', '.txt'), 'r')
        cnt_0 = 0
        cnt_1 = 0

        self.color = [[255, 255, 0], [255, 0, 255]]

        while(True):
            line = self.location_file.readline().replace('\n', '').split(' ')
            if line[0] == '0':
                self.p1.ft1.agents[cnt_0].pos_x = int((int(line[1]) + int(line[3]))/2 * rate_x)
                self.p1.ft1.agents[cnt_0].pos_y =int((int(line[2]) + int(line[4]))/2 * rate_y)
                self.p1.ft1.agents[cnt_0].color = self.color[0]
                cnt_0 += 1
            elif line[0] == '1':
                self.p2.ft1.agents[cnt_1].pos_x = int((int(line[1]) + int(line[3]))/2 * rate_x)
                self.p2.ft1.agents[cnt_1].pos_y = int((int(line[2]) + int(line[4]))/2 * rate_y)
                self.p2.ft1.agents[cnt_1].color = self.color[1]
                cnt_1 += 1

            if cnt_0 == 4 and cnt_1 == 4:
                break
            # self.p1.ft1.agents[j].pos_x = 100
            # self.p1.ft1.agents[j].pos_y = 100 + j * int(self.height() / 5)
            # self.p1.ft1.agents[j].color = self.color[0]
            # self.p2.ft1.agents[j].pos_x = 1050
            # self.p2.ft1.agents[j].pos_y = 100 + j * int(self.height() / 5)
            # self.p2.ft1.agents[j].color = self.color[1]

        self.count = 0
        self.x1 = 0
        self.y1 = 0

        self.initUI()

        #print("m: %2d, apl: %2d, ga: %2d, df: %2d, sv: %2d, w: %2d" %(self.p1.ft1.agents[0].m, self.p1.ft1.agents[0].apl, self.p1.ft1.agents[0].ga, self.p1.ft1.agents[0].df, self.p1.ft1.agents[0].sv, self.p1.ft1.agents[0].w))

    def initUI(self):
        # ??????
        self.setWindowTitle('Warhammer Assistance Program')
        # self.center()
        self.resize(1500, 800)   

         # 1
        self.txtLbl1 = QPushButton("??? ??????", self)
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

        self.img = cv.imread('field.png', cv.IMREAD_COLOR)
        for j in range(4):
            cv.circle(self.img, (self.p1.ft1.agents[j].pos_x, self.p1.ft1.agents[j].pos_y), 8, self.p1.ft1.agents[j].color, -1)
            cv.circle(self.img, (self.p2.ft1.agents[j].pos_x, self.p2.ft1.agents[j].pos_y), 8, self.p2.ft1.agents[j].color, -1)
        cv.imwrite('field.png', self.img)

        self.photo_label = QLabel()
        self.photo_label.setPixmap(QPixmap('field.png'))
        self.photo_label.resize(self.img.shape[0], self.img.shape[1])
        self.photo_label.mousePressEvent = self.click_event

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
        

        # ?????????
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
        tableWidget.setMaximumHeight(70)

        btn_move = QPushButton("?????? ??????(1AP ??????)", self)		
        btn_move.resize(150,50)
        btn_move.clicked.connect(lambda :self.action(agent, 0, dialog, button))

        btn_shoot = QPushButton("??????(1AP ??????)", self)		
        btn_shoot.resize(150,50)
        btn_shoot.clicked.connect(lambda :self.action(agent, 1, dialog, button))	

        btn_fight = QPushButton("??????(1AP ??????)", self)		
        btn_fight.resize(150,50)
        btn_fight.clicked.connect(lambda :self.action(agent, 2, dialog, button))	

        btn_no_action = QPushButton("?????? ??????(?????? ?????????)", self)		
        btn_no_action.resize(150,50)
        btn_no_action.clicked.connect(lambda :self.action(agent, 3, dialog, button))	
            
        if self.agent_selected == agent:
            if self.flag != None:
                text_lbl = QLabel("???????????? ????????? ????????????.")
                btn_move.setEnabled(False)
                btn_shoot.setEnabled(False)
                btn_fight.setEnabled(False)
                btn_no_action.setEnabled(False)
            else:
                text_lbl = QLabel("????????? ???????????????")
        elif agent.action_available == False:
            text_lbl = QLabel("????????? ?????? ?????????????????????.")
            btn_move.setEnabled(False)
            btn_shoot.setEnabled(False)
            btn_fight.setEnabled(False)
            btn_no_action.setEnabled(False)
        elif player.turn == True and self.agent_selected == None:
            text_lbl = QLabel("????????? ???????????? ??? ???????????? ?????? ??? ????????????")
        else:
            btn_move.setEnabled(False)
            btn_shoot.setEnabled(False)
            btn_fight.setEnabled(False)
            btn_no_action.setEnabled(False)
            if player.turn == False:
                text_lbl = QLabel("?????? ????????? ????????????")
            elif self.agent_selected != agent:
                text_lbl = QLabel("????????? ????????? ????????????")

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


        dialog.setWindowTitle("agent information")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(500, 250)
        #dialog.closeEvent = self.CloseEvent
        dialog.exec()

    def action(self, agent, i, dialog, button):
        if not self.agent_selected:
            self.agent_selected = agent
            self.activate_button = button
            self.activate_button.setStyleSheet("QPushButton{"
                                    "color: rgb(58, 134, 255);"
                                    "background-color: white;"
                                    "border: 2px solid rgb(58, 134, 255);"
                                "}")
            
        
        dialog.close()
            
        if i == 3:
            #agent.ap = agent.apl
            agent.ap = 0
            self.agent_selected = None
            agent.action_available = False
            self.activate_button.setStyleSheet("")
            if self.p1.turn == True:
                self.p1.turn = False
                self.p2.turn = True
                self.txtLbl1.setText("")
                self.txtLbl2.setText("??? ??????")
            else:
                self.p1.turn = True
                self.p2.turn = False
                self.txtLbl2.setText("")
                self.txtLbl1.setText("??? ??????")
        else:      
            if i == 0:
                self.flag = "move"
                self.draw_circle(agent.m, agent)
            elif i == 1:
                self.flag = "shoot"
                dialog = WeaponDialog("Ranged", agent, self)
            else:
                self.flag = "fight"

            if agent.ap == 1:
                #agent.ap = agent.apl
                agent.ap = 0
                agent.action_available = False
                self.activate_button.setStyleSheet("")

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
        if self.flag == None:
            self.x1 = event.pos().x()
            self.y1 = event.pos().y() - 62

            print("Hello, x: %3d, y: %3d" %(self.x1, self.y1))
            """i = self.color_check(self.x1, self.y1)
            self.unit_num = None
            if i != None:
                self.unit_num = i[0]
                self.unit_color = i[1]"""
        else:
            if self.flag == "move":
                agent = self.agent_selected
                self.x1 = event.pos().x()
                self.y1 = event.pos().y() - 62

                if agent.ap == 0:
                    self.agent_selected = None

                self.target_range_test(agent)
                if dist((agent.pos_x, agent.pos_y), (self.x1, self.y1)) < agent.m*INCH:
                    agent.pos_x = self.x1
                    agent.pos_y = self.y1
                else:
                    agent.action_available = True
                    agent.ap += 1
                    self.agent_selected = agent
                    self.activate_button.setStyleSheet("QPushButton{"
                                    "color: rgb(58, 134, 255);"
                                    "background-color: white;"
                                    "border: 2px solid rgb(58, 134, 255);"
                                "}")
                
                self.flag = None
            
            elif self.flag == "shoot":
                agent = self.agent_selected
                self.x1 = event.pos().x()
                self.y1 = event.pos().y() - 62
                if (self.img[self.y1][self.x1] != agent.color).any() and ((self.img[self.y1][self.x1] == self.color[0]).all() or (self.img[self.y1][self.x1] == self.color[1]).all()):
                    distance = INFINITE
                    enemy = ''
                    if self.p1.turn:
                        for i in self.p2.ft1.agents:
                            if distance > dist((i.pos_x, i.pos_y), (self.x1, self.y1)):
                                enemy = i
                                distance = dist((i.pos_x, i.pos_y), (self.x1, self.y1))
                    elif self.p2.turn:
                        for i in self.p1.ft1.agents:
                            if distance > dist((i.pos_x, i.pos_y), (self.x1, self.y1)):
                                enemy = i
                                distance = dist((i.pos_x, i.pos_y), (self.x1, self.y1))
                    print('shoot')
                    result = agent.shoot(enemy, self.weapon1)
                    s_dialog = ShootDialog(result, enemy)
                    

                    if agent.ap == 0:
                        self.agent_selected = None

                else:
                    agent.action_available = True
                    agent.ap += 1
                    self.agent_selected = agent
                    self.activate_button.setStyleSheet("QPushButton{"
                                    "color: rgb(58, 134, 255);"
                                    "background-color: white;"
                                    "border: 2px solid rgb(58, 134, 255);"
                                "}")

                self.flag = None

            elif self.flag == "fight":
                agent = self.agent_selected
                self.x1 = event.pos().x()
                self.y1 = event.pos().y() - 62

                if (self.img[self.y1][self.x1] != agent.color).any() and ((self.img[self.y1][self.x1] == self.color[0]).all() or (self.img[self.y1][self.x1] == self.color[1]).all()):
                    distance = INFINITE
                    enemy = ''
                    if self.p1.turn:
                        for i in self.p2.ft1.agents:
                            if distance > dist((i.pos_x, i.pos_y), (self.x1, self.y1)):
                                enemy = i
                                distance = dist((i.pos_x, i.pos_y), (self.x1, self.y1))
                    if self.p2.turn:
                        for i in self.p1.ft1.agents:
                            if distance > dist((i.pos_x, i.pos_y), (self.x1, self.y1)):
                                enemy = i
                                distance = dist((i.pos_x, i.pos_y), (self.x1, self.y1))

                    if dist((agent.pos_x, agent.pos_y), (enemy.pos_x, enemy.pos_y)) <= INCH:
                        agent.fight(enemy)
                        if agent.ap == 0:
                            self.agent_selected = None
                    else:
                        agent.action_available = True
                        agent.ap += 1
                        self.agent_selected = agent
                        self.activate_button.setStyleSheet("QPushButton{"
                                        "color: rgb(58, 134, 255);"
                                        "background-color: white;"
                                        "border: 2px solid rgb(58, 134, 255);"
                                    "}")

                else:
                    agent.action_available = True
                    agent.ap += 1
                    self.agent_selected = agent
                    self.activate_button.setStyleSheet("QPushButton{"
                                    "color: rgb(58, 134, 255);"
                                    "background-color: white;"
                                    "border: 2px solid rgb(58, 134, 255);"
                                "}")

                self.flag = None

            if agent.ap == 0:
                if self.p1.turn == True:
                    self.p1.turn = False
                    self.p2.turn = True
                    self.txtLbl1.setText("")
                    self.txtLbl2.setText("??? ??????")
                else:
                    self.p1.turn = True
                    self.p2.turn = False
                    self.txtLbl2.setText("")
                    self.txtLbl1.setText("??? ??????") 

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

    def target_range_test(self, agent = ''):
        if dist((agent.pos_x, agent.pos_y), (self.x1, self.y1)) > agent.m*INCH:
            cv.circle(self.img, (agent.pos_x, agent.pos_y), agent.m*INCH, (0, 0, 0))
            cv.imwrite('field.png', self.img)
            self.photo_label.setPixmap(QPixmap('field.png'))
        else:
            cv.circle(self.img, (agent.pos_x, agent.pos_y), 8, (0, 0, 0), -1)
            cv.circle(self.img, (agent.pos_x, agent.pos_y), agent.m*INCH, (0, 0, 0))
            cv.circle(self.img, (self.x1, self.y1), 8, agent.color, -1)
            cv.imwrite('field.png', self.img)
            self.photo_label.setPixmap(QPixmap('field.png'))
            agent.pos_x = self.x1
            agent.pos_y = self.y1

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
            print("??????")
        else:
            station = [self.location[self.unit_num].pos_x, self.location[self.unit_num].pos_y]
            self.location[self.unit_num].pos_x = x2
            self.location[self.unit_num].pos_y = y2
            cv.circle(self.img, (station[0], station[1]), 5, (0, 0, 0), -1)
            cv.circle(self.img, (station[0], station[1]), 3*INCH, (0, 0, 0))
            cv.circle(self.img, (x2, y2), 5, self.color[self.unit_color], -1)
            cv.imwrite('field.png', self.img)
            self.photo_label.setPixmap(QPixmap('field.png'))
            print("??????")
        

    def agent_select_test(self, x, y):
        '''for agent in self.p1.ft1.agents:
            if agent.'''
        pass

    def file_open(self):
        root = Tk()
        title = 'open image'
        root.filename = filedialog.askopenfilename(initialdir='', title=title, filetypes=(
        ('png files', '*.png'), ('jpg files', '*.jpg'), ('all files', '*.*')))
        detect.run(weights='yolo/best.pt', source=root.filename, save_txt=True, nosave=True, conf_thres = 0.8, project='')
        root.destroy()
        return root.filename.split('/')[-1]

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class ShootDialog(QDialog):
    def __init__(self, result, agent):
        super().__init__()
        self.setWindowTitle("Second window")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(500, 250)
        #self.closeEvent = self.CloseEvent

        # ?????????
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
        tableWidget.setMaximumHeight(70)

        layout = QVBoxLayout()
        layout.addWidget(tableWidget)
        for text in result:
            txtLbl = QLabel()
            txtLbl.setText(text)
            layout.addWidget(txtLbl)

        self.setLayout(layout)
    
        self.exec()
        

class WeaponDialog(QDialog):
    def __init__(self, weapon_type, agent, app):
        super().__init__()
        self.setWindowTitle("Second window")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(500, 500)
        #self.closeEvent = self.CloseEvent

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)

        weapon_list = []
        verHeaders = []
        self.data = {'a':[], 'ws':[], 'd':[], 'd_crit':[]}
        for weapon in agent.weapons:
            if weapon.type == weapon_type:
                weapon_list.append(weapon)
                verHeaders.append(weapon.weapon_name)
        self.tableWidget.setRowCount(len(weapon_list))
        for weapon in weapon_list:
            self.data["a"].append(weapon.a)
            self.data["ws"].append(weapon.ws)
            self.data["d"].append(weapon.d)
            self.data["d_crit"].append(weapon.d_crit)
        self.tableWidget.setVerticalHeaderLabels(verHeaders)
            
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(str(item))
                self.tableWidget.setItem(m, n, newitem)
                print(str(key) + ", " + str(item) + ", " + str(m) + ", " + str(n))
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)

        
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.tableWidget)

        btn_list = []
        for weapon in weapon_list:
            btn = QPushButton(weapon.weapon_name, self)
            btn_list.append(btn)
            btn.resize(150,50)
            btn.clicked.connect(lambda :self.get_weapon(weapon, app))
            layout.addWidget(btn)

        self.exec()

    def get_weapon(self, weapon, app):
        self.close()
        app.weapon1 = weapon
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exec_()
    img = cv.imread('field.png', cv.IMREAD_COLOR)
    img = np.zeros((img.shape))
    cv.imwrite('field.png', img)

