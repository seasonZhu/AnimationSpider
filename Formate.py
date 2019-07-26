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