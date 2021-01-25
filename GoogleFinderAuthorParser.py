import webbrowser

'''
	Get Author and Journal information from BibTeX.
	Author: Yuyang Qian
	E-mail: qianyy@lamda.nju.edu.cn
	2020/01/25
'''


def authorparser(bib):
	bibs = bib.split('\n')
	aus = []
	book = ""
	for ii, b in enumerate(bibs):
		b = b.strip()
		if 'author={' in b:
			# print(b.replace())
			authors = b.replace('author={', '')
			authors = authors.replace('},', '')
			authors = authors.replace('{', '')
			authors = authors.replace('}', '')
			authors = authors.replace('\\', '')
			authors = authors.replace("'", '')
			authors = authors.split(' and ')
			for a in authors:
				tmpname = ''
				if ', ' in a:
					aaa = a.split(', ')
					for i in range(len(aaa) - 1, -1, -1):
						if tmpname == '':
							tmpname = aaa[i]
						else:
							tmpname = tmpname + ' ' + aaa[i]
				else:
					tmpname = a
				aus += [tmpname]
			book = bibs[ii + 1][bibs[ii + 1].find("{") + 1:bibs[ii + 1].find("}")]
			break
	
	return aus, book


if __name__ == '__main__':
	test = """
	@article{陈玉明2019粒向量与,
	  title={粒向量与 K 近邻粒分类器},
	  author={陈玉明 and 李伟},
	  journal={计算机研究与发展},
	  volume={56},
	  number={12},
	  pages={2600},
	  year={2019}
	}
		"""
	
	# test = """
	# @inproceedings{yan2019law,
	#   title={Law Article Prediction Based on Deep Learning},
	#   author={Yan, Ge and Li, Yu and Shen, Siyuan and Zhang, Shu and Liu, Jia},
	#   booktitle={2019 IEEE 19th International Conference on Software Quality, Reliability and Security Companion (QRS-C)},
	#   pages={281--284},
	#   year={2019},
	#   organization={IEEE}
	# }
	# """
	
	aus, book = authorparser(test)
	for au in aus:
		# try:
		# 	webbrowser.open('https://www.google.com/search?q={}'.format(au))
		# except:
		# 	print('https://www.google.com/search?q={}'.format(au))
		# 	continue
		print(au)
	print(book)
