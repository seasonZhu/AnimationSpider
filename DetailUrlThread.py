from threading import Thread
import re

from bs4 import BeautifulSoup
import requests
from lxml import etree

from DonwloadInfo import DonwloadInfo
from DownloadThread import DownloadThread
import Formate
import Constant

""" 通过详细网址爬取详细网页信息进而启动下载 """
class DetailUrlThread(Thread):
    """ 爬取详细网址信息的线程 """

    def __init__(self, detailUrls, sem):
        """ DetailUrlThread的初始化方法 """
        super().__init__()
        self.detailUrls = detailUrls
        self.sem = sem

    def run(self):
        """ 重写run方法 """
        for detailUrl in self.detailUrls:
            downloadInfo = self.getDownloadInfo(detailUrl = detailUrl)
        
            # 开始信号量锁
            self.sem.acquire()

            # 多线程开始下载
            self.startDownload(downloadInfo = downloadInfo)
            
    def startDownload(self, downloadInfo):
        """ 通过DonwloadInfo模型中的数据进行下载 """
        name = downloadInfo.title + ".torrent"
        downloadThread = DownloadThread(downloadInfo = downloadInfo, name = name, sem = self.sem)
        downloadThread.start()

    def getDownloadInfo(self, detailUrl):
        """ 获取单个文件的信息 """
        detailResponse = requests.get(detailUrl)
        soup = BeautifulSoup(detailResponse.text, "html.parser")
        
        downloadInfos = soup.select("#download")
        href = downloadInfos[0].get("href")
        downloadUrl = Constant.baseURL + href
        '''
        href的格式:
        down.php?date=1556390414&hash=d8e9125797a795c6888e62b6f952b5d6e38265ba
        '''
        # 通过soup获取title
        title = self.getDetailUrlOfTitle(soup)

        # 通过字符串分割获取时间戳和哈希值
        dateAndHash = href.split(sep = "?")[1]

        # 获取时间戳
        date = self.getDetailUrlOfDate(dateAndHash)

        # 获取哈希值
        hashValue = self.getDetailUrlOfHashValue(dateAndHash)

        # 获取文件大小
        size = self.getDetailUrlOfSize(soup)

        # 获取字符串的基本信息
        #basicInfo = self.getDetailUrlOfBasicInfo(detailResponse.text, soup)

        # 生成下载信息模型
        downloadInfo = DonwloadInfo(title, downloadUrl, date, hashValue, size)

        return downloadInfo

    def getDetailUrlOfTitle(self, soup):
        """ 获取详细页面的标题 """
        text = soup.select("#btm > div.main > div.slayout > div > div.c2 > div:nth-child(3) > div.torrent_files > ul > li")[0].get_text()
        # 对于桜都奇葩的命名做特殊处理 
        # 桜都的实在太奇葩 我没有办法做特别好的处理 除非写一个很好的正则表达
        if text.find("[Sakurato.sub]"):
            text = text.replace("[Sakurato.sub]","[Sakurato]")
            title = text.split(sep = ".")[0]
        else:
            title = text.split(sep = ".")[0]
        # 从字符串的右边开始 获取第一次得到"."的位置信息进行切片 也没有解决这个问题
        # rIndex = text.rindex(".")
        # Title = text[:rIndex]
        return title

    def getDetailUrlOfSize(self, soup):
        """ 获取详细页面的文件大小 """
        text = soup.select("#btm > div.main > div.slayout > div > div.c2 > div:nth-child(3) > h2 > span.right.text_normal")[0].get_text()
        sizeText = text.split(sep = "，")[1]
        size = sizeText.split(sep = "：")[1]

        # 这里使用正则表达式获取不到 单位 其实可以用写一个合理的正则去表示
        #sizes = re.search(r"\d+",sizeText)
        #size = sizes.group()
        return size

    def getDetailUrlOfDate(self, dateAndHash):
        """ 获取详细页面的种子时间戳 """
        date = dateAndHash.split(sep = "&")[0].split(sep = "=")[1]
        return date

    def getDetailUrlOfHashValue(self, dateAndHash):
        """ 获取详细页面的种子的哈希值 """
        hashValue = dateAndHash.split(sep = "&")[1].split(sep = "=")[1]
        return hashValue

    def getDetailUrlOfBasicInfo(self, htmlText, soup):
        """ 获取详细页面的基本信息 """
        selector = etree.HTML(htmlText)
        string = selector.xpath('//*[@id="btm"]/div[10]/div[2]/div/div[1]/div[1]/div/p[6]/text()')
        info = soup.select("#btm > div.main > div.slayout > div > div.c1 > div:nth-child(1) > div > p:nth-child(6)")[0].get_text()
        return (string, info)
