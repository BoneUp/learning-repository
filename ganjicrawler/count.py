from page_parsing import page_list, ganji_item, zhuanzhuan_item
import time

while True:
    print("url list has:    ", page_list.find().count())
    print("item list has:   ", ganji_item.find().count()+zhuanzhuan_item.find().count())
    print('\n')
    time.sleep(5)
