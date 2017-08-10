# -*- coding: utf-8 -*-

"""
This is a spider to get the updated articles from journals, i.e.
JF, JFE, JFQA, RFS, Econometrica, JASA

__auther__ = 'Handing Sun'
"""
import spiderFarm
from selenium import webdriver
import os
import json
# import re
# import time
# from bs4 import BeautifulSoup as bs
# import urllib.request


class Spider(object):
    """
    The object of web crawler
    """
    def __init__(self, journal, lastdate):
        # download path setting
        self.chromeOption = webdriver.ChromeOptions()
        self.downloaddir = {
            'JF': "/Users/gyra/Dropbox (Personal)/Python/journalSpider/JF",
            'JFE': "/Users/gyra/Dropbox (Personal)/Python/journalSpider/JFE",
            'JFQA': "/Users/gyra/Dropbox (Personal)/Python/journalSpider/JFQA"
        }.get(journal, "/Users/gyra/Dropbox (Personal)/Python/journalSpider/other")
        self.prefs = {"download.default_directory": self.downloaddir,
                      "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}]}
        self.chromeOption.add_experimental_option("prefs", self.prefs)
        self.browser = webdriver.Chrome(chrome_options=self.chromeOption)
        self.__journal__ = journal
        self.__lastdate__ = lastdate

    def run(self):
        return {
            'JF': lambda: spiderFarm.jf(self.browser, spiderFarm.jfnewissue(self.__lastdate__)),
            'JFE': lambda: spiderFarm.jfe(self.browser, spiderFarm.jfenewissue(self.__lastdate__),
                                          self.downloaddir),
            'JFQA': lambda: spiderFarm.jfqa(self.browser, spiderFarm.jfqanewissue(self.__lastdate__),
                                            self.downloaddir)
        }.get(self.__journal__, lambda: print('Do not have model for this journal yet'))()

    def kill(self):
        print('Mission completed')
        self.browser.quit()

if __name__ == '__main__':
    print(os.getcwd())
    journals = []
    lastdates = []
    with open('lastVolume.txt', 'r') as f:
        Dict = json.load(f)

    pet = Spider('JFQA', Dict['JFQA']) ##############TO BE CHANGED####################
    articleList = pet.run()
    print("\n".join(articleList))
    Dict['JFQA'] = {
        'JF': lambda: spiderFarm.jfnewissue(Dict('JF')),
        'JFE': lambda: spiderFarm.jfenewissue(Dict('JFE')),
        'JFQA': lambda: spiderFarm.jfqanewissue(Dict('JFQA'))
    }.get('JFQA')()
    with open('lastVolume.txt', 'w') as f:
        f.write(json.dumps(Dict))

    pet.kill()


