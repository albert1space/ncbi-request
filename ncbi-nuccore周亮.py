# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 21:59:10 2019

@author: Albert
"""
os.path.basename('C:\Program Files (x86)\Google\Chrome\Application')
# -*- coding: utf-8 -*-
import re
import os
import urllib
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import numpy as np
import time
import string
import random
import csv

keyword = 'mice'
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 1) 
browser.get('https://www.ncbi.nlm.nih.gov/nuccore')#模拟浏览器进入网
#等待直到局部元素显示出来,这里的局部元素为网页搜索框部分
input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#term")))
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search')))#等待直到元素可被点击,这里的元素为搜索按钮
input.send_keys(keyword) #在输入框调用send_keys方法模拟输入关键字
submit.click() #模拟点击搜索按钮操作

#linkurl=[]
def get_products():#nuccore mice
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('#maincontent div div .rprt')
    for item in items:
        title1=str(item.select('.title')[0].text.strip())
        detail1=str(item.select('.supp')[0].text.strip())
        linkurl1=str('https://www.ncbi.nlm.nih.gov')+item.select('.rslt p a')[0]['href']
        print(linkurl1)
        #linkurl.append(linkurl1)
        out =open('ncbi_nuccoreurl.csv', 'a', encoding='utf_8_sig',newline='') 
        fieldnames = [title1, detail1, linkurl1]
        write = csv.writer(out,dialect='excel')
        write.writerow(fieldnames)

def next_page(page_number):
    try:
        get_products() #解析每一页的信息
        #等待直到元素可被点击,这里的元素为输入页码后的的确定按钮
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bottom .next')))
        submit.click() #模拟点击确定按钮，跳转到下一页的操作
    #发生延时异常时，重新调用next_page(page_number)方法
    except TimeoutException:
        next_page(page_number)

'''
with open(filename, 'r', encoding='utf_8_sig',newline='') as file_object:
    for line in file_object:
        #print(line)
        linurl2=re.compile('bp linear.*?,(.*?)\r\n', re.S).findall(line)[-1]
        print(linurl2)
    lines = file_object.readlines()
    type(lines)
    type(line)
'''

file_object=open(filename, 'r', encoding='utf_8_sig',newline='')
i=1
def get_message():
    for line in file_object:
        linurl2=re.compile('bp linear.*?,(.*?)\r\n', re.S).findall(line)[-1]
        browser.get(str(linurl2))
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        DETAIL=soup.select('.genbank')[0].text.strip()
        #DETAIL=soup.find_all(name = 'pre',attrs = {'class' : 'genbank'})[0].text.strip()
        FEATURES=re.compile('(.*?)FEATURES', re.S).findall(DETAIL)[-1]
        out =open('ncbi_nuccoreinfo.csv', 'a', encoding='utf_8_sig',newline='') 
        fieldnames = [linurl2, FEATURES]
        write = csv.writer(out,dialect='excel')
        write.writerow(fieldnames)
        print('完成第'+str(i)+'个')
        i +=1

def main():
    for i in range(1,34000):
        next_page(i)
        print('完成第'+str(i)+'页')
    get_message()
    browser.close()

if __name__ == '__main__':
    main()
