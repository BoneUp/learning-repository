import requests, time
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

headers = {
    'Cookie': "citydomain=bj; __utma=32156897.1460584653.1542167248.1542167248.1542167248.1; __utmc=32156897; __utmz=32156897.1542167248.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ganji_xuuid=dfcc22fa-db1f-4bbe-9e78-96bdc1ec6596.1542167248239; ganji_uuid=5762844831665320704202; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A42448303941%7D; GANJISESSID=j0qvgkcptr6tocgu2illbhuamc; xxzl_deviceid=a3KOha%2F8C50MzxYQykk4eYiKjJ6b4wJA4ia%2FWeeRuzQ333mFNNNfLc1tK5wg6Ey5; lg=1; 58uuid=bb084ff6-5b59-496f-8dd2-e449fcb3f977; init_refer=; new_uv=1; new_session=0; ganji_login_act=1542167725016; __utmb=32156897.4.10.1542167248",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

url = 'http://bj.ganji.com/wu/'
wb_data = requests.get(url, headers=headers)
soup = BeautifulSoup(wb_data.text, 'lxml')
source_list = soup.select('dl.fenlei > dt > a')

for source in source_list:
    logging.debug(source.get_text())
    # print('http://bj.ganji.com'+source.get('href'))

classify = """
http://bj.ganji.com/jiaju/
http://bj.ganji.com/rirongbaihuo/
http://bj.ganji.com/shouji/
http://bj.ganji.com/bangong/
http://bj.ganji.com/nongyongpin/
http://bj.ganji.com/jiadian/
http://bj.ganji.com/ershoubijibendiannao/
http://bj.ganji.com/ruanjiantushu/
http://bj.ganji.com/yingyouyunfu/
http://bj.ganji.com/diannao/
http://bj.ganji.com/xianzhilipin/
http://bj.ganji.com/fushixiaobaxuemao/
http://bj.ganji.com/meironghuazhuang/
http://bj.ganji.com/shuma/
http://bj.ganji.com/laonianyongpin/
http://bj.ganji.com/xuniwupin/
http://bj.ganji.com/qitawupin/
http://bj.ganji.com/ershoufree/
http://bj.ganji.com/wupinjiaohuan/
"""
