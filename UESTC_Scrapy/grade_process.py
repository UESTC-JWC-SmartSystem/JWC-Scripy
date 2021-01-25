import xlrd

courses = []
stugrades = {}
def strisdigit(st):
	return str(st).replace('.', '').isdigit()

def readData(workbookname, xhlie, xfhang):
	global courses
	try:
		xfhang = int(xfhang)
		xhlie = int(xhlie)
		xfhang -= 1
		xhlie -= 1
		workbook = xlrd.open_workbook(workbookname)
		for sheetindex in range(workbook.nsheets):
			booksheet = workbook.sheet_by_index(sheetindex)
			col = booksheet.ncols
			row = booksheet.nrows
			f = open("output_{}.txt".format(booksheet.name), 'w')
			f.truncate()

			print(booksheet.name, ', 尺寸:', row, col)
			weight = []
			flag = False
			for j in range(0, col):
				# print(booksheet.cell_value(xfhang, j))
				if strisdigit(booksheet.cell_value(xfhang, j)) and float(booksheet.cell_value(xfhang, j)) <= 30.0 and float(booksheet.cell_value(xfhang, j)) > 0.0:
					if not flag:
						flag = True
						dy = j
				else:
					if flag:
						maxcol = j
						flag = False
						break
			if flag:
				maxcol = j + 1
			print('学分区域智能识别完成:', dy, maxcol)
			dx = xfhang
			for j in range(0 + dy, maxcol):
				weight += [booksheet.cell_value(dx, j)]

			print('课程权重序列:', weight)
			for i in range(1 + dx, row):
				totweight = 0
				all = 0
				number = str(booksheet.cell_value(i, xhlie))
				if strisdigit(number):
					number = str(int(float(number)))
				for j in range(0 + dy, maxcol):
					if strisdigit(booksheet.cell_value(i, j)):
						totweight += weight[j - dy]
						all += weight[j - dy] * float(booksheet.cell_value(i, j))
				if totweight > 0:
					# print(all / totweight)
					stugrades[number] = str(all / totweight)
					f.write(stugrades[number])
				else:
					if stugrades.get(number, None) == None:
						stugrades[number] = '不存在'
					f.write(stugrades[number])
					# print('不存在')
				f.write('\n')
			f.close()
			print('{} 计算完成, 结果已输出至 output_{}.txt\n'.format(booksheet.name, booksheet.name))
	except Exception as e:
		print(e)

if __name__ == '__main__':
	print('@copyright Zin from SICE 2018\n')
	print('***表格样式详见附加说明***\n')
	workbookname = input("请输入表格名称: 如('综合素质测评结果.xlsx'(无引号))\n")
	xhlie = input("\n请输学号所在列数: (从1开始数)\n")
	xfhang = input("\n请输入学分一栏所在行数: (从1开始数)\n")
	readData(workbookname, xhlie, xfhang)
	readData(workbookname, xhlie, xfhang)
	_ = input('计算结束, 按回车键退出')
