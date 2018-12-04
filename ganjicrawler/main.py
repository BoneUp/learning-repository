from page_parsing import get_page_list, get_info, ganji_item, zhuanzhuan_item, page_list
from channel_list import classify
from multiprocessing import Pool
import time, logging, sys
logging.basicConfig(filename=sys.path[0]+r'\ganji_main.txt',level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.DEBUG)

def get_all_link(page_tag):
    for number in range(1,101):
        logging.info(f'the url is: {page_tag}o{number}/')
        print(f'{page_tag} has done page {number}')
        next_page = get_page_list(page_tag, number)
        if next_page == False:
            print(f'{page_tag} has no next page.')
            break
        elif number + 1 == next_page:
            continue
    time.sleep(5)

def get_item_info(link):
    if get_info(link) == False:
        print("this page thing had selled.-----------    ",link)
    else:    
        print(f'{link} had done.')


if __name__ == '__main__':
    # pool = Pool(4)
    # pool.map(get_all_link, classify.split())
    # logging.info('All link had downloaded.')
    # pool.close()
    # pool.join()
    
    # get item which has didn't download.
    db_urls = [item['url'] for item in page_list.find()]
    ganji_index_urls = [item['url'] for item in ganji_item.find()]
    zhuanzhuan_index_urls = [item['url'] for item in zhuanzhuan_item.find()]
    x = set(db_urls)
    y = set(ganji_index_urls)
    z = set(zhuanzhuan_index_urls)
    rest_of_urls = x - (y | z)
    pool2 = Pool(4)
    pool2.map(get_item_info,rest_of_urls)
    pool2.close()
    pool2.join()
    logging.info('All items had done.')