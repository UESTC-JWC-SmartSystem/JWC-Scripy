# -*- coding:utf-8 -*-
import random
import time
import requests
import re
from selenium.webdriver.common.keys import Keys

from scihub.scihub import SciHub

from scihub.scihub import SciHub
from selenium import webdriver

sh = SciHub()

# options = webdriver.ChromeOptions()
# options.add_argument(
# 	'--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
# )
# driver = webdriver.Chrome(chrome_options=options)

# baseurl = "https://sci-hub.se/"
#
# driver.get(baseurl)
# textbox = driver.find_element_by_name("request")
# textbox.send_keys("Making Agents' Abilities Explicit")
#
# open = driver.find_element_by_link_text("open")
# open.click()
#
# time.sleep(3)

download_file = 'download.txt'
notdownload_file = 'notdownload.txt'
# 论文下载网址
base_url = 'https://sci-hub.se/'


# 下载一篇论文
def download(browser, title, idx):
	# paper1: title, paper0: 编号
	browser.get(base_url)
	# browser.find_element_by_xpath('//*[@id="input"]/form/input[2]').send_keys(title)  # 输入论文title
	browser.find_element_by_name("request").send_keys(title)
	time.sleep(1)
	browser.find_element_by_xpath('//*[@id="open"]').click()  # 点击搜索按钮
	time.sleep(1)
	cur_url = browser.current_url  # 获得跳转后的网址
	
	allow_domain = r'.*sci\-hub\.se.*'  # 网址域名匹配模式
	print('cur URL:', cur_url)
	
	if re.match(allow_domain, cur_url):  # 跳转后依然在本域名内
		# print("URL Matching...")
		
		#
		# 	elem = browser.find_element_by_tag_name('body')
		# 	elem.send_keys(Keys.COMMAND, 's')
		# 	elem.send_keys("123")
		# 	elem.send_keys(Keys.ENTER)
		#
		# try:
		# 	pdf_src = browser.find_element_by_xpath('//iframe[@id="pdf"]').get_attribute('src')  # paper's pdf源地址
		# 	# 切换到iframe当中
		# 	browser.switch_to_frame(browser.find_element_by_xpath('//iframe[@id="pdf"]'))
		# 	try:
		# 		# 遇到有验证码，声音报警，并等待30秒钟以方便手动输入验证码
		# 		browser.find_element_by_xpath('/html/body/div/table/tbody/tr/td/form/input')
		# 		# winsound.PlaySound('alert', winsound.SND_ASYNC)
		# 		time.sleep(30)
		# 	except:
		# 		pass
		#
		# 	finally:
		# 		with open(download_file, 'a') as f:  # 记录已经下载的论文id
		# 			f.write("%s\n" % idx)
		# 		with open('downloads/' + idx + ' ' + title + '.pdf', 'wb') as f:  # 下载论文
		# 			f.write(requests.get(pdf_src).content)
		# 	except:
		# 	with open(notdownload_file, 'a') as f:  # 找不到论文，记录一下
		# 		f.write("%s\n" % idx)
		driver.quit()
		cur_url = str(cur_url)
		if cur_url.find("?rand=") != -1:
			cur_url = cur_url[0: cur_url.find("?rand=")]
		# print(cur_url)
		filename = title.replace(":", "")
		sh.download(cur_url, path=f"downloads/{idx} {filename}.pdf")
	
	else:  # 本网页内没有这篇论文，但链接到了论文的源头，记录其源头
		with open(notdownload_file, 'a') as f:
			f.write("%s %s\n" % (idx, cur_url))


# download(driver, "Making Agents' Abilities Explicit", "A1")
if __name__ == '__main__':
	
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
	
	for i, keyword in enumerate(keyword_list):
		if i + 1700 > 1720:
			time.sleep(3 + random.random() * 3)
			driver = webdriver.Chrome(chrome_options=options)
			download(driver, keyword, idx_list[i])
