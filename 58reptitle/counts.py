import time
from page_parsing import url_list, item_info

while True:
    print("url list number has:    ",url_list.find().count())
    print("item informations has:  ",item_info.find().count())
    print("\n")
    time.sleep(5)