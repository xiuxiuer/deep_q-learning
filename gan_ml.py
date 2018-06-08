import xlrd
import gameplay.gameplay as gp
from copy import deepcopy

rolestatus_book = xlrd.open_workbook("G:\Python\Python35\\test_files\\test.xlsx")
rolestatus_sheet = rolestatus_book.sheet_by_index(0)

episode_num = 2

##print("The number of worksheets is {0}".format(rolestatus_book.nsheets))
##print("The number of worksheets is {0}".format(rolestatus_book.sheet_names()))
##print("{0} {1} {2}".format(rolestatus_sheet.name, rolestatus_sheet.nrows,
##                           rolestatus_sheet.ncols))

#建立全部role各状态属性表 "G:\Python\Python35\test_files\test.xlsx"
role_seq = []
for rIndex in range(rolestatus_sheet.nrows-1):
    role_seq.append(rIndex+1)
print(role_seq)
##allrole_status = dict.fromkeys(role_seq)
allrole_status = {}

#建立role各状态属性名称
for rIndex in range(rolestatus_sheet.nrows):
    if rIndex == 0:
        seq = rolestatus_sheet.row_values(rIndex)
print(seq)

#创建单个role各状态属性表
role_status = dict.fromkeys(seq,)

for rIndex in range(rolestatus_sheet.nrows):
    #确定属性名称，作为字典键
    if rIndex >= 1:
        pre_status = rolestatus_sheet.row_values(rIndex)
        #print(pre_status)
        for cIndex in range(len(pre_status)):
            if type(pre_status[cIndex]) == float:
                role_status[seq[cIndex]] = int(pre_status[cIndex])
            else:
                role_status[seq[cIndex]] = pre_status[cIndex]
##            print(pre_status[cIndex])
        #deepcopy能传递值，=赋值是传递地址
        allrole_status[rIndex] = deepcopy(role_status)

##print(allrole_status)


role_status_backup = deepcopy(allrole_status)
FB = gp.Fight_battle(role_status_backup)

for episode in range(episode_num):
    print('episode:',episode)
    FB.start_step()
    #重置初始属性
    FB.dict_RStatus = deepcopy(allrole_status)
    #print(allrole_status)
##dqn_t = dqn_gp.DQN_gameplay()
