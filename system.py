import os
import sqlite3
import modules

DATABASE_STRESS = "C:/Users/MZI/Desktop/Simulated-Examination-and-Learning-System/data.db"

USERNAME = ""
AUTH = ""
IS_LOG = False

print("---------------驾驶员理论课程模拟考试与学习系统 v1.0--------------------")

db = sqlite3.connect(DATABASE_STRESS)

modules.initdb(db)

select = input("1.注册\n2.登录\n3.退出\n")

while select != "1" and select != "2" and select != "3":
	print("请输入正确的选项！")
	select = input("1.注册\n2.登录\n3.退出\n")

if select == "3":
	quit()
elif select == "1":
	modules.regist(db)

while IS_LOG == False:
	USERNAME, IS_LOG, AUTH = modules.login(db)

print(USERNAME + " 登录成功!(" + AUTH + ")\n")

def judge(str):
	for i in range(0, len(str)):
		if ord(str[i]) < 48 or ord(str[i]) > 57:
			return False
	if int(str) <= 0:
		return False
	return True

while 1:
	if AUTH == "admin":
		select = input("1.加入题目\n2.修改题目\n3.删除题目\n4.退出\n")
		if select != "4" and select != "1" and select != "2" and select != "3":
			print("请输入正确的选项！")
			continue
		elif select == "4":
			quit()
		elif select == "1":
			print("你选择了'1.加入题目'")
			modules.addquestion(db)
		elif select == "2":
			print("你选择了'2.修改题目'")
			modules.modiquestion(db)
		elif select == "3":
			print("你选择了'3.删除题目'")
			modules.delequestion(db)
	elif AUTH == "user":
		select = input("1.生成考试\n2.考试统计\n3.退出\n")
		if select != "3" and select != "2" and select != "1":
			print("请输入正确的选项！")
			continue
		if select == "3":
			quit()
		elif select == "1":
			print("你选择了1.生成考试")
			num = input("请输入你需要的题目数量:\n")
			while judge(num) == False:
				print("请输入正确的数量")
				num = input("请输入你需要的题目数量:\n")
			print("将为你随机生成" + num + "道题目...")
			problem, src = modules.cre8exam(num, db)
			num = int(num)
			ans = modules.exam(num, problem)
			score = modules.submit(USERNAME, ans, src, db)
			print("你的得分是:" + str(score))
			select = input("是否要继续(Yes or No):\n")
			if select.lower() == "no":
				quit()
			os.system("cls")
		elif select == "2":
			print("你选择了2.考试统计")
			modules.examstat(USERNAME, db)

db.close()
