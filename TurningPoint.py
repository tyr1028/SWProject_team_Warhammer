from Player import *

class firefightPhase:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def start(self):
        self.p1.select_kt("Imperial Guard")
        self.p2.select_kt("Space Marine")

        self.p1.select_ft()
        self.p2.select_ft()

        self.p1.ft1.create_agent("Trooper")
        self.p1.ft1.agents[0].set_stats(3,2,2,3,5,7)
        self.p1.ft1.agents[0].create_weapon("Lasgun", "Ranged")
        self.p1.ft1.agents[0].weapons[0].set_stats(4, 4, 2, 3)
        self.p1.ft1.agents[0].create_weapon("Bayonet", "Melee")
        self.p1.ft1.agents[0].weapons[1].set_stats(3, 4, 2, 3)

        self.p2.ft1.create_agent("Warrior")
        self.p2.ft1.agents[0].set_stats(3,3,1,3,3,13)
        self.p2.ft1.agents[0].create_weapon("Auto bolt rifle", "Ranged")
        self.p2.ft1.agents[0].weapons[0].set_stats(4, 3, 3, 4)
        self.p2.ft1.agents[0].create_weapon("Bolt rifle", "Ranged")
        self.p2.ft1.agents[0].weapons[1].set_stats(4, 3, 3, 4)
        self.p2.ft1.agents[0].create_weapon("Stalker bolt rifle", "Ranged")
        self.p2.ft1.agents[0].weapons[2].set_stats(4, 3, 3, 4)
        self.p2.ft1.agents[0].create_weapon("Fists", "Melee")
        self.p2.ft1.agents[0].weapons[3].set_stats(4, 3, 3, 4)

        self.p2.ft2.create_agent("Sergeant")
        self.p2.ft2.agents[0].set_stats(3,3,1,3,3,13)
        self.p2.ft2.agents[0].set_stats(3,3,1,3,3,13)
        self.p2.ft2.agents[0].create_weapon("Occulus bolt carbine", "Ranged")
        self.p2.ft2.agents[0].weapons[0].set_stats(4, 2, 3, 4)
        self.p2.ft2.agents[0].create_weapon("Combat blade", "Melee")
        self.p2.ft2.agents[0].weapons[1].set_stats(4, 3, 3, 5)


        self.p1.ft1.display_agents("Player 1")
        self.p2.ft1.display_agents("Player 2, Fireteam 1")
        self.p2.ft2.display_agents("Player 2, Fireteam 2")

        p1_agent_count = len(self.p1.ft1.agents)
        p2_agent_count = len(self.p2.ft1.agents)

        for i in range(p1_agent_count+p2_agent_count):
            if i % 2 == 0:
                self.p1.select_action()
                

    def select_action(self):
        print("액션: ")
        action = input()
        
        if action == "move":
            self.move()
        elif action == "shoot":
            self.shoot()
