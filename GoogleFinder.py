import time
import webbrowser
import os
from selenium import webdriver
from datetime import datetime
from GoogleFinderAuthorParser import authorparser

options = webdriver.ChromeOptions()
options.add_argument(
	'--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
)
# options.add_argument('--headless')
# options.add_argument("--start-maximized")

# driver = webdriver.Chrome()

driver = webdriver.Chrome(chrome_options=options)
# driver.minimize_window()

while True:
	title = input("> Input paper's title: ")
	title = title.strip()
	if title == '': continue
	
	# try:
	url = 'https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q={}&btnG='.format(title)
	try:
		webbrowser.open(url)
	except:
		print(url)
	driver.get(url)
	
	print('> Finding Citing... {}'.format(datetime.now()))
	cite = driver.find_elements_by_class_name('gs_or_svg')
	cite[1].click()
	
	time.sleep(2)
	
	#### Needless
	# bibtex = driver.find_element_by_link_text('BibTeX')
	# bibtex.click()
	# bibtex = driver.find_elements_by_class_name('gs_citi')
	# print(len(bibtex))
	# bibtex[1].click()
	
	print('> Finding Bibtex... {}'.format(datetime.now()))
	
	while True:
		try:
			cites = driver.find_element_by_id('gs_citi')
			bibtex = cites.find_element_by_xpath(".//a[1]")
			bibtex.click()
			break
		except:
			time.sleep(2)
	
	aus = []
	trytimes = 0
	while trytimes <= 2:
		time.sleep(2)
		# bib = str(driver.page_source)
		# bibs = bib.split('\n')
		# for b in bibs:
		# 	b = b.strip()
		# 	if 'author={' in b:
		# 		# print(b.replace())
		# 		authors = b.replace('author={', '')
		# 		authors = authors.replace('},', '')
		# 		authors = authors.replace('{', '')
		# 		authors = authors.replace('}', '')
		# 		authors = authors.replace('\\', '')
		# 		authors = authors.replace("'", '')
		# 		authors = authors.split(' and ')
		# 		for a in authors:
		# 			tmpname = ''
		# 			if ', ' in a:
		# 				aaa = a.split(', ')
		# 				for i in range(len(aaa) - 1, -1, -1):
		# 					if tmpname == '':
		# 						tmpname = aaa[i]
		# 					else:
		# 						tmpname = tmpname + ' ' + aaa[i]
		# 			aus += [tmpname]
		# 		break
		aus, book = authorparser(str(driver.page_source))
		if len(aus) == 0:
			print('> Finding Bibtex failed, retrying...')
			trytimes += 1
			driver.refresh()
		else:
			break
	
	print('> Finished. Authors are:')
	
	print(aus[0] + '\t' * 7 + book)
	for ii in range(1, len(aus)):
		print(aus[ii])
	print('\n')
	
	clipaus = '\n'.join([str(i) for i in aus])
	# data = "hello world"
	
	os.system("echo '%s' | pbcopy" % clipaus)
	
	for au in aus:
		# new = 'window.open("https://www.google.com/search?q={}");'.format(au)
		# driver.execute_script(new)
		
		try:
			webbrowser.open('https://www.google.com/search?q={}'.format(au))
		except:
			print(
				'https://www.google.com/search?q={}'.format(au))  # Can not open website beacuse of the "UTF-8 Encoding"
			continue
# except:
# 	print('Some thing went wrong, please try again.')
