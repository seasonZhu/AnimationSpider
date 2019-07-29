""" 一些简单的格式化函数 """

# page格式化
def pageFormate(pageNum = None):
    return "&page={}".format(pageNum or 1)

# 搜索格式化
def keywordFormat(keyword):
    return "/search.php?keyword=" + keyword

# 详细url的copy-selector格式化
def detailUrlSelectFormat(index):
    return "#data_list > tr:nth-child({}) > td:nth-child(3) > a".format(index)

""" 下面是想通过搜索列表获取其文件大小 种子数量 正在下载 完成 发布者 通过lxml框架进行 """

# 列表的单个文件大小
def listSizeSelectFormat(index):
    return '//*[@id="data_list"]/tr[{}]/td[4]'.format(index)

# 列表的做种梳理 有问题
def listMakeSeedNumSelectFormat(index):
    return '//*[@id="data_list"]/tr[{}]/td[5]/span/text'.format(index)

# 列表下载数量 有问题
def listDownloadingSelectFormat(index):
    return '//*[@id="data_list"]/tr[{}]/td[6]/span/text'.format(index)

# 列表完成的数量 有问题
def listFinishedSelectFormat(index):
    return '//*[@id="data_list"]/tr[{}]/td[7]/span/text'.format(index)

# 列表发布者
def listPushSelectFormat(index):
    return '//*[@id="data_list"]/tr[{}]/td[8]/a'.format(index)

# 详细页面中的基本信息
#btm > div.main > div.slayout > div > div.c1 > div:nth-child(1) > div
# //*[@id="btm"]/div[10]/div[2]/div/div[1]/div[1]/div/p[6]/text()[1]
# //*[@id="btm"]/div[10]/div[2]/div/div[1]/div[1]/div/p[6]/text()[2]
# //*[@id="btm"]/div[10]/div[2]/div/div[1]/div[1]/div/p[6]/text()[3]
# //*[@id="btm"]/div[10]/div[2]/div/div[1]/div[1]/div/p[6]/text()[4]

#btm > div.main > div.slayout > div > div.c1 > div:nth-child(1) > div > p:nth-child(6)