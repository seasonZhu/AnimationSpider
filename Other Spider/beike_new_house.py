import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

columns = ['title', 'place', 'msg', 'perMeter', 'price']

# 通过select获取信息
def getInfo(soup, selector):
    infoString = '未知'
    info = soup.select(selector)
    if len(info) > 0:
        infoString = info[0].get_text().replace('\n','').replace('\t','')
    return infoString

# 爬取某网页
def get_a_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tags = soup.find_all('li', attrs= {'class': 'resblock-list post_ulog_exposure_scroll has-results'})
    listCount = len(tags)

    titles = ["楼盘名称"]
    places = ["位置信息"]
    msgs = ["户型"]
    prices = ["总价"]
    perMeters = ["单价"]

    for i in range(1, listCount + 1):

        # 名称
        titleSelector = 'body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li:nth-child({}) > div > div.resblock-name > a'.format(i)
        title = getInfo(soup=soup, selector=titleSelector)

        # 位置
        placeSelector = 'body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li:nth-child({}) > div > a.resblock-location'.format(i)
        place = getInfo(soup=soup, selector=placeSelector)

        # 信息
        msgSelector = 'body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li:nth-child({}) > div > a.resblock-room'.format(i)
        msg = getInfo(soup=soup, selector=msgSelector)

        # 单价
        perMeterSelector = 'body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li:nth-child({}) > div > div.resblock-price > div.main-price > span.number'.format(i)
        perMeter = getInfo(soup=soup, selector=perMeterSelector)

        # 总价
        priceSelector = 'body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li:nth-child({}) > div > div.resblock-price > div.second'.format(i)
        price = getInfo(soup=soup, selector=priceSelector)

        dictionary = {
            'title': title,
            'place': place,
            'msg': msg,
            'perMeter': perMeter,
            'price': price
        }

        titles.append(title)
        places.append(place)
        msgs.append(msg)
        prices.append(price)
        perMeters.append(perMeter)

        print(json.dumps(dictionary, ensure_ascii=False))

    data = {
        'title': titles,
        'place': places,
        'msg': msgs,
        'perMeter': perMeters,
        'price': prices,
    }

    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv('WuhanNewHouse.csv', mode ='a', index=False, header=False)

from multiprocessing.pool import Pool

if __name__ == '__main__':
    # 爬一共多少个页面 其实有很多是自己的逻辑
    response = requests.get('https://wh.fang.ke.com/loupan/caidian/pg{}/#caidian'.format(1))
    soup = BeautifulSoup(response.text, 'lxml')
    tags = soup.find_all('li', attrs= {'class': 'resblock-list post_ulog_exposure_scroll has-results'})
    # 单页展示的个数
    listCount = len(tags)
    totalPageCount = 0
    # 总的搜索结果
    searchResult = soup.select('body > div.resblock-list-container.clearfix > div.resblock-have-find > span.value')
    if len(searchResult) > 0:
        searchCount = int(searchResult[0].get_text())
        # 如果总的搜索数结果除以单页展示的个数 大于100 那么上限就是100页,
        page = searchCount / listCount
        if page >= 100:
            page = 100
            totalPageCount = page
        else:
            if searchCount % listCount == 0:
                totalPageCount = page
            else:
                totalPageCount = int(page) + 1
                
            
    # 这两个是无用信息
    pageInfo = soup.select('body > div.page-container.clearfix > div.page-box')
    lastPageInfo = soup.find_all('div', attrs= {'class':'page-box'})
    totalPageCount = int(totalPageCount)
    print("totalPageCount: {}".format(totalPageCount))

    for i in range(0, totalPageCount):
        index = i + 1
        get_a_page(f'https://wh.fang.ke.com/loupan/caidian/pg{index}/#caidian')
    # 这个多线程有问题
    # pool = Pool(5)
    # group = ([f'https://wh.fang.ke.com/loupan/pg{i}' for i in range(1, 101)])
    # pool.map(get_a_page,group)
    # pool.close()
    # pool.join()