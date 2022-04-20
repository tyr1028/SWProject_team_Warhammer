class Player:
    def __init__(self):
        self.cp = 0 # 플로이 사용에 시작되는 cp

    def select_kt(self, kt):
        self.kt = Killteam(kt) 

    def select_ft1(self, ft):
        self.ft1 = Fireteam(ft)

    def select_ft2(self, ft):
        self.ft2 = Fireteam(ft)

class Killteam:
    def __init__(self, kt):
        self.type = kt # 킬팀 종류

class Fireteam:
    def __init__(self, ft):
        self.ft_type = ft
        self.agents = []

    def set_archetypes(self, archetypes): # 파이어팀 당 아키타입 (추후에 Fireteam.csv에서 자동으로 가져오도록 변경 예정)
        self.archetypes = archetypes

    def set_agent_limit(self, limit): # 파이어팀 당 선택할 수 있는 요원 제한 (추후에 Fireteam.csv에서 자동으로 가져오도록 변경 예정/csv파일에 조건 추가 작성 필요)
        self.agent_limit = limit

    def create_agent(self, agent_type): # Agent 객체 생성후 Fireteam의 agents(리스트) 속성에 append 시킴 (GUI 구현 시 리스트박스에서 선택하게 하거나 객체 인식으로 조건에 맞을 경우 추가)
        agent = Agent(agent_type)
        self.agents.append(agent)

    def display_agents(self): # agents 리스트에 존재하는 요원들 전부 표시
        for agent in self.agents:
            print(agent)

class Agent:
    def __init__(self, type):
        self.type = type
        self.pos_x = 0
        self.pos_y = 0
        self.isAlive = True
        self.weapons = []

    def __str__(self):
        return str(self.type, ", ", self.m, ", ", self.apl, ", ", self.ga, ", ", self.df, ", ", self.sv, ", ", self.w)

    def set_stats(self, m, apl, ga, df, sv, w):
        self.m = m
        self.apl = apl
        self.ap = apl
        self.ga = ga
        self.df = df
        self.sv = sv
        self.w = w

