import requests
from bs4 import BeautifulSoup

headers = {
    'cookie': "id58=c5/njVvlR+6lniKTAxTLAg==; 58tj_uuid=db296bf3-e3a3-4069-9d73-91adc0c2cd51; new_uv=1; gr_user_id=730ed7f9-9067-4ae5-9107-071e3dfe911f; _ga=GA1.2.2078882915.1541752817; als=0; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1541752877; wmda_uuid=12dc75b0ecfcd2586c83ef696d8c0dfe; wmda_new_uuid=1; wmda_visited_projects=%3B1409632296065; xxzl_deviceid=5ySzbGEl2ws6sj96dByBJKnxabczPLe8s1a1d23OFsXgfHEu%2BfFLuAWJsd42x2ik; city=bj; 58home=bj; ppStore_fingerprint=BF452D4CD5C03FCE0FED9B6F95FEACB53909321B3E44261B%EF%BC%BF1541753026424; final_history=35856769683255%2C36053934260744; xzuid=85ab7fc4-acef-4f00-a720-77a8438e8849; myfeet_tooltip=end",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}
url = 'https://bj.58.com/sale.shtml'
if __name__ == '__main__':
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('ul.ym-mainmnu > li > ul > li > b > a')

    for link in links:
        tab_url = 'https://bj.58.com'+link.get('href')
        print(tab_url)

channel_list = """
    https://bj.58.com/shouji/
    https://bj.58.com/tongxunyw/
    https://bj.58.com/danche/
    https://bj.58.com/diandongche/
    https://bj.58.com/fzixingche/
    https://bj.58.com/sanlunche/
    https://bj.58.com/peijianzhuangbei/
    https://bj.58.com/diannao/
    https://bj.58.com/bijiben/
    https://bj.58.com/pbdn/
    https://bj.58.com/diannaopeijian/
    https://bj.58.com/zhoubianshebei/
    https://bj.58.com/shuma/
    https://bj.58.com/shumaxiangji/
    https://bj.58.com/mpsanmpsi/
    https://bj.58.com/youxiji/
    https://bj.58.com/ershoukongtiao/
    https://bj.58.com/dianshiji/
    https://bj.58.com/xiyiji/
    https://bj.58.com/bingxiang/
    https://bj.58.com/jiadian/
    https://bj.58.com/binggui/
    https://bj.58.com/chuang/
    https://bj.58.com/ershoujiaju/
    https://bj.58.com/yingyou/
    https://bj.58.com/yingeryongpin/
    https://bj.58.com/muyingweiyang/
    https://bj.58.com/muyingtongchuang/
    https://bj.58.com/yunfuyongpin/
    https://bj.58.com/fushi/
    https://bj.58.com/nanzhuang/
    https://bj.58.com/fsxiemao/
    https://bj.58.com/xiangbao/
    https://bj.58.com/meirong/
    https://bj.58.com/yishu/
    https://bj.58.com/shufahuihua/
    https://bj.58.com/zhubaoshipin/
    https://bj.58.com/yuqi/
    https://bj.58.com/tushu/
    https://bj.58.com/tushubook/
    https://bj.58.com/wenti/
    https://bj.58.com/yundongfushi/
    https://bj.58.com/jianshenqixie/
    https://bj.58.com/huju/
    https://bj.58.com/qiulei/
    https://bj.58.com/yueqi/
    https://bj.58.com/kaquan/
    https://bj.58.com/bangongshebei/
    https://bj.58.com/diannaohaocai/
    https://bj.58.com/bangongjiaju/
    https://bj.58.com/ershoushebei/
    https://bj.58.com/chengren/
    https://bj.58.com/nvyongpin/
    https://bj.58.com/qinglvqingqu/
    https://bj.58.com/qingquneiyi/
    https://bj.58.com/chengren/
    https://bj.58.com/xiaoyuan/
    https://bj.58.com/ershouqiugou/
    https://bj.58.com/tiaozao/
    https://bj.58.com/tiaozao/
    https://bj.58.com/tiaozao/ """