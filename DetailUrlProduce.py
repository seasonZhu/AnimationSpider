from bs4 import BeautifulSoup

import Formate
import Constant

""" 本类主要是将搜索出来的网页列表信息 获取每一列的详细网址 """
class DetailUrlProduce():
    """ 详细网址抓取器 """

    def __init__(self, soup, pageListCount):
        """ DetailUrlProduce的初始化方法 """
        super().__init__()
        self.soup = soup
        self.pageListCount = pageListCount

    def getAllDetailUrls(self):
        """ 获取所有的详细页面的Url 返回一个url数组 """
        print("一页的数量{}".format(self.pageListCount))
        detailUrls = []
        for index in range(1, self.pageListCount + 1):
            detailUrl = Constant.baseURL + self.soup.select(Formate.detailUrlSelectFormat(index))[0].get("href")
            print(detailUrl)
            detailUrls.append(detailUrl)
        return detailUrls
