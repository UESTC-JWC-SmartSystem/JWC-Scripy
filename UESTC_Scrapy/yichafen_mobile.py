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
		self.dic = {}
		self.classify = ''


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


def writeData():
	book = xlwt.Workbook(encoding='utf-8', style_compression=0)
	
	sheet = book.add_sheet('Out', cell_overwrite_ok=True)
	for j in range(len(allsubjects)):
		sheet.write(0, 4 + j, allsubjects[j])
	
	for i in range(len(allstu)):
		sheet.write(i + 1, 0, allstu[i].name)
		sheet.write(i + 1, 1, allstu[i].sex)
		sheet.write(i + 1, 2, allstu[i].number)
		sheet.write(i + 1, 3, allstu[i].classify)
		for j in range(len(allsubjects)):
			sheet.write(i + 1, 4 + j, allstu[i].dic.get(allsubjects[j], ''))
	
	book.save(r'out.xls')


allsubjects = []
readData()
urls = ['https://241374.yichafen.com/mobile/queryscore/sqcode/MsjcMn5mODM2fDVjNjdhMzllYmNiZTQO0O0O.html',
		'https://241374.yichafen.com/mobile/queryscore/sqcode/MsjcMn5mODM5fDVjNjdhNTUyYWNjZTgO0O0O.html',
		'https://241374.yichafen.com/mobile/queryscore/sqcode/MsjcMn5mODQxfDVjNjdhNjM2OWNkMWIO0O0O.html']
classes = ['通信工程', '网络工程', '物联网工程']
driver = webdriver.Chrome()

# i = 0
i = 15
driver.implicitly_wait(1)
while (i < len(allstu)):
	found = False
	for k in range(3):
		url = urls[k]
		driver.implicitly_wait(0.5)
		driver.get(url)
		driver.refresh()
		number = driver.find_element_by_xpath("//input[@name='s_xuehao']")
		number.clear()
		number.send_keys(allstu[i].number)
		name = driver.find_element_by_xpath("//input[@name='s_xingming']")
		name.clear()
		name.send_keys(allstu[i].name)
		try:
			psw = driver.find_element_by_xpath("//input[@name='s_af5d07abb70b9f4f6b0bc928640f3734']")
		except:
			psw = driver.find_element_by_xpath("//input[@name='s_280e207dfc8257ea638b195fe06fdbe7']")
		
		psw.clear()
		psw.send_keys(allstu[i].psw)
		button = driver.find_element_by_xpath("//a[@id='yiDunSubmitBtn']")
		button.click()
		flag = False
		try:
			driver.implicitly_wait(0.5)
			errormsg = driver.find_element_by_xpath("//div[@class='weui-dialog__bd']")
		# print(errormsg.text)
		except:
			flag = True
		
		if flag:
			time.sleep(0.8)
			allstu[i].classify = classes[k]
			found = True
			subnames = driver.find_elements_by_class_name('left_cell')
			grades = driver.find_elements_by_class_name('right_cell')
			for j in range(3, len(subnames)):
				if not subnames[j].text in allsubjects:
					allsubjects.append(subnames[j].text)
				allstu[i].dic[subnames[j].text] = grades[j].text
			break
	print('{} {} : {}, finished'.format(str(i + 1), allstu[i].name, allstu[i].classify))
	i += 1
	writeData()
	print('写入完成')
