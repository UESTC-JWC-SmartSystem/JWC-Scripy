from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
time.sleep(15)
# kes = driver.find_elements_by_xpath("//a[@class='lessonListOperator']")
kes = driver.find_elements_by_class_name('lessonListOperator')
print(kes)
builder = ActionChains(driver)
times = 1
while True:
	for ke in kes:
		time.sleep(0.5)
		ke.click()
		print(times)
		times += 1
		time.sleep(0.5)
		builder.key_down(Keys.ENTER).perform()
		time.sleep(0.5)
		builder.key_down(Keys.ESCAPE).perform()
