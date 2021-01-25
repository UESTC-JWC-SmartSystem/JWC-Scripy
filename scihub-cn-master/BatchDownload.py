# -*- coding:utf-8 -*-
import random
import time

from scihub.scihub import SciHub
from selenium import webdriver

sh = SciHub()

keyword_list = []
idx_list = []
with open("paperlist.txt", "r", encoding='utf-8') as f:
	for line in f.readlines():
		line = line.strip('\n')  # 去掉列表中每一个元素的换行符
		# print(line)
		idx, title = line.split('\t')
		idx_list += [str(idx)]
		keyword_list += [str(title)]
print(len(keyword_list), keyword_list)
# 搜索词
# keywords = "Semi-Supervised learning with Collaborative Bagged Multi-label K-Nearest-Neighbors"

options = webdriver.ChromeOptions()
options.add_argument(
	'--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
)
driver = webdriver.Chrome(chrome_options=options)
# driver = webdriver.Chrome()

for i, keyword in enumerate(keyword_list):
	time.sleep(3 + random.random() * 3)
	
	# print("> Searching for {} {}...".format(idx_list[i], keyword))
	
	url = 'https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q={}&btnG='.format(keyword)
	driver.get(url)
	
	tit = driver.find_element_by_class_name('gs_rt')
	link = tit.find_element_by_xpath(".//a")
	paperurl = link.get_attribute('href')
	print('> paperurl:', paperurl)
	# print(link.get_property('href'))
	# print(link.text)
	
	try:
		# 搜索该关键词相关的论文，limit为篇数
		# result = sh.search(keyword, limit=1)
		# print(result)
		# for index, paper in enumerate(result.get("papers", [])):
		# 	# 批量下载这些论文
		# 	sh.download(paper["url"], path=f"downloads/{idx_list[i]} {keyword}.pdf")
		
		# sh.download(paperurl, path=f"downloads/{idx_list[i]} {keyword}.pdf")
		
		sh.download(keyword, path=f"downloads/{idx_list[i]} {keyword}.pdf")
	except:
		print("{} {}: download failed.")
	
	break
