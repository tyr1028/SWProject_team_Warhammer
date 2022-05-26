from Dice import *
import csv

class Player:
    def __init__(self):
        self.cp = 0 # 플로이 사용에 시작되는 cp
        self.turn = False

    def select_kt(self, kt):
        self.kt = Killteam(kt) 

    def select_ft(self):
        ft_list = self.get_ft_csv()
        for i in range(len(ft_list)):
            text = str(i+1) + ": " + ft_list[i][2]
            print(text, end=" ")

        print("\n파이어팀1 선택: ", end ="")
        user_input = int(input())

        selected_ft = ft_list[user_input-1][2]
        ft1_archetypes = ft_list[user_input-1][3:]

        self.select_ft1(selected_ft)

        print("파이어팀2 선택: ", end ="")
        user_input = int(input())

        selected_ft = ft_list[user_input-1][2]
        ft2_archetypes = ft_list[user_input-1][3:]

        self.select_ft2(selected_ft)
        print(selected_ft)

        self.ft1.set_archetypes(ft1_archetypes)
        self.ft2.set_archetypes(ft2_archetypes)

    def select_ft1(self, ft):
        self.ft1 = Fireteam(ft)
        print("선택된 파이어팀: " + self.ft1.ft_type)

    def select_ft2(self, ft):
        self.ft2 = Fireteam(ft)
        print("선택된 파이어팀: " + self.ft2.ft_type)

    def get_ft_csv(self):
        file = open('game_data/fireTeams.csv')
        type(file)
        csvreader = csv.reader(file)

        header = []
        header = next(csvreader)
        header

        rows = []
        for row in csvreader:
                if row[1] == self.kt.type:
                    rows.append(row)

        file.close()

        return rows
    
    def set_turn(self):
        self.turn = True

    def set_turn_false(self):
        self.turn = False

    def select_agent(self):
        agent_list = []

        for agent in self.ft1.agents:
            agent_list.append(agent)
        for agent in self.ft2.agents:
            agent_list.append(agent)

        for i in range(len(agent_list)):
            result = "%2d: "%i + agent_list[i].type
            print(result, end = "  ")
        print()

        print("위 요원 중 선택: ", end="")
        selected_agent = int(input())

        print(agent_list[selected_agent].type + " 선택")
        return agent_list[selected_agent]

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

    def select_action(self):
        print("액션: ")
        action = input()
        
        if action == "move":
            self.move()
        elif action == "shoot":
            self.shoot()
        elif action == "fight":
            self.fight()
    ################################# Firefight 페이즈에서 선택할 수 있는 요원의 Action 관련 #################################
    def move(self, pos_x, pos_y): # 일반이동 (소모 ap 아직 구현 안 함)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def shoot(self, opponent): # 사격 (소모 ap 아직 구현 안 함)
        target = select_agent(opponent) # 상대 player로부터 공격 대상 선택
        weapon = self.select_weapon("Ranged") # Ranged 타입 무기 선택

        dice_result = dice(weapon.a) # 선택한 무기의 a스탯만큼 주사위 굴림

        attacker_normal, attacker_crit, attacker_miss = 0, 0, 0
        for i in dice_result:
            if i == 6:                # 주사위 6나올 경우 치명타
                attacker_crit += 1
            elif i >= weapon.ws:      # 무기의 ws 수치보다 높을 경우 일반 히트
                attacker_normal += 1
            else:
                attacker_miss += 1
        print("타격성공: %2d(평타: %2d, 치명타: %2d), 타격실패: %2d" %(attacker_normal+attacker_crit, attacker_normal, attacker_crit, attacker_miss))

        dice_result = dice(target.df) # 수비하는 요원의 df수치 만큼 주사위 굴림

        defender_normal, defender_crit, defender_attacker_miss = 0, 0, 0
        for i in dice_result:
            if i == 6:
                defender_crit += 1        # 주사위 6나올 경우 크리티컬 수비
            elif i >= target.sv:
                defender_normal += 1             # 요원의 sv 수치보다 높을 경우 일반 수비
            else:
                defender_attacker_miss += 1
        print("수비성공: %2d(일반수비: %2d, 치명수비: %2d), 수비실패: %2d" %(defender_normal+defender_crit, defender_normal, defender_crit, defender_attacker_miss))

        if defender_crit > 0: 
            if defender_crit <= attacker_crit:   
                attacker_crit -= defender_crit
                defender_crit = 0
            else:
                defender_normal += defender_crit - attacker_crit
                defender_crit, attacker_crit = 0, 0
        if (attacker_crit*2+attacker_normal) <= defender_normal:
            print("수비 포인트가 같거나 더 많아서 공격이 상쇄됐습니다.")
        else:
            total_damage = 0
            while defender_normal >= 2 and attacker_crit > 0:
                print("일반수비 2개를 소모하여 치명타 1개를 상쇄(y/n): ", end ="")
                user_input = input()
                if user_input == "y":
                    attacker_crit -= 1
                    defender_normal -= 2
                else:
                    break
            if defender_normal >= attacker_normal:
                attacker_normal = 0
            else: 
                attacker_normal -= defender_normal
                defender_normal = 0
            total_damage += attacker_crit*weapon.d_crit
            total_damage += attacker_normal*weapon.d

            # print("데미지: %2d" %total_damage)

            if total_damage >= target.w:
                target.w = 0
                target.isAlive = False
                print("처치되었습니다")
            else:
                target.w -= total_damage
                print("%2d만큼의 데미지를 받아 체력이 %2d 만큼 남았습니다" %(total_damage, target.w))

    def fight(self, opponent):
        target = select_agent(opponent) # 상대 player로부터 공격 대상 선택
        attacker_weapon = self.select_weapon("Melee") # 공격자 Melee 타입 무기 선택
        defender_weapon = target.select_weapon("Melee") # 수비자 Melee 타입 무기 선택

        dice_result = dice(attacker_weapon.a) # 선택한 무기의 a스탯만큼 주사위 굴림

        attacker_normal, attacker_crit, attacker_miss = 0, 0, 0
        for i in dice_result:
            if i == 6:                # 주사위 6나올 경우 치명타
                attacker_crit += 1
            elif i >= attacker_weapon.ws:      # 공격자 무기의 ws 수치보다 높을 경우 일반 히트
                attacker_normal += 1
            else:
                attacker_miss += 1
        print("공격자 공격성공: %2d(일반공격: %2d, 치명공격: %2d), 공격실패: %2d" %(attacker_normal+attacker_crit, attacker_normal, attacker_crit, attacker_miss))

        dice_result = dice(target.df) # 수비하는 요원의 df수치 만큼 주사위 굴림

        defender_normal, defender_crit, defender_attacker_miss = 0, 0, 0
        for i in dice_result:
            if i == 6:
                defender_crit += 1        # 주사위 6나올 경우 크리티컬 수비
            elif i >= defender_weapon.ws:
                defender_normal += 1             # 수비자 무기의 ws 수치보다 높을 경우 일반 수비
            else:
                defender_attacker_miss += 1
        print("수비성공: %2d(일반수비: %2d, 치명수비: %2d), 수비실패: %2d" %(defender_normal+defender_crit, defender_normal, defender_crit, defender_attacker_miss))

        turn = 0
        
        for i in range(attacker_normal+attacker_crit+defender_normal+defender_crit):
            if (turn%2 == 0 or defender_normal+defender_crit == 0) and not attacker_normal + attacker_crit == 0:
                while True:
                    print("공격자 턴 / 일반주사위(1): %2d, 치명주사위(2): %d 선택: "%(attacker_normal, attacker_crit), end="")
                    dice_choice = int(input())
                    if dice_choice == 1:
                        if attacker_normal == 0:
                            print("사용할 주사위 없음")
                        else:
                            if defender_normal > 0:
                                print("공격(1) 혹은 방어(2) 선택: ",end="")
                                strike_or_parry = int(input())
                            else:
                                print("상대방 일반수비 주사위가 없어 바로 공격 처리")
                                strike_or_parry = 1

                            if strike_or_parry == 1:
                                print("기존 상대 요원 체력 %2d에서 " %target.w, end="")
                                target.w -= attacker_weapon.d
                                print("공격 무기 데미지 %2d만큼 감소되어 상대 요원 체력이 %2d로 바뀜" %(attacker_weapon.d, target.w))
                            elif strike_or_parry == 2:
                                print("기존 수비자 요원 기본주사위 %2d에서 " %defender_normal)
                                defender_normal -= 1
                                print("1만큼 감소 되어 %2d로 바뀜" %defender_normal)
                                i += 1

                            attacker_normal -= 1

                            turn += 1
                            break

                    if dice_choice == 2:
                        if attacker_crit == 0:
                            print("사용할 주사위 없음")
                        else:
                            if defender_normal + defender_crit > 0:
                                print("공격(1) 혹은 방어(2) 선택: ",end="")
                                strike_or_parry = int(input())
                            else:
                                print("상대방 일반수비 주사위가 없어 바로 공격 처리")
                                strike_or_parry = 1

                            if strike_or_parry == 1:
                                print("기존 상대 요원 체력 %2d에서 " %target.w, end="")
                                target.w -= attacker_weapon.d_crit
                                print("공격 무기 치명 데미지 %2d만큼 감소되어 상대 요원 체력이 %2d로 바뀜" %(attacker_weapon.d_crit, target.w))
                            elif strike_or_parry == 2:
                                if defender_crit > 0:
                                    print("기존 수비자 요원 치명주사위 %2d에서 " %defender_crit)
                                    defender_crit -= 1
                                    print("1만큼 감소 되어 %2d로 바뀜" %defender_crit)
                                    i += 1
                                else:
                                    print("기존 수비자 요원 치명주사위 %2d에서 " %defender_normal)
                                    defender_normal -= 1
                                    print("1만큼 감소 되어 %2d로 바뀜" %defender_normal)
                                    i += 1

                            attacker_crit -= 1
                            
                            turn += 1
                            break


            elif (turn%2 == 1 or attacker_normal+attacker_crit == 0) and not defender_normal + defender_crit == 0:
                while True:
                    print("수비자 턴 / 일반주사위(1): %2d, 치명주사위(2): %d 선택: "%(defender_normal, defender_crit), end="")
                    dice_choice = int(input())
                    if dice_choice == 1:
                        if defender_normal == 0:
                            print("사용할 주사위 없음")
                        else:
                            if attacker_normal > 0:
                                print("공격(1) 혹은 방어(2) 선택: ",end="")
                                strike_or_parry = int(input())
                            else:
                                print("상대방 일반수비 주사위가 없어 바로 공격 처리")
                                strike_or_parry == 1

                            if strike_or_parry == 1:
                                print("기존 상대 요원 체력 %2d에서 " %self.w, end="")
                                self.w -= defender_weapon.d
                                print("공격 무기 데미지 %2d만큼 감소되어 상대 요원 체력이 %2d로 바뀜" %(defender_weapon.d, self.w))
                            elif strike_or_parry == 2:
                                print("기존 공격자 요원 기본주사위 %2d에서 " %attacker_normal)
                                attacker_normal -= 1
                                print("1만큼 감소 되어 %2d로 바뀜" %attacker_normal)
                                i += 1

                            defender_normal -= 1

                            turn += 1
                            break

                    if dice_choice == 2:
                        if defender_crit == 0:
                            print("사용할 주사위 없음")
                        else:
                            if attacker_normal + attacker_crit > 0:
                                print("공격(1) 혹은 방어(2) 선택: ",end="")
                                strike_or_parry = int(input())
                            else:
                                print("상대방 일반수비 주사위가 없어 바로 공격 처리")
                                strike_or_parry == 1

                            if strike_or_parry == 1:
                                print("기존 상대 요원 체력 %2d에서 " %self.w, end="")
                                self.w -= defender_weapon.d_crit
                                print("공격 무기 치명 데미지 %2d만큼 감소되어 상대 요원 체력이 %2d로 바뀜" %(defender_weapon.d_crit, self.w))
                            elif strike_or_parry == 2:
                                if attacker_crit > 0:
                                    print("기존 공격자 요원 치명주사위 %2d에서 " %attacker_crit)
                                    attacker_crit -= 1
                                    print("1만큼 감소 되어 %2d로 바뀜" %attacker_crit)
                                    i += 1
                                else:
                                    print("기존 공격자 요원 기본주사위 %2d에서 " %attacker_normal)
                                    attacker_normal -= 1
                                    print("1만큼 감소 되어 %2d로 바뀜" %attacker_normal)
                                    i += 1

                            defender_crit -= 1
                            
                            turn += 1
                            break

            if self.w <= 0:
                print("공격자 요원이 처치됨")
                self.isAlive = False
                break
            if target.w <= 0:
                print("수비자 요원이 처치됨")
                target.isAlive = False
                break
    
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
