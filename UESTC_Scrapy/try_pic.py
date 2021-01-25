from selenium import webdriver
import pytesseract
import time
import sys, os
import copy
from PIL import Image, ImageDraw
import numpy

# 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
# 该函数也可以改成RGB判断的,具体看需求如何
def getPixel(image, x, y, G, N):
	nearDots = 0
	if (image.getpixel((x - 1, y - 1)) < G):
		nearDots += 1
	if (image.getpixel((x - 1, y)) < G):
		nearDots += 1
	if (image.getpixel((x - 1, y + 1)) < G):
		nearDots += 1
	if (image.getpixel((x, y - 1)) < G):
		nearDots += 1
	if (image.getpixel((x, y + 1)) < G):
		nearDots += 1
	if (image.getpixel((x + 1, y - 1)) < G):
		nearDots += 1
	if (image.getpixel((x + 1, y)) < G):
		nearDots += 1
	if (image.getpixel((x + 1, y + 1)) < G):
		nearDots += 1

	if nearDots >= N:
		return True
	else:
		return False

def clearNoise(image, G, N, Z):
	image2 = copy.deepcopy(image)
	draw = ImageDraw.Draw(image2)

	for x in range(1, image.size[0] - 1):
		for y in range(1, image.size[1] - 1):
			draw.point((x, y), 255)
	for i in range(0, Z):
		for x in range(1, image.size[0] - 1):
			for y in range(1, image.size[1] - 1):
				if getPixel(image, x, y, G, N):
					draw.point((x, y), 0)

	return image2



def getverify1(name):
	im = Image.open(name)
	imgry = im.convert('L')
	im = clearNoise(imgry, 100, 3, 8)
	im.save('g2' + name)
	return pytesseract.image_to_string(im, lang='eng', config='-psm 7')

driver = webdriver.Chrome()
url = 'http://241374.yichafen.com/public/queryscore/sqcode/MsTcInwmMzAxfDViN2E2MGQwNTVkM2UO0O0O.html'
driver.maximize_window()
driver.implicitly_wait(2)
driver.get(url)
driver.implicitly_wait(2)
driver.refresh()
# rangle = (1440, 490, 1545, 530)		# 2k, 150%
rangle = (1485, 655, 1630, 710)		# 2k, 200%
str = ''
driver.save_screenshot('verify.png')
row = Image.open('verify.png')
frame = row.crop(rangle)

frame.save('frame.png')
print(getverify1('frame.png'))
str = getverify1('frame.png')
print(str)
while len(str) != 4:
	driver.implicitly_wait(2)
	reset = driver.find_element_by_xpath('//input[@id="reset"]')
	reset.click()
	driver.implicitly_wait(2)
	driver.save_screenshot('verify.png')
	row = Image.open('verify.png')
	frame = row.crop(rangle)
	frame.save('frame.png')
	str = getverify1('frame.png')
	print(str)
