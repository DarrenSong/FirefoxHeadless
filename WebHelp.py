from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as expected
import time
from bs4 import BeautifulSoup, Comment
import collections
from htmlbs import *


class WebHelp:

    __path = ''
    __url = ''
    driver = ''

    def __init__(self, path, url):
        self.__path = path
        self.__url = url

    def configWeb(self):
        firefox_options = Options()
        # firefox_options.add_argument('--headless')
        firefox_options.add_argument('-disable-gpu')
        firefox_options.add_argument('lang=zh_CN.UTF-8')
        self.driver = webdriver.Firefox(executable_path=self.__path, firefox_options=firefox_options)

    def getPage(self):
        self.driver.get(self.__url)
        # 模拟滚动
        for i in range(1, 11):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight/10*%s);" % i
            )
            time.sleep(1)
        html = self.driver.page_source.encode('utf-8')

        return html

    def reflash_web(self):
        self.driver.refresh()
        for i in range(1, 11):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight/10*%s);" % i
            )
            time.sleep(1)
        html = self.driver.page_source.encode('utf-8')

        return html

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    # firefox driver路径
    path = 'C:/Program Files/Mozilla Firefox/geckodriver'
    # 抓取的网页url
    url = "https://ds.dsproxy.net/ds_jxf01/#/game/1-3-5"
    wh = WebHelp(path, url)
    wh.configWeb()  # 配置driver
    hb = HtmlBs()
    while True:
        tm_start = time.time()

        htl = wh.getPage()  # 请求数据

        soup = hb.getSoup(htl)
        inlist = hb.getIndex(soup)  # 从请求的数据里解析期号
        nulist = hb.getNum(soup)  # 从请求的数据里解析中奖号码
        d = collections.OrderedDict()
        for i in range(len(inlist)):
            d[inlist[i]] = nulist[i]
        print(inlist)
        print(nulist)
        print(d)
        tm_end = time.time()
        tm_c = tm_end - tm_start
        print('time cost', tm_c, 's')
        wh.reflash_web()
        time.sleep(30)
