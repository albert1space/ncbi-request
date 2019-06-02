# -*- coding: utf-8 -*-
import re
import urllib
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pymysql
import numpy as np
import time
import string
import random
'''写入mysql数据库准备
create database ncbiitem;
use tncbiitem;
create table ncbi_goods(
titles varchar(250),
details varchar(250),
linkurls varchar(250),
designs  varchar(250),
Submittes varchar(250),
Studys varchar(250),
Samples varchar(250),
Strategys varchar(250),
Sources varchar(250),
Layouts varchar(250),
Runs varchar(250),
Publisheds varchar(250))
'''
keyword = 'mice'
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 1) 
conn=pymysql.connect(host="127.0.0.1",user="root",passwd="albert",
                     port=3306,db="taobaoitem",charset='utf8')

def search(keyword):
    try:
        print('正在搜索')
        browser.get('https://www.ncbi.nlm.nih.gov/sra') #模拟浏览器进入网
        #等待直到局部元素显示出来,这里的局部元素为网页搜索框部分
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#term"))
        )
        #等待直到元素可被点击,这里的元素为搜索按钮
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#search')))
        input.send_keys(keyword) #在输入框调用send_keys方法模拟输入关键字
        submit.click() #模拟点击搜索按钮操作
    #发生延时异常时，重新调用search()方法
    except TimeoutException:
        search(keyword)

def get_products():
    print('获取信息')
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('#maincontent div div .rprt')
    for item in items:
        title1=str(item.select('.title')[0].text.strip())
        detail1=str(item.select('.supp')[0].text.strip())
        linkurl1=str('https://www.ncbi.nlm.nih.gov')+item.select('.rslt p a')[0]['href']
        print(linkurl1)
        sra=urllib.request.urlopen(linkurl1)
        sradata=sra.read().decode("gbk","ignore")
        design1=re.sub('\[|]|,|\'', '',str(re.compile("Design: <span>(.*?)<",re.S).findall(sradata)))
        Submitte1=re.sub('\[|]|,|\'', '',str(re.compile("Submitted by: <span>(.*?)<",re.S).findall(sradata)))
        Study1=re.sub('\[|]|,|\'', '',str(re.compile("Study: <span>(.*?)<",re.S).findall(sradata)))
        Sample1=re.sub('\[|]|,|\'', '',str(re.compile("Sample: <span>(.*?)<",re.S).findall(sradata)))
        Strategy1=re.sub('\[|]|,|\'', '',str(re.compile("Strategy: <span>(.*?)<",re.S).findall(sradata)))
        Source1=re.sub('\[|]|,|\'', '',str(re.compile("Source: <span>(.*?)<",re.S).findall(sradata)))
        Layout1=re.sub('\[|]|,|\'', '',str(re.compile("Layout: <span>(.*?)<",re.S).findall(sradata)))
        Run1=str('https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=')+re.sub('\[|]|,|\'', '',str(re.compile(">(.{2,10})</a></td><td align=",re.S).findall(sradata)))
        Published1=re.sub('\[|]|,|\'', '',str(re.compile("</td><td>(.{2,30})</td></tr></tbody>",re.S).findall(sradata)))
        sql1="insert into ncbi_goods(titles,details,linkurls,designs,Submittes,Studys,Samples,Strategys,Sources,Layouts,Runs,Publisheds) values('"+str(title1)+"','"+str(detail1)+"','"+str(linkurl1)+"','"+str(design1)+"','"+str(Submitte1)+"','"+str(Study1)+"','"+str(Sample1)+"','"+str(Strategy1)+"','"+str(Source1)+"','"+str(Layout1)+"','"+str(Run1)+"','"+str(Published1)+"')"
        conn.query(sql1)
        conn.commit()
    print('该页写入数据库完成')


def next_page(page_number):
    try:
        get_products() #解析每一页的信息
        #等待直到元素可被点击,这里的元素为输入页码后的的确定按钮
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bottom .next')))
        submit.click() #模拟点击确定按钮，跳转到下一页的操作
    #发生延时异常时，重新调用next_page(page_number)方法
    except TimeoutException:
        next_page(page_number)

def main():
    for i in range(1,3400):
        next_page(i)
    browser.close()

if __name__ == '__main__':
    main()


