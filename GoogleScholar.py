# -*- coding:utf-8 -*-
# Author: Yuyang Qian
# E-mail: qianyy@lamda.nju.edu.cn
# 2020/01/23

from selenium import webdriver
import time
import random

options = webdriver.ChromeOptions()
options.add_argument(
	'--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
)
driver = webdriver.Chrome(chrome_options=options)

driver.get(
	'https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%2C5&sciodt=0%2C5&cites=18033016632353916230%2C8169143659367785069%2C9531422230648007638%2C12889020650932489309%2C4177478703400227684%2C10756183883336767069%2C851381508492614013%2C17963738474200527518%2C1712486865046005197%2C11179168796140083353%2C1520485412061122499&scipsc=&as_ylo=2019&as_yhi=2019'
)


def hash(title, author):  # Ensure that the output is not repeated
	return str(title) + ', ' + str(author)


art_list = []
print('\n\n')

for i in range(1000):
	results = driver.find_elements_by_class_name('gs_rt')
	for re in results:
		try:
			rep = re.find_element_by_xpath("..")  # parent of re
			author = rep.find_element_by_class_name("gs_a")  # find author information
			
			if hash(re.text, author.text) not in art_list:  # Ensure that the output is not repeated
				print('{}\t{}'.format(re.text, author.text))  # Output the results in the command line.
			art_list += [hash(re.text, author.text)]
		except:  # Can't find author information
			authortxt = 'No Author Information'
			
			if hash(re.text, authortxt) not in art_list:  # Ensure that the output is not repeated
				print('{}\t{}'.format(re.text, authortxt))  # Output the results in the command line.
			art_list += [hash(re.text, authortxt)]
	
	try:
		next_page = driver.find_element_by_link_text("下一页")  # Click the "Next Page" Button
		next_page.click()
		time.sleep(3 + random.random() * 3)  # Random Sleep 3~6s
	except:
		break  # Programme finished, or encounter Man-machine verification
