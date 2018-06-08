import numpy as np
import matplotlib as plot
from copy import deepcopy
import dqn_gameplay as dqn

dqn_gp = dqn.DQN_gameplay()
class Fight_battle:
    '战场过程'
    step_try_best = 10
    dict_RStatus = {}
    action_base = [[20,-1,-1,-1],[-10,5,-1,-1],[-10,-1,5,-1],[-10,-1,-1,2]]

    #init  
    def __init__(self,dict_role_s):
        self.dict_RStatus = deepcopy(dict_role_s)#self.get_sequenceOfAction()
        self.dict_RStatus_aftAction = dict_role_s
        #self.episode = episode
        #print(self.action_1,self.action_2)
        self.team_win = 0
        self.kta = 0
        self.dead_man = [0,0,0]
        step_for_action = 0
        self.start_step()

    def start_step(self):
        #设定好初始值后，再开始战斗
        #state_reward = []
        for i in range(self.step_try_best):
            #print(self.dict_RStatus)
            #为循环需要再次设定初始值，设定经过动作后的角色属性，也就是状态
            if i >=1:
                #确定动作
                action_1 = self.action_base[dqn_gp.choose_action([1,2,3,4,5,6,7,8,9,10])[0]]
                action_2 = self.action_base[dqn_gp.choose_action([1,2,3,4,5,6,7,8,9,10])[1]]
                print(i,action_1, action_2)
                self.dict_RStatus[1]['hp'] += action_1[0]
                self.dict_RStatus[1]['attack']+= action_1[1]
                self.dict_RStatus[1]['deffence'] += action_1[2]
                self.dict_RStatus[1]['speed'] += action_1[3]
                self.dict_RStatus[7]['hp'] += action_2[0]
                self.dict_RStatus[7]['attack']+= action_2[1]
                self.dict_RStatus[7]['deffence'] += action_2[2]
                self.dict_RStatus[7]['speed'] += action_2[3]
##                    print('次，改属性',RStatus)
            self.team_win = 0
            self.kta = 0
            self.dead_man = [0,0,0]
            self.dict_RStatus_foruse = self.get_sequenceOfAction(self.dict_RStatus)
            state_reward = deepcopy(self.run_battle(self.dict_RStatus_foruse))
            dqn_gp.state_receive[0] = state_reward[0][0];dqn_gp.state_receive[1] = state_reward[0][1];dqn_gp.state_receive[2] = state_reward[0][2];dqn_gp.state_receive[3] = state_reward[0][3]
            dqn_gp.state_receive[4] = state_reward[1][0];dqn_gp.state_receive[5] = state_reward[1][1];dqn_gp.state_receive[6] = state_reward[1][2];dqn_gp.state_receive[7] = state_reward[1][3]
            dqn_gp.state_receive[8] = -state_reward[2][0] - state_reward[2][1] + state_reward[2][2]
            print(dqn_gp.state_receive,'state_reward')

    #更新进行动作后的状态
    def get_s_aftAction(self):
        print(self.dict_RStatus_aftAction)
        return
    
	#角色行动
    def role_fight(self,dict_RStatus_temp):
##        print(dict_RStatus_temp)
        for RStatus in dict_RStatus_temp:
            #print(list(RStatus.values())[0]['army_index'])
            target_1 = 99
            #hp不足0的单位要标记一下target_1
            if list(RStatus.values())[0]['hp'] <= 0:
                target_1 = 100
            #找一个有队伍号且hp大于0的活单位，单位hp不大于0，调整target_1值，不能影响后面角色无法找到目标的判断，并用于判断胜负team
            if list(RStatus.values())[0]['army_index'] == 1 and list(RStatus.values())[0]['hp'] > 0:
                self.team_win = list(RStatus.values())[0]['army_index']
                for role in dict_RStatus_temp:
                    #遍历角色列表寻找有效目标
                    if list(role.values())[0]['army_index'] == 2 and list(role.values())[0]['hp'] > 0:
                        #target_1还是初始值，则表示没有目标
                        if target_1 == 99:
                            #存下潜在目标的字典转列表的索引，print(dict_RStatus_temp.index(role))
                            target_1 = dict_RStatus_temp.index(role)
                            #print(list(dict_RStatus_temp[target_1].values())[0]['position'],list(dict_RStatus_temp[target_1].values())[0]['name'])
                        else:
                            #优先选择position更小更近的目标
                            if list(role.values())[0]['position'] < list(dict_RStatus_temp[target_1].values())[0]['position']:
                                target_1 = dict_RStatus_temp.index(role)
##                                print(print(list(dict_RStatus_temp[target_1].values())[0]['position'],list(dict_RStatus_temp[target_1].values())[0]['name']))
            elif list(RStatus.values())[0]['army_index'] == 2 and list(RStatus.values())[0]['hp'] > 0:
                self.team_win = list(RStatus.values())[0]['army_index']
##                print(list(RStatus.values())[0]['name'])
                for role in dict_RStatus_temp:
                    if list(role.values())[0]['army_index'] == 1 and list(role.values())[0]['hp'] > 0:
                        if target_1 == 99:
                            target_1 = dict_RStatus_temp.index(role)
                        else:
                            if list(role.values())[0]['position'] < list(dict_RStatus_temp[target_1].values())[0]['position']:
                                target_1 = dict_RStatus_temp.index(role)
            
            #有单位还能找到目标
            if target_1 == 100: #一个死单位改的target_1，不用做处理
                pass
            elif target_1 != 99:
                list(dict_RStatus_temp[target_1].values())[0]['hp'] -= max(0,(list(RStatus.values())[0]['attack'] - list(dict_RStatus_temp[target_1].values())[0]['deffence']))
                #print(list(RStatus.values())[0]['name'],'攻击了',list(dict_RStatus_temp[target_1].values())[0]['name'],'造成了：', \(list(RStatus.values())[0]['attack'] - list(dict_RStatus_temp[target_1].values())[0]['deffence']),'伤害', \'剩余hp',list(dict_RStatus_temp[target_1].values())[0]['hp'])                    
                if list(dict_RStatus_temp[target_1].values())[0]['hp'] <= 0:
                    #print(list(dict_RStatus_temp[target_1].values())[0]['name'],"is dead!")
                    self.dead_man[list(dict_RStatus_temp[target_1].values())[0]['army_index']] += 1
            else: #target_1 == 99 活单位找不到目标，表示战斗结束
                pass
        return

    #确定用于战斗的角色及其行动顺序
    def get_sequenceOfAction(self, dict_RStatus):
        dict_role_sequenced = []
        #print(dict_RStatus)
        dict_role_sequenced_temp = sorted(dict_RStatus.items(),
                                     key = lambda x:x[1]['speed'],
                                     reverse = True)
##        print('aaa')
        newkey = 1
        for role in dict_role_sequenced_temp:
            #excel中的空值导入后是str类型，填了数字才是float或int类型
            if role[1]['army_index'] != '':
                dict_role = {newkey:role[1]}
                newkey = newkey +1
                dict_role_sequenced.append(dict_role)
        #print(dict_role_sequenced)
        return dict_role_sequenced

    #进行战斗，模拟时间tick展开
    def run_battle(self, dict_RStatus_sequence):
        #result输出的东西，清空一下
        state_army1_1 = []
        state_army1_2 = []
        hp_army1 = 0
        hp_army2 = 0
        #战场内排序确定行动过程
        dict_RStatus_temp = deepcopy(dict_RStatus_sequence)#self.get_sequenceOfAction()
        #print(dict_RStatus_temp)
        #dict_RStatus_temp_b = deepcopy(self.get_sequenceOfAction())
        for RStatus in dict_RStatus_temp:
            if list(RStatus.values())[0]['ID'] == 1:
                state_army1_1.append(list(RStatus.values())[0]['hp'])
                state_army1_1.append(list(RStatus.values())[0]['attack'])
                state_army1_1.append(list(RStatus.values())[0]['deffence'])
                state_army1_1.append(list(RStatus.values())[0]['speed'])
            if list(RStatus.values())[0]['ID'] == 7:
                state_army1_2.append(list(RStatus.values())[0]['hp'])
                state_army1_2.append(list(RStatus.values())[0]['attack'])
                state_army1_2.append(list(RStatus.values())[0]['deffence'])
                state_army1_2.append(list(RStatus.values())[0]['speed'])
        #进行回合战斗模拟
        for i in range(20):
            for cnt in self.dead_man:
                if cnt >=2:
                    self.kta = 99
            if self.kta == 99:
##                print('获胜方，army_index：',self.team_win)
##                print('回合：',i+1) #在战斗结束后的那个回合输出的这个信息
                break
            self.role_fight(dict_RStatus_temp)

		#罗列记录战斗后的状态，包括奖励、状态等等，返回给其他要用的地方
        for RStatus in dict_RStatus_temp:
            if list(RStatus.values())[0]['army_index'] == 1:
                hp_army1 += list(RStatus.values())[0]['hp']
            elif list(RStatus.values())[0]['army_index'] == 2:
                hp_army2 += list(RStatus.values())[0]['hp']

        self.score_winner = 10000 if self.team_win == 1 else -10000
        result = [state_army1_1,state_army1_2,[hp_army1, hp_army2, self.score_winner]]
        return result
