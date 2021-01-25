import base64
import time
import xlrd
import os
from selenium import webdriver

START = 0
DIR = r'./17班_pic'

allstu = []


class stu():
	def __init__(self, name, sex, number, psw):
		self.name = name
		self.sex = sex
		self.number = number
		self.psw = psw[-7:-1]


def readData():
	global allstu
	workbook = xlrd.open_workbook('data.xlsx')
	booksheet = workbook.sheet_by_index(0)
	col = booksheet.ncols
	row = booksheet.nrows
	print(row, col)
	for i in range(row):
		allstu.append(stu(booksheet.cell_value(i, 0), booksheet.cell_value(i, 1),
						  str(int(booksheet.cell_value(i, 3))), booksheet.cell_value(i, 2)))


readData()
url = 'http://idas.uestc.edu.cn/authserver/login?service=http%3A%2F%2Fecard.uestc.edu.cn%2Fcaslogin.jsp'
driver = webdriver.Chrome()
for i in range(START, len(allstu)):
	driver.delete_all_cookies()
	driver.refresh()
	driver.get(url)
	name = driver.find_element_by_xpath("//input[@id='username']")
	name.clear()
	# print(allstu[i].number)
	name.send_keys(allstu[i].number)
	psw = driver.find_element_by_xpath("//input[@id='password']")
	psw.clear()
	psw.send_keys(allstu[i].psw)
	submit = driver.find_element_by_xpath("//button[@type='submit']")
	submit.click()
	flag = True
	try:
		driver.implicitly_wait(0.2)
		fail = driver.find_element_by_xpath("//span[@class='auth_error']")
		flag = False
	except:
		flag = True

	if flag:
		try:
			driver.implicitly_wait(0.2)
			fail = driver.find_element_by_xpath("//label[@class='logout_info']")
			flag = False
		except:
			flag = True
		if flag:
			try:
				driver.implicitly_wait(0.2)
				img = driver.find_element_by_xpath("//img[@style='height:80px;width:60px']")
			except:
				driver.back()
				try:
					driver.implicitly_wait(0.2)
					img = driver.find_element_by_xpath("//img[@style='height:80px;width:60px']")
				except:
					driver.back()
					try:
						driver.implicitly_wait(0.2)
						img = driver.find_element_by_xpath("//img[@style='height:80px;width:60px']")
					except:
						flag = False

			if flag:
				imgsrc = img.get_attribute('src')[22:]
				imgdata = base64.b64decode(imgsrc)
				flag = os.path.exists(DIR)
				if not flag:
					os.makedirs(DIR)
				file = open(DIR + '/{}.jpg'.format(allstu[i].number[-5:-3] + " " + allstu[i].number[-2:] + " " + allstu[i].name), 'wb')
				file.write(imgdata)
				file.close()
				quitbutton = driver.find_element_by_xpath("//a[@href='/caslogout.jsp']")
				quitbutton.click()
				print("{} {}: Yes".format(i, allstu[i].name))
			else:
				print("{} {}: No".format(i, allstu[i].name))
		else:
			print("{} {}: No".format(i, allstu[i].name))
	else:
		print("{} {}: No".format(i, allstu[i].name))
