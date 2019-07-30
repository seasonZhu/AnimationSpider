import datetime

""" 搜集详细页面的信息模型,后续可根据实际需要数据的情况进行更多信息的保存 """
class DonwloadInfo:
    """ 下载对象的信息模型 """
    
    def __init__(self, title, downloadURL, date, hashValue, size):
        """ DonwloadInfo的初始化方法 """
        self.title = title
        self.downloadURL = downloadURL
        self.date = date
        self.hashValue = hashValue
        self.time = self.toTimeString(date)
        self.size = size

    # 初始化中的子函数 子函数必须写在调用之前
    def toTimeString(self, date):
        """ 时间戳转字符串的方法 """
        timeStamp = int(date)
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        return time  