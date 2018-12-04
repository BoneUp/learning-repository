# python3
# -*- coding:utf-8 -*-
import time, re, pymongo, logging

import requests
from fake_useragent.fake import UserAgent
from pyquery import PyQuery

from random import random
from urllib.parse import urlencode

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s\n")
logging.disable(logging.CRITICAL)

client = pymongo.MongoClient('localhost', 27017)
wechat = client['wechat']
article = wechat['article']
base_url = 'https://weixin.sogou.com/weixin?'
headers = {
    'Cookie':
    'IPLOC=CN4404; SUID=104849DF7C20940A000000005BF7BF35; SUV=1542962997086773; SNUID=91C9C85E8187F9D393655FD182CF07F0; ad=fZllllllll2bdED@lllllVsTs8DlllllT1Ow9lllll9lllllVCxlw@@@@@@@@@@@; CXID=422D07CA6F706732129F0BD8061AEB95; pgv_pvi=4601563136; pgv_si=s4813998080; ld=RZllllllll2bdEDMlllllVsTsDylllllT1Ow9lllllylllllVZlll5@@@@@@@@@@; LSTMV=236%2C71; LCLKINT=5151; ABTEST=0|1542963146|v1; JSESSIONID=aaaOlMKWrsUNC-px-v6Cw; weixinIndexVisited=1; ppinf=5|1542966103|1544175703|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozOldXV3xjcnQ6MTA6MTU0Mjk2NjEwM3xyZWZuaWNrOjM6V1dXfHVzZXJpZDo0NDpvOXQybHVHYWxzQXl4UVNReklDWWswY0lVcnRNQHdlaXhpbi5zb2h1LmNvbXw; pprdig=soX6QVIAf9IWm-XFuuLHWtFIezC-1sedKQIHQVhknHB6fa2bQG3KkZvxwscBO_tfKToXto8qt17_oo7DXRsFv_77armP0k55er3eTSpk7OuRBW2fvhJedx64fmqMC78OPhJ3KV-sE6_-BtO_r08p8HxLfTxpzTE422AURo3Z3cA; sgid=08-38080205-AVv3y1dz6VfHwuTYxcrGfeo; ppmdig=15429661040000006c05a94d787ab436d429b1025c50fba8; sct=3',
    'Host':
    'weixin.sogou.com',
    'Referer':
    'https://weixin.sogou.com/weixin?oq=&query=%E4%B8%80%E5%8A%A06T&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=0&_sug_=n&type=2&sst0=1542966114223&page=12&ie=utf8&p=40040108&dp=1&w=01015002&dr=1',
    'Save-Data':
    'on',
    'Upgrade-Insecure-Requests':
    '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
proxy = None


def get_proxy():
    logging.debug('You are in get_proxy()')
    try:
        response = requests.get('http://127.0.0.1:5000/get')
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


#request the url and response text of html
def get_html(url, count=1):
    logging.debug('You are in get_html()')
    print("Crawling :", url)
    global proxy
    try:
        if proxy:
            proxies = {'http': 'http://' + proxy}
            response = requests.get(
                url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(
                url, allow_redirects=False, headers=headers)
        time.sleep(5)
        if response.status_code == 200:
            print("This page is OK...")
            return response.text
        if response.status_code == 320:
            print("It's 302 now....")
            # mean you need proxy
            # TODO: defind a method to change ip
            proxy = get_proxy()
            if proxy:
                print("Using proxy:", proxy)
                return get_html(url)
            else:
                print("Can't get the proxy...")
                logging.error("Can't get the proxy..")
                return None
    except ConnectionError as e:
        logging.warning("It's erroe:{}".format(e.args))
        print("Try to request url {} times....".format(count))
        if count >= 5:
            print("It's error out of {} times.".format(count))
            logging.error("It's error out of {} times.".format(count))
            return None
        count += 1
        proxy = get_proxy()
        return get_html(url, count)


#create url and request it
def get_index(keyword, page):
    logging.debug("You're in get_index()")
    data = {'query': keyword, 'type': 2, 'page': page}
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


# parse the index page and get the url of every article's link
def parse_index(html):
    logging.debug("You're in parse_index()")
    doc = PyQuery(html)
    items = doc('.news-box ul.news-list li div.txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


# request the wechat official article
def get_article_html(url):
    logging.debug("You're in get_article_html()")
    try:
        response = requests.get(
            url, headers={"User-Agent": UserAgent().random})
        time.sleep(3)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        logging.error("Get the article_html error : {}".format(
            response.status_code))
        return None


# parse the weixin_article detail
def parse_detail(html):
    logging.debug("You're in parse_detail()")
    doc = PyQuery(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content ').text()
    date = re.findall(
        '<div id="js_article".*?<em id="publish_time".*?>(.*?)</em>', html,
        re.S)[0]
    logging.debug("The data selector is: {}".format(
        str(doc('em.rich_media_meta_text')).strip()))
    nick_name = doc('#js_name').text()
    official_account = doc(
        '#js_profile_qrcode > div > p:nth-child(3) > span').text()
    return {
        'title': title,
        'content': content,
        'date': date,
        'nick_name': nick_name,
        'official_account': official_account,
    }


def save_to_mongo(data):
    if article.update({'title': data['title']}, {'$set': data}, True):
        print('Mongodb had already put in the data:', data['title'])
    else:
        print('Saved fail:', data['title'])


def main():
    logging.debug("You're in main()")
    for i in range(1, 2):
        html = get_index('一加6T', i)
        if html:
            logging.debug('Index HTML OK.....')
            article_urls = parse_index(html)
            logging.debug(article_urls)
            for article_url in article_urls:
                logging.debug(article_url)
                html = get_article_html(article_url)
                if html:
                    logging.debug('Article HTML OK.....')
                    article_data = parse_detail(html)
                    if article_data:
                        save_to_mongo(article_data)


if __name__ == '__main__':
    main()
