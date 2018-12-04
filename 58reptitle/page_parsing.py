import requests, time, pymongo
from bs4 import BeautifulSoup

headers = {
    'cookie': "id58=c5/njVvlR+6lniKTAxTLAg==; 58tj_uuid=db296bf3-e3a3-4069-9d73-91adc0c2cd51; new_uv=1; gr_user_id=730ed7f9-9067-4ae5-9107-071e3dfe911f; _ga=GA1.2.2078882915.1541752817; als=0; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1541752877; wmda_uuid=12dc75b0ecfcd2586c83ef696d8c0dfe; wmda_new_uuid=1; wmda_visited_projects=%3B1409632296065; xxzl_deviceid=5ySzbGEl2ws6sj96dByBJKnxabczPLe8s1a1d23OFsXgfHEu%2BfFLuAWJsd42x2ik; city=bj; 58home=bj; ppStore_fingerprint=BF452D4CD5C03FCE0FED9B6F95FEACB53909321B3E44261B%EF%BC%BF1541753026424; final_history=35856769683255%2C36053934260744; xzuid=85ab7fc4-acef-4f00-a720-77a8438e8849; myfeet_tooltip=end",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

client = pymongo.MongoClient('localhost', 27017)
test = client['test']
url_list = test['url_list']
item_info = test['item_info']

# This is spider1 to get info_url from one tab.seller=0 is mean that it sell by own-person
def get_list_url(channel, page, seller=0):
    page_url = f'{channel}{seller}/pn{page}/'
    wb_data = requests.get(page_url, headers=headers)
    time.sleep(4)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    # judge the page exist or not
    if soup.find('td','t'):
        for link in soup.select('td.t > a.t'):
            item_link = link.get('href').split('&')[0]
            if 'zhuanzhuan' in item_link.split('.'):
                pass
            else:
                url_list.insert_one({'url':item_link})
                print('url:', item_link)
    else:
        print(f"Now in page {page}.")
        return True

# This is spider2 to get item_url for one_sell_thing
def get_thing_detail(url):
    # if 'zhuanzhuan' in url.split('.'):
    #     url = 'http:'+ url
    wb_data = requests.get(url, headers=headers)
    time.sleep(4)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # reject = soup.select('body > script:nth-of-type(2)')[0].get('src')
    if soup.find('div','main'):
        print('not exist.')
    else:
        if '58' in url.split('.'):
            print('im in 58')
            # title = soup.select('div.detail-title > h1')
            title = soup.title.text
            price = soup.select('div.infocard__container__item__main > span')[0].get_text().strip()
            post_date = soup.select('div.detail-title__info__text')[0].get_text()
            area = soup.select('div.infocard__container__item__main > a[target="_blank"]')[0].get_text()
            item_info.insert_one({
                'from':'58同城',
                'index_url':url,
                'title':title,
                'price':price,
                'post_date':post_date,
                'area':area
            })
        # elif 'zhuanzhuan' in url.split('.'):
        #     print('im in zhuanzhuan')
        #     title = soup.select('div.info > div.info-title'),
        #     price = soup.select('span')
        #     print('url:',url)
        #     print(soup.prettify())

if __name__ == '__main__':
    get_list_url('https://bj.58.com/pbdn/',5)


    # get_thing_detail('https://bj.58.com/pingbandiannao/36009696629252x.shtml')
    # get_thing_detail('https://www.zhuanzhuan.com/detail.html?infoId=1061175321730908172&fullCate=5,37&fullLocal=1&metric=listpc&psid=188777670202115296994237894&entinfo=36075377929999_p&slot=-1')