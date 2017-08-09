# -*- coding: utf-8 -*-

"""
This is a model to get the updated articles JF

__auther__ = 'Handing Sun'
"""

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from selenium.common.exceptions import NoSuchElementException


def jf(browser, newissue):
    """
    This is the function for Journal of Finance
    :param browser: webdriver object
    :param newissue: new issue to be downloaded
    :return: new downloaded articles
    """

    browser.get('http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6261')
    print('Opening: ' + browser.title)

    currentIssue = browser.find_element_by_link_text(newissue)
    currentIssue.click()

    articleList = []
    pdfs = browser.find_elements_by_class_name("tocArticle")
    for i in range(1, len(pdfs)):
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

    print('Finish updating')
    browser.quit()
    return articleList


def jfnewissue(lastdate):
    return datetime.strftime(datetime.strptime(lastdate, '%B %Y') + relativedelta(months=2), '%B %Y')
