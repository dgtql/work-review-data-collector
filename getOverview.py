# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:55:47 2021

@author: 51zhu
"""


from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# get links for treatment groups
treat_urls = []
with open('comp_controll.csv', 'r', encoding = 'utf-8') as f:
    for line in f:
        line = line.strip().split(',')
        name = line[0]
        review_link = line[-1]
        if 'eng' in review_link:
            root = review_link.split('?')[0]
            if len(root)>15:
                treat_urls.append((name,root))
        else:
            if len(review_link)>15:
                treat_urls.append((name, review_link))
            
# test
def getLink(url):
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\51zhu\\AppData\\Local\\Google\\Chrome\\User Data\\")
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(url)
    
    button = driver.find_element_by_css_selector("#EmpLinksWrapper > div.d-none.d-md-block > div > div.d-flex > div > div:nth-child(2) > p")
    button.click()
    
    button = driver.find_element_by_css_selector("#EmpLinksWrapper > div.d-none.d-md-block > div > div.d-flex > div > div:nth-child(2) > div > ul > li:nth-child(1) > a")
    button.click()
    
    html = driver.page_source
    driver.close()
    return html


# parse
def parse_page(html):
    holder = []
    soup = BeautifulSoup(html, 'html.parser')
    
    size = soup.find("div", {"data-test":"employer-size"}).text
    holder.append(size)
    
    c_type = soup.find("div", {"data-test":"employer-type"}).text
    holder.append(c_type)    
    
    founded = soup.find("div", {"data-test":"employer-founded"}).text
    holder.append(founded)    
    
    industry = soup.find("div", {"data-test":"employer-industry"}).text
    holder.append(industry) 
    
    rev = soup.find("div", {"data-test":"employer-revenue"}).text
    holder.append(rev) 
    return holder


def write_file(holder, d_path, name):
    with open(d_path, 'a', encoding = 'utf-8') as f:
        f.write(name+'\t'+'\t'.join(holder)+'\n')
    return


for name, url in treat_urls[127:]:
    try:
        html = getLink(url)
        holder = parse_page(html)
    except:
        print(name,' --- fail')
        continue
    #holder = parse_page(html)
    write_file(holder, '.\\overviewData\\control.txt', name)
    print(name, ' --- done')








































