import xlrd
import xlwt

courses = [[], [], [], []]
weight = [[], [], [], []]
allstu = {}


class stu():
	def __init__(self, number, name):
		self.number = number
		self.name = name
		self.dic = {}
		self.classify = ''


sheetlist = ['dy.xlsx', 'dygfs.xlsx', 'de1.xlsx', 'de2.xlsx']


def readData():
	global courses, weight
	for (classify, listname) in enumerate(sheetlist):
		workbook = xlrd.open_workbook(listname)
		print(workbook.nsheets)
		for sheetindex in range(workbook.nsheets):
			booksheet = workbook.sheet_by_index(sheetindex)
			print(booksheet.name)
			col = booksheet.ncols
			row = booksheet.nrows
			print(col, row)

			if classify >= 2:
				for i in range(2, col):
					if booksheet.cell_value(0, i) not in courses[sheetindex]:
						courses[sheetindex] += [booksheet.cell_value(0, i)]
						weight[sheetindex] += [booksheet.cell_value(1, i)]

			if classify == 0:
				for turn in range(4):
					for i in range(2, col):
						courses[turn] += [booksheet.cell_value(0, i)]
						weight[turn] += [booksheet.cell_value(1, i)]

			if classify == 1:
				for i in range(2, col):
					courses[3] += [booksheet.cell_value(0, i)]
					weight[3] += [booksheet.cell_value(1, i)]

			for i in range(2, row):
				for j in range(2, col):
					number = booksheet.cell_value(i, 0)
					if str(number).replace('.', '').isdigit():
						number = str(int(number))
					name = booksheet.cell_value(i, 1)
					if allstu.get(number, None) == None:
						allstu[number] = stu(number, name)

					coursename = booksheet.cell_value(0, j)
					if str(booksheet.cell_value(i, j)).replace('.', '').isdigit():
						allstu[number].dic[coursename] = booksheet.cell_value(i, j)
					if classify >= 2:
						allstu[number].classify = booksheet.name


classes = ['通信工程', '网络工程', '物联网工程', '国防生']


def writeData():
	book = xlwt.Workbook(encoding='utf-8', style_compression=0)
	for classify in range(4):
		sheet = book.add_sheet(classes[classify], cell_overwrite_ok=True)
		for (i, course) in enumerate(courses[classify]):
			sheet.write(0, 2 + i, course)
			sheet.write(1, 2 + i, weight[classify][i])

		turn = 0
		for (number, student) in allstu.items():
			# print(student.classify)
			# print(classes[classify])
			if student.classify == classes[classify]:
				sheet.write(turn + 2, 0, student.number)
				sheet.write(turn + 2, 1, student.name)
				for (i, course) in enumerate(courses[classify]):
					if student.dic.get(course, None) == None:
						sheet.write(turn + 2, i + 2, '不存在')
					else:
						sheet.write(turn + 2, i + 2, student.dic[course])
				turn += 1
	book.save(r'grade_all.xls')


readData()
print(courses[0])
print(courses[1])
print(courses[2])
print(courses[3])
writeData()
# for (number, student) in allstu.items():
# 	print(number)
# 	print(student.name)
# 	print(student.classify)
# 	for (course, grade) in student.dic.items():
# 		print(course, grade)
