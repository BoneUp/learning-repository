#python3
#--*utf-8*--

import requests, random, re, json
from requests.exceptions import RequestException
from multiprocessing import Pool

angent = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
]
headers = {
    'Cookie': "__mta=48591641.1542680412801.1542680449642.1542680453599.5; uuid_n_v=v1; uuid=CEC8BA30EC6A11E8BA374D91ED77FFAF1CC1605B230048F593250DD820EE69D3; _csrf=34e179fd74a14078c3be3439f3141f4ac66b0495cd4298478e470da3541df1de; _lxsdk_cuid=1672eeb015f0-023e1529b0c54d-b79183d-1fa400-1672eeb0160c1; _lxsdk=CEC8BA30EC6A11E8BA374D91ED77FFAF1CC1605B230048F593250DD820EE69D3; __mta=48591641.1542680412801.1542680412801.1542680414081.2; _lxsdk_s=1672eeb0162-2fa-3d7-f45%7C%7C12",
    # 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    'User-Agent':random.choice(angent)
}
def get_one_page(url):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            print("ok")
            return response.text
    except RequestException:
        print("fail")
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)

    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4],
            'score':item[5]+item[6]
        }

def write_to_file(content):
    with open(r'E:\study files\crawler\study\maoyantop100\result.txt', "a", encoding='utf-8') as f:
        print(content)
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        # f.write(f'{content}\n')
        f.close()

def main(num):
    html = get_one_page('http://maoyan.com/board/4?offset={}'.format(num))
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    # pool = Pool(4)
    # pool.map(main, [num for num in range(0, 100, 10)])
    # pool.close()
    # pool.join()
    for num in range(0, 100 ,10):
        main(num)