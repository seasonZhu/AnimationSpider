""" 引入的风格参考了request 说来很巧,我自己一开始也是按照 系统 第三方 自己的顺序进行的, 没想到这个就是Python公认的引用顺序 """
import re
import os
from threading import Semaphore

import requests
from bs4 import BeautifulSoup

import Formate
import Constant
from DetailUrlProduce import DetailUrlProduce
from DetailUrlThread import DetailUrlThread
from CSVWriter import CSVWriter

""" 模块的主程序入口,启动下载 """

def searchAnimation(keyword = None, pageNum = None):
    """ 通过关键词搜索动画 返回搜索页的soup """
    if keyword == None or keyword == "" :
        keyword = "极影字幕社 鬼灭之刃"

    page = Formate.pageFormate(pageNum)
    keyword = Formate.keywordFormat(keyword)
    keywordURL = Constant.baseURL + keyword + page
    keywordResponse = requests.get(keywordURL, headers = Constant.headers)
    soup = BeautifulSoup(keywordResponse.text, Constant.htmlParser)
    htmlText = keywordResponse.text
    return (soup, htmlText)

def getSearchPageNum(keyword) -> int:
    """ 获取搜索的动画一共有多少页 """
    (soup, _) = searchAnimation(keyword = keyword)

    # 异常处理网页搜索的内容为空,直接在这里退出
    listInfos = soup.select("#data_list > tr > td")
    if len(listInfos) > 0:
        text = listInfos[0].get_text()
        if text == Constant.noResource:
            return None

    pageLastInfos = soup.select("#btm > div.main > div.pages.clear > a.pager-last.active")
    pageInfos = soup.select("#btm > div.main > div.pages.clear > a:nth-child(3)")

    if pageLastInfos == None and pageInfos == None:
        print("获取页码数量的最后一页和页码的可见的最后一页都为空")
        return None

    if len(pageLastInfos) > 0:
        """
        我在思考这种类似可选类型的方式是否可以使用
        """
        pageNum = pageLastInfos[0].get_text() or 1
        return pageNum
    elif len(pageInfos) > 0:
        pageNum = pageInfos[0].get_text() or 1
        return pageNum
    else:
        return 1

def getSearchOnePageListCount(soup) -> int:
    """ 每一页的动画列表的动画数量 """
    dataListInfos = soup.select("#data_list")
    if len(dataListInfos) == 0:
        return 0

    dataList = dataListInfos[0]
    dataText = dataList.get_text()
    # 判断资源为空不能通过dataList.contents来进行区别,以为数据为空的时候,这数组还是有值的而且大于0
    if Constant.noResource in dataText:
        return 0
    else:
        contents= dataList.contents
        del contents[0]
        count = int(len(contents) / 2)
        return count

def getAllPageListCount(soup) -> int:
    """ 搜索动画总的数量 """
    resultCountInfos = soup.select("#btm > div.main > div > h2 > span")
    resultCountText = resultCountInfos[0].get_text()
    # 使用正则获取其中的数字
    resultCounts = re.search(r"\d+",resultCountText)
    resultCount = resultCounts.group()
    return resultCount

def getDetailUrls(soup, htmlText) -> list:
    """ 获取详细的动画页面的Url """
    pageListCount = getSearchOnePageListCount(soup)
    detailUrProduce = DetailUrlProduce(soup = soup, pageListCount = pageListCount, htmlText = htmlText)
    detailUrls = detailUrProduce.getAllDetailUrls()
    return detailUrls

def searchAction(keyword, page):
    """ 搜索行为 """
    (soup, htmlText) = searchAnimation(keyword = keyword, pageNum = page)

    animationsNums = getAllPageListCount(soup)
    if animationsNums == 0 or animationsNums == None:
        print("搜索的动画结果为0或为空,请确认动画名称是否正确.")
        return

    # 获取列表中的详细信息是在主线程中解析的
    detailUrls = getDetailUrls(soup = soup, htmlText = htmlText)

    # 使用信号量控制并发的数量 并发线程太多也不是好事
    sem = Semaphore(value = 10)

    # 多线程获取详细网址列表中的信息
    detailUrlThread = DetailUrlThread(detailUrls = detailUrls, sem = sem)
    detailUrlThread.start()

    detailUrlThread.join()
    print("所有的下载完成")

    # 在主线程中进行最后的写入,这样更安全,其实并不是这样,只是这样写了而已
    writer = CSVWriter(keyword = keyword)
    writer.write(detailUrlThread.downloadInfos)

    # 下载完成后打开下载种子的文件夹
    os.system(r"open {}".format(Constant.seedFilePath))

def searchPrepare():
    """ 搜索的准备工作 """
    keyword = None
    if keyword == None:
        keyword = input("请输入动画名:")

    # 判断文件夹是否存在,如果不存在就创建一个
    if not os.path.exists(Constant.seedFilePath):
        os.makedirs(Constant.seedFilePath)

    # 将工作目录改到影片的[Seed]文件夹 用于管理种子
    os.chdir(Constant.seedFilePath)

    # 获取通过关键字搜索的页面数量
    pageNum = getSearchPageNum(keyword = keyword)

    return (keyword, pageNum)

def startSearch():
    """ 开始搜索 """
    (keyword, pageNum) = searchPrepare()

    if pageNum == None:
        print("通过关键词没有搜索到结果,是否重来一次?(输入小写的y表示重来)")
        result = input("是否重新来一次:")
        if result == "y":
           startSearch()
           return
        else:
            print("退出")
            return

    for page in range(1, int(pageNum) + 1):
        print("第{}页".format(page))
        searchAction(keyword = keyword, page = page)