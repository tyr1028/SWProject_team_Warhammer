from Player import *

class firefightPhase:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def start(self):
        p1_agent_count = len(self.p1.ft1.agents)
        p2_agent_count = len(self.p2.ft1.agents)

    def select_action(self):
        print("액션: ")
        action = input()
        
        if action == "move":
            self.move()
        elif action == "shoot":
            self.shoot()
