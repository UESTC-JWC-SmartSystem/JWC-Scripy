import numpy as np
import uestc
import xlrd
import xlwt
import time

class stu():
	def __init__(self, name, sex, number, psw):
		self.name = name
		self.sex = sex
		self.number = number
		self.psw = psw[-7:-1]
		self.dic = {}


allstu = []


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
	for j in range(len(subjects)):
		sheet.write(0, 3 + j, subjects[j])

	for i in range(len(allstu)):
		sheet.write(i + 1, 0, allstu[i].name)
		sheet.write(i + 1, 1, allstu[i].sex)
		sheet.write(i + 1, 2, allstu[i].number)
		for j in range(len(subjects)):
			sheet.write(i + 1, 3 + j, allstu[i].dic.get(subjects[j], ''))

	book.save(r'out.xls')


kinds = ['学科通识课程', '实践类核心课程', '学科基础课程', '学科基础课程', '实践类核心课程', '学科拓展课程', '本专业选修课', '大学体育IV', '大学体育III']
subjects = []
readData()
for i in range(0, len(allstu)):
# for i in range(0, 5):
	try:
		time.sleep(2)
		ssion = uestc.login(allstu[i].number, allstu[i].psw)
		re = uestc.query.get_score(ssion, '163')
		for subject in re:
			if subject[4] in kinds:
				allstu[i].dic[subject[3]] = subject[6]
				if not subject[3] in subjects:
					subjects.append(subject[3])
		re = uestc.query.get_score(ssion, '183')
		for subject in re:
			if subject[4] in kinds:
				allstu[i].dic[subject[3]] = subject[6]
				if not subject[3] in subjects:
					subjects.append(subject[3])

		print(allstu[i].name, "succeed")
		if i % 10 == 0:
			writeData()
	except:
		print(allstu[i].name, "failed")
writeData()
