# -*- coding: utf-8 -*-

"""
This is a model to get the updated articles JF

__auther__ = 'Handing Sun'
"""

import time
from selenium import webdriver
import os


def jf(browser):
    os.chdir("/Users/gyra/Dropbox (Personal)/Python/journalSpider/JF")
    browser.get('http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6261')
    print('Opening: ' + browser.title)

    currentIssue = browser.find_element_by_link_text('December 2016')
    currentIssue.click()

    articleList = []
    pdfs = browser.find_elements_by_class_name("tocArticle")
    for i in range(2, len(pdfs) - 3):
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