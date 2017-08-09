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
from spiderFarm import jf, jfe
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import urllib.request

journals = ['JFE']
urls = ['http://www.sciencedirect.com/science/journal/0304405X']
journalDict = dict(zip(journals, urls))


class spider(object):
    """
    The object of web crawler
    """
    def __init__(self, journal):
        # download path setting
        chromeOption = webdriver.ChromeOptions()
        prefs = {"download.default_directory": "/Users/gyra/Dropbox (Personal)/Python/journalSpider/JF",
                 "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}]}
        chromeOption.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(chrome_options=chromeOption)
        __journal__ = journal

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing the browser")
        browser.quit()

    def run(self):
        {
            'JF': lambda: jf(browser),
            'JFE': lambda: jfe(browser)
        }.get(__journal__, 'Do not have model for this journal yet')()

if __name__ = '__main__':
    pet = spider('JF')
    pet.run()
