import os 
import pygame
from Player import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

p1 = Player()
p2 = Player()

p1.select_kt("Imperial Guard")
p2.select_kt("Space Marine")

p1.select_ft1("Guardsman")
p1.select_ft2("Tempestus Scion")

p2.select_ft1("Intercessor")
p2.select_ft2("Incursor")

p1.ft1.create_agent("Trooper")
p1.ft1.agents[0].set_stats(3,2,2,3,5,7)
p2.ft1.create_agent("Warrior")
p2.ft1.agents[0].set_stats(3,3,1,3,3,13)

p1.ft1.display_agents()
p2.ft1.display_agents()



