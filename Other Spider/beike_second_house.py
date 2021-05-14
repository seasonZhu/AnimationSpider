import requests
from pyquery import PyQuery as pq
import json
import pandas as pd

columns = ['title', 'msg', 'price', 'per_meter']

# 爬取某网页
def get_a_page(url):
    result = requests.get(url)
    doc = pq(result.text)
    ul = doc('.sellListContent')
    divs = ul.children('.clear .info.clear').items()
    count = 0
    titles = []
    places = []
    msgs = []
    prices = []
    per_meters = []
    for div in divs:
        count += 1
        title = div.children('.title a').text()
        place = div.children('.address .flood .positionInfo a').text()
        msg = div.children('.address .houseInfo').text()
        price = div.children('.address .priceInfo .totalPrice span').text()
        per_meter = div.children('.address .priceInfo .unitPrice').attr('data-price')
        dict = {
            'title': title,
            'place': place,
            'msg': msg,
            'price': price,
            'per_meter': per_meter
        }
        titles.append(title)
        places.append(place)
        msgs.append(msg)
        prices.append(price)
        per_meters.append(per_meter)
        print(str(count) + ':' + json.dumps(dict, ensure_ascii=False))
        datas={
            'title': titles,
            'place': places,
            'msg': msgs,
            'price': prices,
            'per_meter': per_meters
        }
        df = pd.DataFrame(data=datas, columns=columns)
        df.to_csv('sjz.csv', mode='a', index=False, header=False)

from multiprocessing.pool import Pool

if __name__ == '__main__':
    for i in range(1, 101):
        get_a_page(f'https://wh.ke.com/ershoufang/pg{i}mw1l2/')
    # pool = Pool(5)
    # group = ([f'https://sjz.ke.com/ershoufang/pg{x}mw1l2/' for x in range(1, 101)])
    # pool.map(get_a_page,group)
    # pool.close()
    # pool.join()