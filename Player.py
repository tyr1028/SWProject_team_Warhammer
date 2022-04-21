from Dice import *

def select_agent(player):
    agent_list = []

    for agent in player.ft1.agents:
        agent_list.append(agent)
    """for agent in player.ft2.agents:
        target_list.append(agent)"""

    for i in range(len(agent_list)):
        result = "%2d: "%i + agent_list[i].type
        print(result, end = " ")
    print()

    print("위 요원 중 선택: ", end="")
    selected_agent = int(input())

    print(agent_list[selected_agent].type + " 선택")
    return agent_list[selected_agent]


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
        self.agents = [] # 파이어팀에 속해있는 요원 리스트

    def set_archetypes(self, archetypes): # 파이어팀 당 아키타입 (추후에 Fireteam.csv에서 자동으로 가져오도록 변경 예정)
        self.archetypes = archetypes

    def set_agent_limit(self, limit): # 파이어팀 당 선택할 수 있는 요원 제한 (추후에 Fireteam.csv에서 자동으로 가져오도록 변경 예정/csv파일에 조건 추가 작성 필요)
        self.agent_limit = limit

    def create_agent(self, agent_type): # Agent 객체 생성후 Fireteam의 agents(리스트) 속성에 append 시킴 (GUI 구현 시 리스트박스에서 선택하게 하거나 객체 인식으로 조건에 맞을 경우 추가)
        agent = Agent(agent_type)
        self.agents.append(agent)

    def display_agents(self, player_name): # agents 리스트에 존재하는 요원들 전부 표시 
        print(player_name, "의 요원")
        for agent in self.agents:
            print(agent)

            print(agent.type + "의 무기들") # 요원들이 각자 가지고 있는 무기도 표시
            for weapon in agent.weapons:
                print(weapon)

        print("_______________________________")

class Agent:
    def __init__(self, type):
        self.type = type
        self.pos_x = 0
        self.pos_y = 0
        self.isAlive = True # 요원의 생존 여부
        self.weapons = [] # 요원이 장비하고 있는 무기 리스트 

    def __str__(self):
        return (self.type + " - m:%2d, apl:%2d, ga:%2d, df:%2d, sv:%2d+, w:%2d" %(self.m, self.apl, self.ga, self.df, self.sv, self.w))

    def set_stats(self, m, apl, ga, df, sv, w):
        self.m, self.apl, self.ga, self.df, self.sv = m, apl, ga, df, sv # 변동 없는 스탯들
        self.ap, self.w = apl, w # 변동 될 수 있는 스탯들 (ap는 firefight 페이즈 동안 사용가능한 ap표시, w는 체력이다보니 공격받으면 내려감)

    def create_weapon(self, weapon_name, type): # Weapon 객체 생성후 Agent의 weapons(리스트) 속성에 append 시킴 
        weapon = Weapon(weapon_name, type)
        self.weapons.append(weapon)

    def display_weapons(self, weapons): # weapons 리스트에 존재하는 무기들 전부 표시
        print(self.type, "의 무기들")
        for weapon in self.weapons:
            print(weapon)

    def select_weapon(self, weapon_type): # 사격 혹은 격투 시 무기 선택(사격/격투 무기타입: Ranged/Melee)
        weapon_list = []
        for weapon in self.weapons:
            if weapon.type == weapon_type:
                weapon_list.append(weapon)

        # 현재는 무기리스트를 출력해줘서 선택 입력받는 형식인데 GUI구현하면 리스트박스에서 선택하도록 수정할 예정 
        for i in range(len(weapon_list)):
            result = "%2d: "%i + weapon_list[i].weapon_name
            print(result, end = " ")
        print()

        print("위 무기 중 선택: ", end="")
        selected_weapon = int(input())

        print(weapon_list[selected_weapon].weapon_name + " 선택")
        return weapon_list[selected_weapon]
    ################################# Firefight 페이즈에서 선택할 수 있는 요원의 Action 관련 #################################
    def move(self): # 일반이동 (소모 ap 아직 구현 안 함)
        pass

    def shoot(self, opponent): # 사격 (소모 ap 아직 구현 안 함)
        target = select_agent(opponent) # 상대 player로부터 공격 대상 선택
        weapon = self.select_weapon("Ranged") # Ranged 타입 무기 선택

        dice_result = dice(weapon.a) # 선택한 무기의 a스탯만큼 주사위 굴림

        hit, hit_crit, miss = 0, 0, 0
        for i in dice_result:
            if i == 6:                # 주사위 6나올 경우 치명타
                hit_crit += 1
            elif i >= weapon.ws:      # 무기의 ws 수치보다 높을 경우 일반 히트
                hit += 1
            else:
                miss += 1
        print("타격성공: %2d(평타: %2d, 치명타: %2d), 타격실패: %2d" %(hit+hit_crit, hit, hit_crit, miss))

        dice_result = dice(target.df) # 수비하는 요원의 df수치 만큼 주사위 굴림

        save, save_crit, wound = 0, 0, 0
        for i in dice_result:
            if i == 6:
                save_crit += 1        # 주사위 6나올 경우 크리티컬 수비
            elif i >= target.sv:
                save += 1             # 요원의 sv 수치보다 높을 경우 일반 수비
            else:
                wound += 1
        print("수비성공: %2d(일반수비: %2d, 치명수비: %2d), 수비실패: %2d" %(save+save_crit, save, save_crit, wound))

        if save_crit > 0:          
            if save_crit <= hit_crit:   
                hit_crit -= save_crit
                save_crit = 0
            else:
                save += save_crit - hit_crit
                save_crit, hit_crit = 0, 0
        if (hit_crit*2+hit) <= save:
            print("수비 포인트가 같거나 더 많아서 공격이 상쇄됐습니다.")
        else:
            total_damage = 0
            while save >= 2 and hit_crit > 0:
                print("일반수비 2개를 소모하여 치명타 1개를 상쇄(y/n): ", end ="")
                user_input = input()
                if user_input == "y":
                    hit_crit -= 1
                    save -= 2
                else:
                    break
            if save >= hit:
                hit = 0
            else: 
                hit -= save
                save = 0
            total_damage += hit_crit*weapon.d_crit
            total_damage += hit*weapon.d

            print("데미지: %2d" %total_damage)

            if total_damage >= target.w:
                target.w = 0
                target.isAlive = False
                print("처치되었습니다")
            else:
                target.w -= total_damage
                print("%2d만큼의 데미지를 받아 체력이 %2d 만큼 남았습니다" %(total_damage, target.w))

class Weapon:
    def __init__(self, weapon_name, type, variant = "default"):
        self.weapon_name = weapon_name
        self.type = type
        self.variant = variant

    def __str__(self):
        return ("  " + self.weapon_name + " - " + self.type + " - a:%2d, bs/ws:%2d+, d:%2d, d_crit:%2d" %(self.a, self.ws, self.d, self.d_crit))

    def set_stats(self, a, ws, d, d_crit):
        self.a = a
        self.ws = ws
        self.d = d                  # 일반 데미지
        self.d_crit = d_crit        # 치명타(주사위에서 6나올 경우)시 데미지
