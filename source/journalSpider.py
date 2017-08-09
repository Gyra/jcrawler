# -*- coding: utf-8 -*-

"""
This is a spider to get the updated articles from journals, i.e.
JF, JFE, JFQA, RFS, Econometrica, JASA

__auther__ = 'Handing Sun'
"""
from spiderFarm import jf#, jfe
from selenium import webdriver
# import re
# import time
# import os
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup as bs
# import urllib.request

journals = ['JFE']
urls = ['http://www.sciencedirect.com/science/journal/0304405X']
journalDict = dict(zip(journals, urls))


class spider(object):
    """
    The object of web crawler
    """
    def __init__(self, journal):
        # download path setting
        self.chromeOption = webdriver.ChromeOptions()
        self.prefs = {"download.default_directory": "/Users/gyra/Dropbox (Personal)/Python/journalSpider/JF",
                 "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}]}
        self.chromeOption.add_experimental_option("prefs", self.prefs)
        self.browser = webdriver.Chrome(chrome_options=self.chromeOption)
        self.__journal__ = journal

    def run(self):
        return {
            'JF': lambda: jf(self.browser),
            'JFE': lambda: jfe(self.browser)
        }.get(self.__journal__, 'Do not have model for this journal yet')()

if __name__ == '__main__':
    pet = spider('JF')
    articleList = pet.run()
    print("\n".join(articleList))


