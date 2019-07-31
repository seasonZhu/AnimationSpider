import csv
import datetime

import Constant

def singleton(cls, *args, **kwargs):
    """ 单例方法 """
    instances = {}
    
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

#@singleton
class CSVWriter():
    def __init__(self, keyword):
        """ csv写入器 """
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        keyword = keyword.replace("/", "_")
        self.csvFile = Constant.seedFilePath + "/{}".format(keyword) + "_" + time + ".csv"

    def write(self, downloadInfos):
        """ 写入的方法 """
        if len(downloadInfos) == 0 or downloadInfos == None:
            return

        for info in downloadInfos:
            with open (self.csvFile, "a+") as fp:
                writer = csv.writer(fp)
                writer.writerow((info.title, info.downloadURL, info.time, info.hashValue, info.size))

        