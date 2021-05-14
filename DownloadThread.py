from threading import Thread
import os

import requests

from DonwloadInfo import DonwloadInfo
import Constant

""" 通过下载信息进行下载 """
class DownloadThread(Thread):
    """ 下载的线程 """
    def __init__(self, downloadInfo, name, sem):
        """ DownloadThread的初始化方法 """
        super().__init__()
        self.downloadInfo = downloadInfo
        self.name = name
        self.sem = sem

        for _, _, files in os.walk(Constant.seedFilePath):  
            self.seedFiles = files

    def run(self):
        """ 重写run方法 """
        # 如果已经包含了就不用下载了 注意[Seeds]文件夹下面不要再有文件夹了 否则会读更深的文件夹 就不会遍历[Seeds]文件夹下面的文件而是其子文件夹的文件
        if self.name in self.seedFiles:
            print("已有{}种子文件,直接返回".format(self.name))
        else:
            print("异步获取下载信息: {}, 准备开始下载".format(self.downloadInfo.title))
            self.download(self.downloadInfo.downloadURL, self.name)

        # 解开信号锁
        self.sem.release()

    def download(self, downloadURL, name):
        """ 进行下载请求 """
        response = requests.post(downloadURL, headers = Constant.headers)
        data = response.content
        self.write(name = name, data = data)
        
    def write(self, name, data):
        """ data二进制写入,保存为种子 """
        # 使用try except else finaly 进行异常捕获, 先运行try里面的代码,如果捕获到异常则走except中的代码,否则走else,最后不管是走expect还是else最终都会走到finally中
        try:
            with open(name,"wb") as f:
                f.write(data)
        except FileNotFoundError as error:
            message = "FileNotFoundError. Sorry, the file" + name + "does not exit"
            print(message,error)
        else:
            message = name + " download success!"
            print(message)
        finally:
            pass