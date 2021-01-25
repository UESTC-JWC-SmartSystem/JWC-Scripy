import xlrd
import xlwt
from selenium import webdriver
import time
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
						  booksheet.cell_value(i, 3), booksheet.cell_value(i, 2)))

def writeData(turn, data):
	book = xlwt.Workbook(encoding='utf-8', style_compression=0)
	try:
		sheet = book.get_sheet('Out', cell_overwrite_ok=True)
	except:
		sheet = book.add_sheet('Out', cell_overwrite_ok=True)
	sheet.write(turn, 0, allstu[turn].name)
	sheet.write(turn, 1, allstu[turn].number)
	sheet.write(turn, 2, '网工')
	for i in range(len(data)):
		sheet.write(turn, i+3, data[i])

	book.save(r'网工.xls')


readData()
url = 'http://241374.yichafen.com/public/queryscore/sqcode/MsTcInwmMzAxfDViN2E2MGQwNTVkM2UO0O0O.html'
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)
i = 131
while(i < len(allstu)):
	driver.refresh()
	number = driver.find_element_by_xpath("//input[@name='s_xuehao']")
	number.clear()
	number.send_keys(allstu[i].number)
	name = driver.find_element_by_xpath("//input[@name='s_xingming']")
	name.clear()
	name.send_keys(allstu[i].name)
	psw = driver.find_element_by_xpath("//input[@name='s_2c54d23b18177aabe8759f1f551451f3']")
	psw.clear()
	psw.send_keys(allstu[i].psw)
	verify = driver.find_element_by_xpath("//input[@name='verify']")
	verify.clear()
	time.sleep(3)
	button = driver.find_element_by_xpath("//input[@id='queryBtn']")
	button.click()
	time.sleep(0.5)
	try:
		driver.implicitly_wait(1)
		backbtn = driver.find_element_by_id('backBtn')
		result = driver.find_element_by_xpath("//td[@id='result_content']")
		resstr = result.get_attribute('innerText')
		resstr = str(resstr)[0:-1]
		data = str(resstr).split('\t')
		data = data[-16:]
		print('{}	网工		'.format(allstu[i].name) + str(data))
		writeData(i, data)
		backbtn.click()
		flag = 3
	except:
		errormsg = driver.find_element_by_id("tableError")
		errmsg = errormsg.get_attribute('textContent')
		if('验证码' in errmsg):
			flag = 1
		else:
			flag = 2
			print('{}:该同学不为网工专业'.format(allstu[i].name))
	if flag == 2 or flag == 3:
		i += 1