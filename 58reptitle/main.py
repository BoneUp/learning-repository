from multiprocessing import Pool
from channel_extract import channel_list
from page_parsing import get_list_url
import time

def get_all_page_links(channel):
    time.sleep(5)
    judge_num = 0
    for num in range(1, 101):
        judge = get_list_url(channel, num)
        # judge_num to know if the missing page has get 5, stop this loop.
        if judge:
            judge_num += 1
        if judge_num == 5:
            judge_num = 0
            print("break url:  ", channel)
            break

if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_page_links, channel_list.split())