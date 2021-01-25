import requests
import uestc
from bs4 import BeautifulSoup

ssion = uestc.login("2016010909009", "yy19980803")
# uestc.query.get_picture(ssion)
re = uestc.query.get_score(ssion, "183")
print(re)