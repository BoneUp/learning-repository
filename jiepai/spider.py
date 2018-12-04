# python3
#  ------ ** utf-8 ** ----------
#获取头条的街拍类目下的链接，然后进入帖子爬取图片
import requests, random, json, lxml, re, pymongo, os, sys
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from hashlib import md5

client = pymongo.MongoClient('localhost', 27017)
jiepai = client['jiepai']
jiepai_items = jiepai['jiepai_items']
downloaded = jiepai['downloaded']

anget = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
]
headers = {
    "user-agent": random.choice(anget)
}
# rebuild the url and request because it's load by js
def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery'
    }

    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("Request Failed....")
        return None
# get posts' link in the home page.
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')
# resquest the link and return text          
def get_page_detail(url):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("Request detail Failed....")
        return None
# analy the page and get the img-link
def parse_page_detail(html, url):
    soup = BeautifulSoup(html, lxml)
    title = soup.select('title')[0].get_text()
    print(title)
    image_pattern = re.compile(r'gallery: JSON\.parse\("(.*?)"\),', re.S)
    result = re.search(image_pattern, html)
    if result:
        result = str(result.group(1)).replace('\\', '')
        data = json.loads(result)
        if data and "sub_images" in data.keys():
            sub_images = data.get("sub_images")
            images = [item.get("url") for item in sub_images]
            return {
                'title': title,
                'url': url,
                'images': images
            }

def save_to_mongo(data):
    if jiepai_items.insert(data):
        print("save to mongo Done.....")
        return True
    return False

# request the ima-url and download it.
def download_img(url):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            save_image(response.content)
            return True
        return None
    except RequestException:
        print("Request img-url Failed.....")
        return None

def save_image(content):
    file_path = '{}\\jiepai-pictures'.format(sys.path[0])
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    img_path = '{}\\{}.{}'.format(file_path, md5(content).hexdigest(), 'jpg')
    if not os.path.exists(img_path):
        with open(img_path, 'wb') as f:
            f.write(content)
            f.close() 
            print(img_path, 'downloaded......')

def main(offset):
    html = get_page_index(offset, '街拍')
    for url in parse_page_index(html):
        html2 = get_page_detail(url)
        if html2:
            result = parse_page_detail(html2, url)
            if result:save_to_mongo(result)

if __name__ == '__main__':
    main(0)