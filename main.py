import os 
from Player import *
from TurningPoint import *
from GUI_ver2 import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

p1 = Player()
p2 = Player()
ffp = firefightPhase(p1,p2)
ffp.start()

app = QApplication(sys.argv)
gui = App(p1, p2)
gui.show()
app.exec_()
img = cv.imread('field.png', cv.IMREAD_COLOR)
img = np.zeros((img.shape))
cv.imwrite('field.png', img)

'''p1.ft1.agents[0].shoot(p2)
p2.ft2.agents[0].fight(p1)'''