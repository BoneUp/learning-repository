#  python3
#  ------- coding: utf8 --------

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def search(word):
    browser.get('https://login.taobao.com/member/login.jhtml')
    browser.maximize_window()
    # input = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
    # )
    # submit = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
    # )
    # account_login = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, '#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-sign > a.h'))
    # )
    # account_login.click()
    time.sleep(2)
    login()
    time.sleep(5)
    input.send_keys(word)
    submit.click()

def login():
    
    # 点击账号密码登陆
    account_pw = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static'))
    )
    account_pw.click()
    # 获取输入账号名和密码的位置
    account = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_username_1'))
    )
    password = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_password_1'))
    )
    account.send_keys('迷路de小蚂蚁')
    time.sleep(2)
    password.send_keys('poanga123.0a0598/')

    # 获取滑动条的size
    span_background = browser.find_element_by_css_selector("#nc_1__scale_text > span")
    span_background_size = span_background.size
    print(span_background_size)
    
    # 获取滑块的位置
    button = browser.find_element_by_css_selector("#password-label")
    button_location = button.location
    print(button_location)
    
    # 拖动操作：drag_and_drop_by_offset
    # 将滑块的位置由初始位置，右移一个滑动条长度（即为x坐标在滑块位置基础上，加上滑动条的长度，y坐标保持滑块的坐标位置）
    x_location = button_location["x"] + span_background_size["width"]
    y_location = button_location["y"]
    ActionChains(browser).click_and_hold(button).drag_and_drop_by_offset(button, x_location, y_location).perform()

def main():
    search('美食')

if __name__ == '__main__':
    main()