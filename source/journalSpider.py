# -*- coding: utf-8 -*-

"""
This is a spider to get the updated articles from journals, i.e.
JF, JFE, JFQA, RFS, Econometrica, JASA

__auther__ = 'Handing Sun'
"""

import re
import time
from selenium import webdriver
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import urllib.request

os.chdir("/Users/gyra/Dropbox (Personal)/Python/journalSpider/JF")

journals = ['JF', 'JFE']
urls = ['http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6261', 'http://www.sciencedirect.com/science/journal/0304405X?sdc=1']
journalDict = dict(zip(journals, urls))

# download path setting
chromeOption = webdriver.ChromeOptions()
prefs = {"download.default_directory": "/Users/gyra/Dropbox (Personal)/Python/journalSpider/JF",
         "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}]}
chromeOption.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(chrome_options=chromeOption)

browser.get(journalDict['JF'])
print('Opening: ' + browser.title)

currentIssue = browser.find_element_by_link_text('February 2017')
currentIssue.click()

articleList = []
pdfs = browser.find_elements_by_class_name("tocArticle")
for i in range(2, len(pdfs)-3):
    pdfs = browser.find_elements_by_class_name("tocArticle")
    article = pdfs[i].find_element_by_tag_name("a")
    print('Now downloading article:\n' + article.text)
    articleList.append(article.text)
    article.click()
    pdflinks = browser.find_elements_by_class_name("js-article-section__pdf-container-link")
    pdflink = pdflinks[1].get_attribute("href")
    browser.get(pdflink)
    print('___________start downloading____________')
    rawname = pdflink.split("/")
    filename = rawname[-2].replace(".", "") + "." + rawname[-1]
    flag = False
    while not flag:
        time.sleep(2)
        flag = os.path.isfile(filename)

    os.rename(filename, articleList[-1] + ".pdf")
    browser.back()

print(articleList)
browser.quit()
