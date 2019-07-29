from bs4 import BeautifulSoup
from lxml import etree

import Formate
import Constant

""" 本类主要是将搜索出来的网页列表信息 获取每一列的详细网址 """
class DetailUrlProduce():
    """ 详细网址抓取器 """

    def __init__(self, soup, pageListCount, htmlText):
        """ DetailUrlProduce的初始化方法 """
        super().__init__()
        self.soup = soup
        self.pageListCount = pageListCount
        self.htmlText = htmlText

    def getAllDetailUrls(self):
        """ 获取所有的详细页面的Url 返回一个url数组 """
        print("一页的数量{}".format(self.pageListCount))
        detailUrls = []
        for index in range(1, self.pageListCount + 1):
            detailUrl = Constant.baseURL + self.soup.select(Formate.detailUrlSelectFormat(index))[0].get("href")
            print(detailUrl)
            detailUrls.append(detailUrl)
            self.getListInfo(index = index)
        return detailUrls

    def getListInfo(self, index):
        selector = etree.HTML(self.htmlText)
        size = selector.xpath(Formate.listSizeSelectFormat(index))[0].text
        makeSeedNum = selector.xpath(Formate.listMakeSeedNumSelectFormat(index))
        downloading = selector.xpath(Formate.listDownloadingSelectFormat(index))
        finished = selector.xpath(Formate.listFinishedSelectFormat(index))
        push = selector.xpath(Formate.listPushSelectFormat(index))[0].text
        print(size, makeSeedNum, downloading, finished, push)