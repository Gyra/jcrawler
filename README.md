# jcrawler

This is a simple web crawler to download the latest articles from several journals.
The crawler relies on Python 3.x and Selenium (Chrome webdriver)

It will check the lastVolume.txt, a utf8 JSON, to get the issue number that already be downloaded.
Then it go through the journal list to download available new issues,
and put the pdf files to target directories.

(Currently....you can not skip any issues and then pick up and fetch afterwords. In other word, you need to remember to run it on time)
(Propably will fix it when I remember it :D)
(P.S, working on it now, see updates)


Since it is based on Selenium, it is not quick, and it is just designed for personal usage, so it is not that smart too.
So, just re-engineer it to suit specific perpose.

CHANGE ALL THE DIRECTORIES(in journalcrawler.py) BEFORE USE

UPDATE: 
Adding the option that allows to download the current issue when no new issue is available
