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

select = input("1.注册\n2.登录\n")

while select != "1" and select != "2":
	print("请输入正确的选项！")
	select = input("1.注册\n2.登录\n")

if select == "1":
	modules.regist(db)

while IS_LOG == False:
	USERNAME, IS_LOG, AUTH = modules.login(db)

print(USERNAME + '\t' + AUTH)

if AUTH == "admin":
	select = input("1.加入题目\n请做出你的选择:\n")
	if select == "1":
		print("你选择了'1.加入题目'")
		modules.addquestion(db)
elif AUTH == "user":
	select = input("1.生成考试\n请做出你的选择:\n")
	if select == "1":
		print("你选择了1.生成考试")
		num = input("请输入你需要的题目数量:\n")
		print("将为你随机生成" + str(num) + "道题目")
		exam = modules.cre8exam(num, db)
		ans = modules.examination(exam)
		modules.submitans(USERNAME, ans, db)

db.close()
