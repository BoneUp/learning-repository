import requests, time, pymongo, sys
from bs4 import BeautifulSoup
import logging
logging.basicConfig(filename=sys.path[0]+r'\ganjiparsing.txt',level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.DEBUG)

client = pymongo.MongoClient('localhost', 27017)
Classify_list = client['Classify_list']
page_list = Classify_list['page_list']
ganji_item = Classify_list['ganji_item']
zhuanzhuan_item = Classify_list['zhuanzhuan_item']

# get the each classify-page list
headers = {
    'Cookie': "citydomain=bj; __utma=32156897.1460584653.1542167248.1542167248.1542167248.1; __utmc=32156897; __utmz=32156897.1542167248.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ganji_xuuid=dfcc22fa-db1f-4bbe-9e78-96bdc1ec6596.1542167248239; ganji_uuid=5762844831665320704202; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A42448303941%7D; GANJISESSID=j0qvgkcptr6tocgu2illbhuamc; xxzl_deviceid=a3KOha%2F8C50MzxYQykk4eYiKjJ6b4wJA4ia%2FWeeRuzQ333mFNNNfLc1tK5wg6Ey5; lg=1; 58uuid=bb084ff6-5b59-496f-8dd2-e449fcb3f977; init_refer=; new_uv=1; new_session=0; ganji_login_act=1542167725016; __utmb=32156897.4.10.1542167248",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}
def get_page_list(url_tag, pgnumber):
    if pgnumber == 1:  # beacuase the first page don't have tail 'o1'
        url = url_tag
    else:
        url = f'{url_tag}o{pgnumber}/'
    wb_data = requests.get(url, headers=headers)
    time.sleep(3)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # jude the page have personal-seller or not to use diffrent select rule
    if len(soup.select('li.ontab > a')) != 0 and soup.select('li.ontab > a')[0].get_text() == '个人':
        links = soup.select('dl > dd.feature > div > ul > li > a')
    else:
        links = soup.select('tr > td.t > a')
    logging.info(f'page:{url}')
    for link in links:
        #TODO: put data into mongodb
        page_list.insert_one({'url':link.get('href').split('?')[0]})

    #TODO: get the next page and return it
    next_page = soup.select('div.pageBox > ul > li > a.next') #get the next page
    if len(next_page) != 0:
        logging.debug(next_page)
        logging.debug(next_page[0].get('href').split('/')[-2][1:])
        return next_page[0].get('href').split('/')[-2][1:]
    elif len(next_page) == 0:
        logging.debug('No next page here.')
        return False  # no next page link


# get the post information
def get_info(url):
    wb_data = requests.get(url, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # have two diffrent style page to analyze
    if 'http://zhuanzhuan' in url.split('.'):
        title = soup.select('div.box_left_top > h1')
        price = soup.select('span.price_now > i')
        area = soup.select('div.palce_li > span > i')
        if len(title)==0 and len(price)==0 and len(area)==0:
            return False
        zhuanzhuan_item.insert_one({
            'title': title[0].get_text(),
            'price': price[0].get_text(),
            'area': area[0].get_text(),
            'url': url
        })
        logging.debug(title[0].get_text())
        logging.debug(price[0].get_text())
        logging.debug(area[0].get_text())
    else:  
        try:  # ganji.com has two diffrent type page.
            try:
                soup.select('div.content.clearfix > div.leftBox > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > label')[0].get_text() == '类　　型：'
                types = soup.select('div.content.clearfix > div.leftBox > div:nth-of-type(2)> div > ul > li:nth-of-type(1) > span > a')
                title = soup.select('h1.title-name')
                post_date = soup.select('li > i.pr-5')
                price = soup.select('ul.det-infor > li:nth-of-type(2) > i')
                area = soup.select('ul.det-infor > li:nth-of-type(3)')
                ganji_item.insert_one({
                'title': title[0].get_text(),
                'type': types[0].get_text(),
                'post_date': post_date[0].get_text().strip(),
                'price': price[0].get_text(),
                'area': list(area[0].stripped_strings),
                'url': url
                })
            except:
                title = soup.select('h1.title-name')
                post_date = soup.select('li > i.pr-5')
                price = soup.select('ul.det-infor > li:nth-of-type(1) > i')
                area = soup.select('ul.det-infor > li:nth-of-type(2)')
                ganji_item.insert_one({
                'title': title[0].get_text(),
                'post_date': post_date[0].get_text().strip(),
                'price': price[0].get_text(),
                'area': list(area[0].stripped_strings),
                'url': url
                })
        except:
            logging.info(f'break url:  {url}')
            return False


if __name__ == '__main__':
    get_page_list('http://bj.ganji.com/bangong/',47)
    get_page_list('http://bj.ganji.com/nongyongpin/',3)
    # get_info(page_list.find()[0]['url'])
    # get_info('http://bj.ganji.com/rirongbaihuo/35962301776182x.htm')
    # get_info('http://zhuanzhuan.ganji.com/detail/1062602699832229889z.shtml')
    print(page_list.find().count())
