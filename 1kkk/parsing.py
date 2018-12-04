from bs4 import BeautifulSoup
import requests,time, logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# logging.disble(logging.CRITICAL)

headers = {
    'Cookie': "DM5_MACHINEKEY=aac3e620-ab75-47d2-9a4a-113f29d6ef1f; UM_distinctid=16717dc92267e-091895c3f58757-b79183d-1fa400-16717dc922849a; dm5cookieenabletest=1; dm5imgpage=228369|1:1:55:0,174992|1:1:56:0; firsturl=http%3A%2F%2Fwww.1kkk.com%2Fch3-174992%2F; dm5imgcooke=228369%7C2%2C174992%7C2; dm5_newsearch=%5b%7b%22Title%22%3a%22%e6%bc%ab%e5%a8%81%22%2c%22Url%22%3a%22%5c%2fsearch%3ftitle%3d%25E6%25BC%25AB%25E5%25A8%2581%26language%3d1%22%7d%2c%7b%22Title%22%3a%22%e9%92%a2%e9%93%81%e4%be%a0%22%2c%22Url%22%3a%22%5c%2fsearch%3ftitle%3d%25E9%2592%25A2%25E9%2593%2581%25E4%25BE%25A0%26language%3d1%22%7d%5d; image_time_cookie=174992|636779637441353081|0; readhistory_time=636779640349345365; ComicHistoryitem_zh=History=15677,636779640349345365,168055,1,0,0,0,0&ViewType=0",
    'User-Agent': "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36"
}
url = 'http://www.1kkk.com/manhua15677/'
# url = 'http://www.1kkk.com/manhua7070/'
web = 'http://www.1kkk.com'

def get_onebook_links(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title = soup.select('div.banner_detail_form > div.info > p.title')[0].get_text().replace(' ','')[:-4]
    # chapters = soup.find_all(id="chapterlistload")[0].find_all('li')
    chapters = soup.select('div[id="chapterlistload"] li')
    manga = {
        'title':title,
        'url':url,
        'manga_chapters':{}
    }
    for ob in chapters:
        chapter = ob.get_text().replace(' ','')
        link = ob.select('a')[0].get('href')
        manga['manga_chapters'][chapter] = web + link
    print(manga)

def get_img(url):
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    img_links = soup.select('div[id="cp_img"]')
    print(img_links, len(img_links))
    # for link in img_links:
    #     print(link.get('src'))

if __name__ == '__main__':
    get_img('http://m.1kkk.com/ch1-168055/')