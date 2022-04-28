import os 
import pygame
from Player import *
from TurningPoint import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

p1 = Player()
p2 = Player()

p1.select_kt("Imperial Guard")
p2.select_kt("Space Marine")

p1.select_ft()
p2.select_ft()

p1.ft1.create_agent("Trooper")
p1.ft1.agents[0].set_stats(3,2,2,3,5,7)
p1.ft1.agents[0].create_weapon("Lasgun", "Ranged")
p1.ft1.agents[0].weapons[0].set_stats(4, 4, 2, 3)
p1.ft1.agents[0].create_weapon("Bayonet", "Melee")
p1.ft1.agents[0].weapons[1].set_stats(3, 4, 2, 3)

p2.ft1.create_agent("Warrior")
p2.ft1.agents[0].set_stats(3,3,1,3,3,13)
p2.ft1.agents[0].create_weapon("Auto bolt rifle", "Ranged")
p2.ft1.agents[0].weapons[0].set_stats(4, 3, 3, 4)
p2.ft1.agents[0].create_weapon("Bolt rifle", "Ranged")
p2.ft1.agents[0].weapons[1].set_stats(4, 3, 3, 4)
p2.ft1.agents[0].create_weapon("Stalker bolt rifle", "Ranged")
p2.ft1.agents[0].weapons[2].set_stats(4, 3, 3, 4)
p2.ft1.agents[0].create_weapon("Fists", "Melee")
p2.ft1.agents[0].weapons[3].set_stats(4, 3, 3, 4)

p2.ft2.create_agent("Sergeant")
p2.ft2.agents[0].set_stats(3,3,1,3,3,13)
p2.ft2.agents[0].set_stats(3,3,1,3,3,13)
p2.ft2.agents[0].create_weapon("Auto bolt rifle", "Ranged")
p2.ft2.agents[0].weapons[0].set_stats(4, 2, 3, 4)
p2.ft2.agents[0].create_weapon("Fists", "Melee")
p2.ft2.agents[0].weapons[1].set_stats(4, 3, 3, 5)


p1.ft1.display_agents("Player 1")
p2.ft1.display_agents("Player 2, Fireteam 1")
p2.ft2.display_agents("Player 2, Fireteam 2")

#p1.ft1.agents[0].shoot(p2)
p2.ft1.agents[0].shoot(p1)