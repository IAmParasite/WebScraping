# -*- coding: utf-8 -*-
# @Time    : 12.2
# @Author  : IAmParasite
# @FileName: PythonScraping-HeathrowAirport.py
# @Software: Visual Studio Code

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

# 爬取的页数
Pages_num = 3
# 间隔时间
Intervel_time = 600
# 添加文件输出路径，会覆盖文件之中已有的数据！
f1 = open("HeathrowAriport-Flights.json", "w+")

# 设置ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")

# 初始化Driver
driver = webdriver.Chrome(
    executable_path='chromedriver', 
    options=chrome_options)
driver.get('https://www.heathrow.com/arrivals')

# Drvier get到网站之后需要重新设置window_size, 否则数据确实一部分
driver.set_window_size(300, 1000)
#driver.maximize_window()

# 设置Json数据的字典，便于输出
JsonData = {"Sheduled" : [], "Flight" :[], "Arriving from": [], "Airline" :[], "Terminal": [], "Status" : []}

def work():
    #获取页面上所有的class名称为airline-listing-line-item的元素
    res = driver.find_elements_by_class_name('airline-listing-line-item')
    time.sleep(1)
    
    # 错误检查
    if(len(res) == 0):
        return
    list_element = res[0].text.split('\n')
    #print(list_element)

    # 存储数据
    for e in res:
        list_element = e.text.split('\n')
        JsonData["Sheduled"].append(list_element[0])
        JsonData["Flight"].append(list_element[1])
        JsonData["Arriving from"].append(list_element[2])
        JsonData["Airline"].append(list_element[3])
        JsonData["Terminal"].append(list_element[4])
        JsonData["Status"].append(list_element[5])
        
    # 获取页面上所有的button信息
    button = driver.find_elements_by_tag_name('button')
    time.sleep(1)

    for e in button:
        #点击按钮翻到下一页
        if(e.text == "Show later flights"):
            # 不能直接 e.click()
            driver.execute_script("arguments[0].click();", e)
            time.sleep(1)
    
if __name__ == "__main__":
    while(True):
        for i in range(Pages_num):
            work()
        f1.write(json.dumps(JsonData))
        time.sleep(Intervel_time)
        # 刷新页面，否则爬取的内容还是之前的内容
        driver.refresh()

driver.close()
f1.close()