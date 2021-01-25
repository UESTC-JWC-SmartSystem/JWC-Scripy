from selenium import webdriver
import time
addN = [22.554515, 22.549734, 22.584194, 22.57326, 22.624308, 22.630545, 22.565104, 22.564871, 22.587862, 22.597802,
		22.618156, 22.615467, 22.588758, 22.589449, 22.582337, 22.589878, 22.603579, 22.60635]
addE = [113.908382, 113.912108, 113.90963, 113.920045, 113.939123, 113.935135, 114.017562, 114.017159, 114.054716,
		114.048826, 114.09556, 114.096193, 114.112716, 114.112702, 114.117852, 114.114349, 114.165255, 114.16387]
driver = webdriver.Chrome()
url = 'https://www.google.com/maps/'
i = 0
# for i in range(0, len(addE)):
driver.get(url)
address = driver.find_element_by_xpath("//input[@id='searchboxinput']")
inputstr = str(addE[i]) + '°E' + ' ' + str(addN[i]) + '°N'
address.send_keys(inputstr)
confirm = driver.find_element_by_xpath("//button[@id='searchbox-searchbutton']")
confirm.click()
driver.implicitly_wait(15)
nearby = driver.find_element_by_xpath("//div[@class='section-action-button-icon maps-sprite-pane-action-ic-searchnearby']")
nearby.click()
time.sleep(3)
address.send_keys('小区')
confirm.click()
time.sleep(5)

results = driver.find_elements_by_class_name('section-result-text-content')
re1 = []
re2 = []
for j in range(len(results)):
	tmp = str(results[j].get_attribute('innerText'))
	tmp = tmp[:-1]
	tmp1 = tmp[:tmp.find('\n')]
	tmp2 = tmp[tmp.find('\n') + 1:]
	re1 += [tmp1]
	re2 += [tmp2]
	# print(results[j].get_attribute('innerText'))
# print(re)
print(str(i+1) + '	', end='')
print("	".join(str(k) for k in re1))
print("	", end='')
print("	".join(str(k) for k in re2))
# driver.save_screenshot(str(i + 1) + '.png')