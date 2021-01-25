import xlrd
import xlwt

allstueng = {}

class stu():
	def __init__(self, number, name):
		self.number = number
		self.name = name
		self.dic = {}
		# self.classify = ''


def findeng(number, courses):
	if allstueng.get(number, '#N/A') == '#N/A':
		return '#N/A'
	else:
		return allstueng[number].dic.get(courses, '#N/A')

def readData():
	global courses, weight
	workbook = xlrd.open_workbook('english.xlsx')
	print(workbook.nsheets)
	for sheetindex in range(workbook.nsheets):
		courses = []
		booksheet = workbook.sheet_by_index(sheetindex)
		print(booksheet.name)
		col = booksheet.ncols
		row = booksheet.nrows
		print(col, row)
		for i in range(5, col):
			courses += [booksheet.cell_value(1, i)]
		print(courses)
		for i in range(3, row):
			tmpstu = stu(booksheet.cell_value(i, 0), booksheet.cell_value(i, 2))
			if str(tmpstu.number).replace('.', '').isdigit():
				tmpstu.number = str(int(tmpstu.number))
			for j in range(5, col):
				tmpstu.dic[courses[j - 5]] = booksheet.cell_value(i, j)
			print(tmpstu.number)
			allstueng[tmpstu.number] = tmpstu

	print(len(allstueng))
	print('英语分数读取完成。\n')

	workbook = xlrd.open_workbook('ALL.xlsx')
	print(workbook.nsheets)
	for sheetindex in range(workbook.nsheets):
		booksheet = workbook.sheet_by_index(sheetindex)
		print(booksheet.name)
		col = booksheet.ncols
		row = booksheet.nrows
		print(col, row)
		f = open("output_{}.txt".format(booksheet.name), 'w')
		f.truncate()
		for i in range(2, row):
			number = booksheet.cell_value(i, 1)
			if str(number).replace('.', '').isdigit():
				number = str(int(number))
			print(number)
			f.write('{}	{}	{}\n'.format(findeng(number, '英语A类'), findeng(number, '英语B类'), findeng(number, '英语C类')))
		f.close()
	print('finish')



# def writeData():
# 	book = xlwt.Workbook(encoding='utf-8', style_compression=0)
# 	for classify in range(4):
# 		sheet = book.add_sheet(classes[classify], cell_overwrite_ok=True)
# 		for (i, course) in enumerate(courses[classify]):
# 			sheet.write(0, 2 + i, course)
# 			sheet.write(1, 2 + i, weight[classify][i])
#
# 		turn = 0
# 		for (number, student) in allstu.items():
# 			# print(student.classify)
# 			# print(classes[classify])
# 			if student.classify == classes[classify]:
# 				sheet.write(turn + 2, 0, student.number)
# 				sheet.write(turn + 2, 1, student.name)
# 				for (i, course) in enumerate(courses[classify]):
# 					if student.dic.get(course, None) == None:
# 						sheet.write(turn + 2, i + 2, '不存在')
# 					else:
# 						sheet.write(turn + 2, i + 2, student.dic[course])
# 				turn += 1
# 	book.save(r'grade_all.xls')


readData()
# writeData()
