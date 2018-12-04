import spider
from multiprocessing import Pool

def get_links():
    pool = Pool(4)
    pool.map(spider.main, range(0, 220, 20))
    pool.close()
    pool.join()

def get_imgs(links):
    for link in links:
        ded = spider.download_img(links)
        if ded == True:
            spider.downloaded.insert({'url':link}) # save the images link for download continiun.

def conform():
    db_url = []
    for item in spider.jiepai_items.find():
        for url in item["images"]:
            db_url.append(url)
    dl_url = [item['url'] for item in spider.downloaded.find()]
    x = set(db_url)
    y = set(dl_url)
    not_dl_link = x - y
    return not_dl_link

if __name__ == '__main__':
    # get_links()


    not_dl_link = conform()
    # print(not_dl_link)
    pool2 = Pool(4)
    pool2.map(get_imgs, not_dl_link)
    pool2.close()
    pool2.join()