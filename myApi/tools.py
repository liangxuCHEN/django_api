# encoding=utf8
import pandas as pd
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

def init_driver():
    # os.environ['webdriver.gecko.driver'] = "D:\geckodriver\geckodriver.exe"
    profile_dir = r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\2mdtv4bf.tianmao'
    driver = webdriver.Firefox(profile_dir, executable_path=r'D:\geckodriver\geckodriver.exe')
    return driver


def send_key_slow(keys, element):
    for k in keys:
        element.send_keys(k)
        time.sleep(0.1)


def login(driver):
    driver.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(4)
    send_key_slow(u'林氏木业家具旗舰店:a186', driver.find_element_by_id('TPL_username_1'))
    time.sleep(2)
    send_key_slow('bciz2s9j6t', driver.find_element_by_id('TPL_password_1'))
    time.sleep(1)
    driver.find_element_by_id("TPL_password_1").send_keys(Keys.ENTER)
    WebDriverWait(driver, 100, poll_frequency=1).until(lambda x: x.find_elements_by_id('J_boss_announcement'))


def down_load_file(driver, ship_time_from, ship_time_end, page_num):

    base_url = "https://portal-jia.tmall.com/msf/verificationOrderExport.do?shipTimeFrom=%s&shipTimeEnd=%s&" \
               "identifyStatus=0&orderId=&buyerNick=&tpName=&currentPage=%d"
    for i in range(0, int(page_num) + 10, 10):
        try:
            url = base_url % (ship_time_from, ship_time_end, i)
            driver.execute_script("window.open('%s')" % url)
        except TimeoutException:
            pass
        finally:
            time.sleep(1.5)
    driver.quit()


def merge_file(data):

    df_out = pd.DataFrame()
    driver = init_driver()
    login(driver)

    # 清空文件夹
    path_dir = os.listdir(data['dir_name'])
    for all_dir in path_dir:
        child = os.path.join('%s\%s' % (data['dir_name'], all_dir))
        os.remove(child)

    down_load_file(driver, data['ship_time_from'], data['ship_time_end'], data['page_num'])

    # 遍历指定目录，合并目录下的所有文件xls为一个xls
    path_dir = os.listdir(data['dir_name'])
    for all_dir in path_dir:
        child = os.path.join('%s\%s' % (data['dir_name'], all_dir))
        try:
            df = pd.read_excel(child, skiprows=1)
            df[u'订单编号'] = df[u'订单编号'].apply(str)
            df_out = df_out.append(df)
        except:
            print("In the %s, there are some error data." % child)

    df_out.to_excel('%s\%s.xls' % (data['dir_name'], data['output_file_name']))
    return True

