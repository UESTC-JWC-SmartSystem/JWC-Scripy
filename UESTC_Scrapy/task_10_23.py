import xlrd
import xlwt

courses = []
weight = []
allstu = {}


class stu():
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.dic = {}
        self.classify = ''


sheetlist = ['task_10_23/da2_1.xlsx', 'task_10_23/da2_2.xlsx', 'task_10_23/da1_1.xlsx', 'task_10_23/da1_2.xlsx', 'task_10_23/da1_3.xlsx']
afterDIVIDE = 1
NUMBERCOL = 1
NAMECOL = 0

classes = []

def readData():
    global courses, weight, classes
    for (classify, listname) in enumerate(sheetlist):
        workbook = xlrd.open_workbook(listname)
        print(workbook.nsheets)
        for sheetindex in range(workbook.nsheets):
            booksheet = workbook.sheet_by_index(sheetindex)
            print(booksheet.name)
            col = booksheet.ncols
            row = booksheet.nrows
            print(col, row)

            if classify <= afterDIVIDE:
                classes += [booksheet.name]
                courses += [[]]
                weight += [[]]
                for i in range(2, col):
                    if not booksheet.cell_value(0, i) in courses[len(classes) - 1]:
                        courses[len(classes) - 1] += [booksheet.cell_value(0, i)]
                        weight[len(classes) - 1] += [booksheet.cell_value(1, i)]
            else:
                for j in range(len(classes)):
                    if classes[j] in booksheet.name:
                        for i in range(2, col):
                            if not booksheet.cell_value(0, i) in courses[j]:
                                courses[j] += [booksheet.cell_value(0, i)]
                                weight[j] += [booksheet.cell_value(1, i)]


            for i in range(2, row):
                for j in range(2, col):
                    number = booksheet.cell_value(i, NUMBERCOL)
                    if str(number).replace('.', '').isdigit():
                        number = str(int(number))
                    name = booksheet.cell_value(i, NAMECOL)
                    if allstu.get(number, None) == None:
                        allstu[number] = stu(number, name)

                    coursename = booksheet.cell_value(0, j)
                    if str(booksheet.cell_value(i, j)).replace('.', '').isdigit():
                        allstu[number].dic[coursename] = booksheet.cell_value(i, j)
                    if classify <= afterDIVIDE:
                        allstu[number].classify = booksheet.name



def writeData():
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    for classify in range(len(classes)):
        sheet = book.add_sheet(classes[classify], cell_overwrite_ok=True)
        for (i, course) in enumerate(courses[classify]):
            sheet.write(0, 2 + i, course)
            sheet.write(1, 2 + i, weight[classify][i])

        turn = 0
        for (number, student) in allstu.items():
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
writeData()
# for (number, student) in allstu.items():
# 	print(number)
# 	print(student.name)
# 	print(student.classify)
# 	for (course, grade) in student.dic.items():
# 		print(course, grade)
