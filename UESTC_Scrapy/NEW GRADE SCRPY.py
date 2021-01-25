import base64
import time
import xlrd
import os

import xlwt
from selenium import webdriver

START = 0

allstu = []


class stu():
	def __init__(self, name, sex, number, psw):
		self.name = name
		self.sex = sex
		self.number = number
		self.psw = psw[-7:-1]
		self.course = {}


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
subjects = []

def writeData():
	book = xlwt.Workbook(encoding='utf-8', style_compression=0)

	sheet = book.add_sheet('Out', cell_overwrite_ok=True)
	for j in range(len(subjects)):
		sheet.write(0, 3 + j, subjects[j])

	for i in range(len(allstu)):
		sheet.write(i + 1, 0, allstu[i].name)
		sheet.write(i + 1, 1, allstu[i].sex)
		sheet.write(i + 1, 2, allstu[i].number)
		for j in range(len(subjects)):
			sheet.write(i + 1, 3 + j, allstu[i].course.get(subjects[j], ''))

	book.save(r'grade_get.xls')
readData()
for i in range(START, len(allstu)):
	driver = webdriver.Chrome()
	driver.delete_all_cookies()
	driver.refresh()
	url = 'http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal'
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
				time.sleep(0.5)
				try:
					conti = driver.find_element_by_link_text("点击此处")
					conti.click()
				except:
					# print('{} 登陆正常'.format(stu))
					_ = 1
				
				url = 'http://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=203'
				driver.get(url)
				time.sleep(0.5)
				driver.get(url)
			except:
				flag = False

			if flag:
				datas = driver.find_elements_by_xpath("//td")
				re = []
				for turn, data in enumerate(datas):
					# print(turn + 1, data.text)
					re += [data.text]
					if (turn + 1) % 10 == 0:
						if re[3] not in subjects:
							subjects += [re[3]]
						allstu[i].course[re[3]] = re[6]
						re = []
				writeData()
				print("{} {}: Yes".format(i, allstu[i].name))
		else:
			print("{} {}: No".format(i, allstu[i].name))
	else:
		print("{} {}: No".format(i, allstu[i].name))
	driver.close()