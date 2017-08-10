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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from zipfile import ZipFile
from glob import glob


def jf(browser, newissue):
    """
    This is the function for Journal of Finance
    :param browser: webdriver object
    :param newissue: new issue to be downloaded
    :return: new downloaded articles
    """

    browser.get('http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6261')
    print('Opening: ' + browser.title)

    articleList = []
    try:
        currentIssue = browser.find_element_by_xpath('//*[@id="recentIssues"]/div[2]/ul/li[1]/p[1]/a')
        if newissue == currentIssue.text:
            currentIssue.click()
        else:
            print('No volume of JF: ' + newissue + ' is available')
            return articleList
    except NoSuchElementException:
        print("Maybe the structure of JF's web is changed")
        return articleList


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

        while not os.path.isfile(filename):
            time.sleep(2)

        os.rename(filename, articleList[-1] + ".pdf")
        browser.back()

    print('Finish updating')
    browser.quit()
    return articleList


def jfnewissue(lastdate):
    return datetime.strftime(datetime.strptime(lastdate, '%B %Y') + relativedelta(months=2), '%B %Y')


def jfe(browser, newissue, downloaddir):
    """
    This is the function for Journal of Financial Econometrics
    :param browser: webdriver object
    :param newissue: new issue to be download
    :return: new downloaded articles
    """

    browser.get('http://www.sciencedirect.com/science/journal/0304405X')
    print('Opening: ' + browser.title)

    articleList = []
    try:
        currentIssue = browser.find_element_by_xpath('//*[@id="volumeIssueData"]/ol/li[3]/ol/li[1]/div[1]/span[1]')
        if newissue == currentIssue.text:
            currentIssue.click()
        else:
            print('No volume of JFE: ' + newissue + ' is available')
            return articleList
    except NoSuchElementException:
        print("Maybe the structure of JFE's web is changed")
        return articleList

    pdfslink = browser.find_element_by_xpath('//*[@id="multiPdfIcon"]')
    pdfslink.click()

    os.chdir(downloaddir)
    downloadbutton = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ddm"]'))).click()
    articleList = list(map(lambda x: x.text, WebDriverWait(browser, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'fileName')))))

    while not glob('*.zip'):
        time.sleep(5)

    with ZipFile(glob('*.zip')[0], 'r') as zip_ref:
        zip_ref.extractall(downloaddir)

    os.remove(glob('*.zip')[0])
    return articleList


def jfenewissue(lastdate):
    volume = int(lastdate.split(',')[0].strip().split(' ')[1])
    issue = int(lastdate.split(',')[1].strip().split(' ')[1])
    if issue <= 3:
        issue = issue + 1
    else:
        volume = volume + 1
        issue = 1
    return 'Volume ' + str(volume) + ', ' + 'Issue ' + str(issue)
