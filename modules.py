import sqlite3

def login(db):
	user = input("请输入你要登录的账户名:")
	password = input("请输入你的密码:")
	dx = db.cursor()
	dx.execute("select username, password, authority  from auth")
	user_tuple = dx.fetchall()
	up_dic = dict()
	ua_dic = dict()
	for item in user_tuple:
		up_dic[item[0]] = item[1]
		ua_dic[item[0]] = item[2]
	if user not in up_dic:
		print("用户名不存在，请注册！")
		select = input("选择是否要注册(Yes or No)")
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
	username_tuple = dx.fetchall()
	username_list = list()
	for item in username_tuple:
		username_list.append(item[0])
	user = input("请输入你要注册的账户名:")
	while user in username_list:
		print("改账号名已经存在，请重试")
		user = input("请输入你要注册的账户名:")
	password = input("请输入你的密码:")
	repeat = input("请重新输入你的密码:")
	while password != repeat:
		print("密码不相同请重试")
		password = input("请输入你的密码:")
		repeat = input("请重新输入你的密码:")
	dx.execute('INSERT INTO auth(username,password,authority) VALUES(?,?,?)',(user, password,"user"))
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
		db.execute("create table submission(id integer primary key ,\
											username varchar(20),\
											answers varchar(50),\
											score INT);")
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
	st_ans = input("请输入标准答案")
	if questype == "选择":
		dx.execute('INSERT INTO question(description,options,type,st_answer) VALUES(?,?,?,?)',(description,options,questype,st_ans))
		print("你添加了一道选择题")
	else:
		dx.execute('INSERT INTO question(description,type,st_answer) VALUES(?,?,?)',(description,questype,st_ans))
		print("你添加了一道判断题")
	db.commit()

def cre8exam(num, db):
	lis = []
	print("生成试卷成功！")
	return lis

def examination(exam):
	print("开始考试！")
	ans = ""
	for item in exam:
		select = input("选择你的答案:\n")
		print(exam)
	return ans

def judge(ans, db):
	print("正在判分，请稍等...")
	return 100

def submit(user, ans, db):
	score = str(judge(ans, db))
	print(user + "\t" + ans + "\t" + score)
