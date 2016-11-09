import os
import sqlite3
import random
import getpass

def judgenum(str):
	for i in range(0, len(str)):
		if ord(str[i]) < 48 or ord(str[i]) > 57:
			return False
	if int(str) <= 0:
		return False
	return True

def login(db):
	user = input("请输入你要登录的账户名:\n")
	password = getpass.getpass("请输入你的密码:\n")
	dx = db.cursor()
	dx.execute("select username, password, authority  from auth")
	user_turple = dx.fetchall()
	up_dic = dict()
	ua_dic = dict()
	for item in user_turple:
		up_dic[item[0]] = item[1]
		ua_dic[item[0]] = item[2]
	if user not in up_dic:
		print("用户名不存在，请注册！")
		select = input("选择是否要注册(Yes or No)\n")
		if select.lower() == "yes":
			regist(db)
		return "", False, ""
	else:
		if(up_dic[user] == password):
			return user, True, ua_dic[user]
		else:
			print("密码错误!")
			return "", False, ""

def regist(db):
	dx = db.cursor()
	dx.execute("select username from auth")
	username_turple = dx.fetchall()
	username_list = list()
	for item in username_turple:
		username_list.append(item[0])
	user = input("请输入你要注册的账户名:\n")
	while user in username_list:
		print("改账号名已经存在，请重试")
		user = input("请输入你要注册的账户名:\n")
	password = input("请输入你的密码:\n")
	repeat = input("请重新输入你的密码:\n")
	while password != repeat:
		print("密码不相同请重试")
		password = input("请输入你的密码:\n")
		repeat = input("请重新输入你的密码:\n")
	dx.execute('INSERT INTO auth(username,password,authority) VALUES(?,?,?)',(user, password,"user"))
	dx.execute('INSERT INTO userstat(username,examnum,examscore,record) VALUES(?,?,?,?)',(user,0,0,"你还没有参加过考试"))
	db.commit()

def initdb(db):
	dx = db.cursor()
	try:
		dx.execute("create table auth(	id integer primary key autoincrement,\
										username varchar(20),\
										password varchar(20),\
										authority varchar(20));")
	except:
		pass
	try:
		dx.execute("create table question(	id integer primary key autoincrement,\
											type varchar(20),\
											description varchar(50),\
											options varchar(50),\
											st_answer varchar(50));")
	except:
		pass
	try:
		dx.execute("create table userstat(	username varchar(20),\
											examscore integer,\
											examnum integer,\
											record text);")
	except:
		pass
	db.commit()

def addquestion(db):
	dx = db.cursor()
	questype = input("请输入问题的类型(选择or判断):\n")
	description = input("请输入问题的描述:\n")
	options = ""
	if questype == "选择":
		chc = 65
		for i in range(0, 4):
			options += chr(chc) + " "
			options += input("请输入"+chr(chc)+"的选项:\n")
			chc += 1
			options += "\n"
		print(options)
	st_ans = input("请输入标准答案:\n")
	if questype == "选择":
		dx.execute('INSERT INTO question(description,options,type,st_answer) VALUES(?,?,?,?)',(description,options,questype,st_ans))
		print("你添加了一道选择题\n")
	else:
		dx.execute('INSERT INTO question(description,type,st_answer) VALUES(?,?,?)',(description,questype,st_ans))
		print("你添加了一道判断题\n")
	db.commit()

def cre8exam(num, db):
	dx = db.cursor()
	dx.execute("select id, type, description, options from question")
	problem_turple = dx.fetchall()
	problem_list = list()
	src_list = list()
	while int(num) > len(problem_turple):
		print("题库目前只有" + str(len(problem_turple)) + "道题目，请输入小于等于" + str(len(problem_turple)) + "的数目")
		num = input("请输入你需要的题目数量:\n")
		while judgenum(num) == False:
			print("请输入正确的数量")
			num = input("请输入你需要的题目数量:\n")
	num = int(num)
	randm = list()
	for i in range(0, len(problem_turple)):
		randm.append(i)
	random.shuffle(randm)
	randm = randm[:num]
	for i in randm:
		problem_list.append(problem_turple[i])
		src_list.append(problem_turple[i][0])
	return problem_list, src_list

def exam(num, problem):
	print("考试开始！")
	ans = ""
	print(problem)
	for i in range(0, num):
		print(str(i+1) + "." + problem[i][2])
		if problem[i][1] == "选择":
			print(problem[i][3])
		if problem[i][1] == "选择":
			select = input("请选择（A,B,C或者D):\n").upper()
			while select != "A" and select != "B" and select != "C" and select != "D":
				print("请输入正确的选择!")
				select = input("请选择（A,B,C或者D):\n").upper()
			ans += select
		elif problem[i][1] == "判断":
			select = input("请选择（T或者F):\n").upper()
			while select != "T" and select != "F":
				print("请输入正确的选择!")
				select = input("请选择（T或者F):\n").upper()
			ans += select
	return ans

def judge(ans, st):
	print("正在判分，请稍等...")
	tot = len(st)
	score = 100.0
	for i in range(0, tot):
		if ans[i] != st[i]:
			score -= 100 / tot;
	return int(score)

def submit(user, ans,src, db):
	dx = db.cursor()
	dx.execute("select id, st_answer from question")
	problem_turple = dx.fetchall()
	standard = ""
	wrong_answer = ""
	correct_answer = ""
	question_des = ""
	for i in src:
		standard += problem_turple[i-1][1]
	score = judge(ans, standard)
	tot = len(standard)
	wrong_num = 0
	for i in range(0, tot):
		if ans[i] != standard[i]:
			wrong_num += 1
			wrong_answer += str(src[i]) + ans[i] +" "
			correct_answer += str(src[i]) + standard[i] +" "
			dx.execute("select id,type,description,options from question")
			question_turple = dx.fetchall()
			for j in question_turple:
				if(j[0]==src[i]):
					if(j[1]=="选择"):
						question_des += "你做错的题：\n\n"+str(wrong_num)+"(选择题)\n"+j[2] +"\n"+"选项是"+j[3]+"\n你的选项是：" + ans[i] +"\n"+"正确选项是：" + standard[i] +"\n"
					else:
						question_des += "你做错的题：\n\n"+str(wrong_num)+"(判断题)\n"+j[2] +"\n你的选项是："+ ans[i] +"\n"+"正确选项是："  + standard[i] +"\n"
	dx.execute("select username,examnum from userstat")
	users_turple = dx.fetchall()
	for i in users_turple:
		if (i[0] == user):
			count = i[1]
	dx.execute("select username,examscore from userstat")
	score_turple = dx.fetchall()
	score_count = 0
	for i in score_turple:
		if (i[0] == user):
			score_count = (i[1]*count+score)/(count+1)
	text=""
	dx.execute("select username,record from userstat")
	record_old = dx.fetchall()
	for i in record_old:
		if(i[0] == user):
			if(i[1] != None):
				text += i[1]
	score_count_str = str(score_count)
	count_str = str(count + 1)
	dx.execute("UPDATE userstat set examscore ="  + score_count_str + " where username='" + user +"'")
	dx.execute("UPDATE userstat set examnum = " + count_str +  " where username='" + user +"'")
	text += "第" +count_str+ "次考试:\n" +"这次考试成绩是："+ str(score) +"\n"+question_des +"\n"+"-"
	dx.execute("UPDATE userstat set record = '" + text +  "' where username='" + user +"'")
	db.commit()
	return score

def delequestion(db):
	dx = db.cursor()
	dx.execute("select id, type, description, options, st_answer from question")
	problem_list = dx.fetchall()
	if len(problem_list) == 0:
		print("题库中暂时没有题目,请尝试添加题目!")
		return
	print("现在为你列出所有的题目")
	for item in problem_list:
		print(str(item[0]) + " (" + item[1] + ") " + item[2])
	select = input("请输入你要删除的题目编号:\n")
	while int(select) <= 0 or int(select) > len(problem_list):
		print("编号不存在,请重试!")
		select = input("请输入你要删除的题目编号:\n")
	select = int(select)
	problem_list.pop(select-1)
	dx.execute("drop table question;")
	dx.execute("create table question(	id integer primary key autoincrement,\
										type varchar(20),\
										description varchar(50),\
										options varchar(50),\
										st_answer varchar(50));")
	for item in problem_list:
		dx.execute('INSERT INTO question(type, description, options, st_answer) VALUES(?,?,?,?)',(item[1], item[2], item[3], item[4]))
	db.commit()
	print("删除成功!")

def modiquestion(db):
	dx = db.cursor()
	dx.execute("select id, type, description, options, st_answer from question")
	problem_list = dx.fetchall()
	if len(problem_list) == 0:
		print("题库中暂时没有题目,请尝试添加题目!")
		return
	print("现在为你列出所有的题目")
	for item in problem_list:
		print(str(item[0]) + " (" + item[1] + ") " + item[2])
	select = input("请输入你要修改的题目编号:\n")
	while int(select) <= 0 or int(select) > len(problem_list):
		print("编号不存在,请重试!")
		select = input("请输入你要修改的题目编号:\n")
	questype = input("请输入问题的类型(选择or判断):\n")
	description = input("请输入问题的描述:\n")
	options = ""
	if questype == "选择":
		chc = 65
		for i in range(0, 4):
			options += chr(chc) + " "
			options += input("请输入"+chr(chc)+"的选项:\n")
			chc += 1
			options += "\n"
		print(options)
	st_ans = input("请输入标准答案:\n")
	dx.execute("UPDATE question set type = '" + questype +  "' where id=" + select)
	dx.execute("UPDATE question set description = '" + description +  "' where id=" + select)
	dx.execute("UPDATE question set options = '" + options +  "' where id=" + select)
	dx.execute("UPDATE question set st_answer = '" + st_ans +  "' where id=" + select)
	db.commit()
	print("修改成功!")

def examstat(user,db):
	dx = db.cursor()
	dx.execute("select username,examscore from userstat")
	user_text = dx.fetchall()
	for i in user_text:
		if (i[0] == user):
			print ("你的平均分是:"+str(i[1]))
			score_record = i[1]
	dx.execute("select username,record from userstat")
	user_exam = dx.fetchall()
	text_list = []
	text_str = ""
	for i in user_exam:
		if(i[0]==user):
			text_str += i[1]
	#print(text_str)
	if (len(text_str)>9):
		x=0
		while len(text_str) > 1:
			if (text_str[x]=="-"):
				if (len(text_list)>0):
					text_list.append(text_str[:x])
					text_str = text_str[x+1:]
				else:
					text_list.append(text_str[9:x])
					text_str = text_str[x+1:]
			x += 1
	#print (text_list)
	count = len(text_list)
	if (score_record == 0 and len(text_str)==9):
		print ("你还没有参加考试")
	else:
		print (text_list[0])
	for i in range(1,count):
		select = input("1.查看下一场\n2.退出\n")
		while select != "1" and select != "2":
			print("请输入正确的选项!")
			select = input("1.查看下一场\n2.退出\n")
		if select == "2":
			break
		if select == "1":
			os.system("cls")
			print (text_list[i])
			