# -*- coding: utf-8 -*-

"""
This is a model to get the updated articles JF

__auther__ = 'Handing Sun'
"""

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from zipfile import ZipFile
from glob import glob
# from selenium.common.exceptions import NoSuchElementException


def rfs(browser, newissue, downloaddir):
    """
    This is the function for The Review of Financial Studies
    :param browser: webdriver object
    :param downloaddir: directory for new articles
    :param newissue: new issue to be download
    :return: new download articles
    """

    def loader(browser, downloaddir):
        os.chdir(downloaddir)
        pdfs = browser.find_elements_by_class_name('item-title')
        for i in range(len(pdfs)):
            pdfs = browser.find_elements_by_class_name('item-title')
            article = pdfs[i].find_element_by_tag_name('a')
            print('Now downloading article:\n' + article.text)
            articleList.append(article.text)
            article.click()
            time.sleep(1)
            pdflink = browser.find_element_by_class_name('article-pdfLink').get_attribute('href')
            browser.get(pdflink)
            filename = pdflink.split('/')[-1]

            while not os.path.isfile(filename) and not os.path.isfile('watermark.pdf'):
                time.sleep(2)

            if os.path.isfile(filename):
                os.rename(filename, articleList[-1] + '.pdf')
            elif os.path.isfile('watermark.pdf'):
                os.rename('watermark.pdf', articleList[-1] + '.pdf')
                
            browser.back()
            time.sleep(1)

        print('Finish updating')
        return articleList

    browser.get('https://academic.oup.com/rfs/issue')
    print('Opening: ' + browser.title)

    articleList = []
    try:
        currentIssue = browser.find_element_by_xpath('//*[@id="InfoColumn"]/div/div[1]/div[2]/div[2]')
        if newissue == currentIssue.text:
            return loader(browser, downloaddir), True
        else:
            msg = 'No volume of The Review of Financial Studies: ' \
                  '' + newissue + ' is available\n' \
                                  'Do you want current available issue: ' + currentIssue.text + '? Enter: true/false: '
            if {'true': True, 'false': False, 'yes': True, 'no': False}[input(msg).lower().strip()]:
                return loader(browser, downloaddir), False
            else:
                return articleList, False
    except:
        print("Maybe the structure of RFS's web is changed")
        return articleList


def rfsnewissue(lastdate):
    """
    :param lastdate: i.e. July 2017
    :return: i.e. Auguest 2017
    """
    return datetime.strftime(datetime.strptime(lastdate, '%B %Y') + relativedelta(months=1), '%B %Y')


def jfqa(browser, newissue, downloaddir):
    """
    This is the function for Journal of Financial Quantitative Analysis
    :param browser: webdriver object
    :param newissue: new issue to be download
    :param downloaddir: directory for the downloaded zip file
    :return: new downloaded articles
    """

    def loader(browser, downloaddir):
        os.chdir(downloaddir)
        articleList = list(map(lambda x: x.text, browser.find_elements_by_class_name('part-link')))
        browser.find_element_by_xpath('//*[@id="follow"]/form/a[1]').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="downloadSelectedProductParts"]').click()
        time.sleep(2)
        WebDriverWait(browser, 25).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="confirm-modal"]/div/div[3]/div[2]/a'))).click()

        while not glob('*.zip'):
            time.sleep(2)

        with ZipFile(glob('*.zip')[0], 'r') as zip_ref:
            zip_ref.extractall(downloaddir)

        os.remove(glob('*.zip')[0])
        return articleList

    browser.get('https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/latest-issue')
    print('Opentng: ' + browser.title)

    articleList = []
    try:
        currentIssue = browser.find_element_by_xpath('//*[@id="maincontent"]/div/div[1]/div[1]/div/div[1]/h2/span[2]')
        if newissue == currentIssue.text:
            return loader(browser, downloaddir), True
        else:
            msg = 'No volume of Journal of Financial Quantitative Analysis: ' \
                  '' + newissue + ' is available\nDo you want current available issue: ' \
                                  '' + currentIssue.text + '? Enter true or false: '
            if {'true': True, 'false': False, 'yes': True, 'no': False}[input(msg).lower().strip()]:
                return loader(browser, downloaddir), False
            else:
                return articleList, False
    except:
        print("Maybe the structure of JFQA's web is changed")
        return articleList


def jfqanewissue(lastdate):
    """
    :param lastdate: i.e. June 2017
    :return: i.e. August 2017
    """
    return datetime.strftime(datetime.strptime(lastdate, '%B %Y') + relativedelta(months=2), '%B %Y')


def jf(browser, newissue, downloaddir):
    """
    This is the function for Journal of Finance
    :param browser: webdriver object
    :param newissue: new issue to be downloaded
    :param downloaddir: directory for new articles
    :return: new downloaded articles
    """

    def loader(browser, currentIssue, downloaddir):
        currentIssue.click()

        os.chdir(downloaddir)
        pdfs = browser.find_elements_by_class_name("tocArticle")
        for i in range(len(pdfs)):
            pdfs = browser.find_elements_by_class_name("tocArticle")
            article = pdfs[i].find_element_by_tag_name("a")
            print('Now downloading article:\n' + article.text)
            articleList.append(article.text)
            article.click()
            time.sleep(1)
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
            time.sleep(1)

        print('Finish updating')
        return articleList

    browser.get('http://onlinelibrary.wiley.com/journal/10.1111/(ISSN)1540-6261')
    print('Opening: ' + browser.title)

    articleList = []
    try:
        currentIssue = browser.find_element_by_xpath('//*[@id="recentIssues"]/div[2]/ul/li[1]/p[1]/a')
        if newissue == currentIssue.text:
            return loader(browser, currentIssue, downloaddir), True
        else:
            msg = 'No volume of Journal of Finance: ' \
                  '' + newissue + ' is available\nDo you want current available issue: ' \
                                  '' + currentIssue.text + '? Enter: true/false: '
            if {'true': True, 'false': False, 'yes': True, 'no': False}[input(msg).lower().strip()]:
                return loader(browser, currentIssue, downloaddir), False
            else:
                return articleList, False
    except:
        print("Maybe the structure of JF's web is changed")
        return articleList


def jfnewissue(lastdate):
    """
    :param lastdate: i.e. June 2017
    :return: i.e. August 2017
    """
    return datetime.strftime(datetime.strptime(lastdate, '%B %Y') + relativedelta(months=2), '%B %Y')


def jfe(browser, newissue, downloaddir):
    """
    This is the function for Journal of Financial Econometrics
    :param browser: webdriver object
    :param newissue: new issue to be download
    :param downloaddir: directory for the downloaded zip file
    :return: new downloaded articles
    """

    def loader(browser, downloaddir):
        browser.find_element_by_xpath('//*[@id="multiPdfIcon"]').click()
        time.sleep(1)
        os.chdir(downloaddir)
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ddm"]'))).click()
        time.sleep(1)
        articleList = list(map(lambda x: x.text, WebDriverWait(browser, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'fileName')))))

        while not glob('*.zip'):
            time.sleep(5)

        with ZipFile(glob('*.zip')[0], 'r') as zip_ref:
            zip_ref.extractall(downloaddir)

        os.remove(glob('*.zip')[0])
        return articleList

    browser.get('http://www.sciencedirect.com/science/journal/0304405X')
    print('Opening: ' + browser.title)

    articleList = []
    try:
        currentIssue = browser.find_element_by_xpath('//*[@id="volumeIssueData"]/ol/li[3]/ol/li[1]/div[1]/span[1]')
        if newissue == currentIssue.text:
            return loader(browser, downloaddir), True
        else:
            msg = 'No volume of Journal of Financial Econometrics: ' \
                  '' + newissue + ' is available\nDo you want current available issue: ' \
                                  '' + currentIssue.text + '? Enter true or false: '
            if {'true': True, 'false': False, 'yes': True, 'no': False}[input(msg).lower().strip()]:
                return loader(browser, downloaddir), False
            else:
                return articleList, False
    except:
        print("Maybe the structure of JFE's web is changed")
        return articleList


def jfenewissue(lastdate):
    """
    :param lastdate: i.e. Volume 125, Issue 3
    :return: i.e. Volume 126, Issue 1
    """
    volume = int(lastdate.split(',')[0].strip().split(' ')[1])
    issue = int(lastdate.split(',')[1].strip().split(' ')[1])
    if issue < 3:
        issue = issue + 1
    else:
        volume = volume + 1
        issue = 1
    return 'Volume ' + str(volume) + ', ' + 'Issue ' + str(issue)
