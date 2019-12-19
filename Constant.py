""" 保存常量,注意的是seedFilePath需要根据自己的电脑系统进行适当的调整,并且文件夹下面不要再创建子文件夹 """
import os

# 基本网址 这两个网址的是同一个系统写的,所以爬起来一模一样
baseURL = "http://www.acgsou.com/"#"https://www.36dm.com/"#

# 请求头
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}

# 工作目录
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件夹名称路径
workFolderPath = "[Animation Seed]"

# 不同的系统,请对其进行修改
seedFilePath = "/Users/season/Movies/[Seed]"

def getDefaultSeedFilePath():
    """ 该函数是默认的使用工程的父目录作为种子下载的存储路径,如果上面的seedFilePath不会配置,直接调用该函数 """
    return os.path.join(path, workFolderPath)