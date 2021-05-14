from multiprocessing.pool import Pool
from pyquery import PyQuery as pq
from decimal import *
from pymongo import MongoClient
import requests
import json


'''爬虫函数'''
headers = {
    'Cookie': 
'antipas=055q44g56yx8C7g3d9E511541I; uuid=98a1c52c-9028-4d03-87c4-6cadd5154669; cityDomain=sjz; clueSourceCode=%2A%2300; user_city_id=1; ganji_uuid=9641587977218796738126; sessionid=ee95e085-bddc-4618-9f2e-3b5149751c57; lg=1; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2298a1c52c-9028-4d03-87c4-6cadd5154669%22%2C%22ca_city%22%3A%22wh%22%2C%22sessionid%22%3A%22ee95e085-bddc-4618-9f2e-3b5149751c57%22%7D; preTime=%7B%22last%22%3A1604303935%2C%22this%22%3A1604303874%2C%22pre%22%3A1604303874%7D',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

datas = []

def get_page(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    doc = pq(response.text)
    ul = doc('.carlist.clearfix.js-top')
    links = ul.find('a')
    
    for link in links:
        name = pq(link)('h2').text()
        img = pq(link)('img').attr('src')
        msg = pq(link)('.t-i').text()
        year = msg.split('|')[0]
        distance = msg.split('|')[1]
        now_price = pq(link)('.t-price p').text()
        original_price = pq(link)('.t-price em').text()
        if len(original_price) == 0:
            original_price = now_price
        discount = Decimal(now_price.replace('万', ''))*100/Decimal(original_price.replace('万', ''))
        discount_str = str(Decimal(discount).quantize(Decimal('0.00')))+'%'
        dict ={
           'name': name,
           'img': img,
           'year': year,
           'distance': distance,
           'now_price': now_price,
           'original_price': original_price,
           'discount': discount_str
        }
        datas.append(dict)
        print(json.dumps(dict, ensure_ascii=False))

def dataBaseSave(datas):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["guazi_ershouche"]
    mydb.insert_many(datas)

'''图表显示'''
from matplotlib import pyplot as plt
# 获取数据
def get_mongo_datas():
    datas = collection.find({})
    return datas
# 给条形图上方加上纵坐标的值
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, height+0.01*height, height, ha='center',  va='bottom')
        rect.set_edgecolor('white')
# 生成二维柱状条形图
def create_two_dimensional_diagram(datas):
    price_5 = 0
    price_10 = 0
    price_20 = 0
    price_20_plus = 0
    for data in datas:
        price = Decimal(data.get('now_price').replace('万', ''))
        if price < 5:
            price_5 += 1
        elif price >= 5 and price < 10:
            price_10 += 1
        elif price >= 10 and price < 20:
            price_20 += 1
        else:
            price_20_plus += 1
    price_y = [price_5, price_10, price_20, price_20_plus]
    price_x = ['0~5', '5~10', '10~20', '20+']
    plt.rcParams['font.sans-serif'] = ['Hei']
    rects = plt.bar(price_x, price_y, align='center')
    # 在直方图上加上纵坐标的值
    add_labels(rects)
    plt.title('价格-数量关系图')
    plt.ylabel('数量(辆)')
    plt.xlabel('价格(万)')
    plt.show()

'''词云显示'''
import jieba
from wordcloud import WordCloud

def create_wordCloud(datas):
    names = []
    for data in datas:
        names.append(data.get('name').replace(' ',''))
    big_name = ''.join(names)
    wl = jieba.lcut(big_name, cut_all=True)
    wl_space_split = ' '.join(wl)
    stopwords = ['豪华', '豪华型', '豪华版', '自动', '精英'
                 , '舒适', '舒适版', '进口'
                 , 'OL', '运动', '运动版'
                 , '舒适型', 'VI', 'OT','CVT']
    wc = WordCloud(background_color='white',  # 背景颜色
                   width=1000,
                   height=600,
                   stopwords=stopwords).generate(wl_space_split)
    wc.to_file('%s.png' % 'SUV2')

'''主函数'''
if __name__ == '__main__':
    # pool = Pool(3)
    # group = ([f'https://www.guazi.com/sjz/buy/o{x}h2n2/#bread' for x in range(1, 51)])
    # pool.map(get_page, group)
    # pool.close()
    # pool.join()

    for x in range(1, 51):
        get_page(f'https://www.guazi.com/sjz/buy/o{x}h2n2/#bread'.format(x))

    # 数据库保存
    #dataBaseSave(datas=datas)
    
    # 柱状图
    create_two_dimensional_diagram(datas=datas)
    # 词云
    create_wordCloud(datas=datas)



'''
# 别样的引入方式
try:
    import requests
except ImportError:
    import os
    os.system('pip install requests')
    import requests

# 如果引入不了第三方,就引入系统的
try:
    import simplejson as json
except ImportError:
    import json
'''