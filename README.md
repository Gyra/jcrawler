# jcrawler

This is a simple web crawler to download the latest articles from several journals.
The crawler relies on Python 3.x and Selenium (Chrome webdriver)

It will check the lastVolume.txt, a utf8 JSON, to get the issue number that already be downloaded.
Then it go through the journal list to download available new issues,
and put the pdf files to target directories.

Since it is based on Selenium, it is not quick, and it is just designed for personal usage, so it is not that smart too.
So, just re-engineer it to suit specific perpose.

Setup of Selenium and Chrome webdriver please refer to the official documents. If webdriver is installed in directory other than default `/usr/local/bin` or `/usr/bin`(Mac), please change corresponding code in `journalspider.py`

CHANGE ALL THE DIRECTORIES(in journalcrawler.py) BEFORE USE (including one source dir and 4 journal dir)

先配置好`Chrome webdriver`的路径，这里默认放在了`/usr/local/bin`或者`/usr/bin`（Mac）， 如果在别的地方，要在`journalspider.py`里加指示。

pdf有四个路径，还有一个源文件路径要改成本地的

UPDATE: 
Adding the option that allows to download the current issue when no new issue is available

***
【其实我是在试github怎么用啊哈哈哈
