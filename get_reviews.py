# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:19:09 2020

@author: 51zhu
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def parse_page(html, holder):

    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all("div", class_ = "gdReview")
    num_block = len(blocks)
    
    for block in blocks:
        try:
            stars = block.find("span", {"class":"ratingNumber mr-xsm"}).text
        except:
            stars = 'None'
        
        try:
            date = block.find("span", {"class":"authorJobTitle middle common__EiReviewDetailsStyle__newGrey"}).text
        except:
            date = 'None'
        
        try:
            long = block.find("span", {"class":"pt-xsm pt-md-0 css-1qxtz39 eg4psks0"}).text
        except:
            long = 'None'
        
        try:
            pros = block.find("span", {"data-test": "pros"}).text
            cons = block.find("span", {"data-test": "cons"}).text
        except:
            pros = 'None'
            cons = 'None'
        
        
        try:
            ceo_block = block.find_all("div", {"class":"d-flex align-items-center mr-std"})[1]
            if ceo_block.find('rect'):
                ceo = 'M'
            elif ceo_block.find('path',{'d':'M8.835 17.64l-3.959-3.545a1.19 1.19 0 010-1.735 1.326 1.326 0 011.816 0l3.058 2.677 7.558-8.678a1.326 1.326 0 011.816 0 1.19 1.19 0 010 1.736l-8.474 9.546c-.501.479-1.314.479-1.815 0z'}):
                ceo = 'G'
            elif ceo_block.find('circle'):
                ceo = 'None'
            else:
                ceo = 'B'
        except:
            ceo = 'None'
    
        try:
            rec_block = block.find_all("div", {"class":"d-flex align-items-center mr-std"})[0]
            if rec_block.find('rect'):
                rec = 'M'
            elif rec_block.find('path',{'d':'M8.835 17.64l-3.959-3.545a1.19 1.19 0 010-1.735 1.326 1.326 0 011.816 0l3.058 2.677 7.558-8.678a1.326 1.326 0 011.816 0 1.19 1.19 0 010 1.736l-8.474 9.546c-.501.479-1.314.479-1.815 0z'}):
                rec = 'G'
            elif rec_block.find('circle'):
                rec = 'None'
            else:
                rec = 'B'    
        except:
            rec = 'None'
        
        try:
            out_block = block.find_all("div", {"class":"d-flex align-items-center mr-std"})[2]
            if out_block.find('rect'):
                out = 'M'
            elif out_block.find('path',{'d':'M8.835 17.64l-3.959-3.545a1.19 1.19 0 010-1.735 1.326 1.326 0 011.816 0l3.058 2.677 7.558-8.678a1.326 1.326 0 011.816 0 1.19 1.19 0 010 1.736l-8.474 9.546c-.501.479-1.314.479-1.815 0z'}):
                out = 'G'
            elif out_block.find('circle'):
                out = 'None'
            else:
                out = 'B'    
        except:
            out = 'None'
    
        out_data_raw = [stars, date, long, pros, cons, ceo, rec, out]
        out_data = [x.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\t", " ") for x in out_data_raw]
        holder.append(out_data)         
    return num_block
        
def get_company_reviews(url, out_list):
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\51zhu\\AppData\\Local\\Google\\Chrome\\User Data\\")
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(url)
    page = 1
    time.sleep(1)
    html = driver.page_source
    num_block = parse_page(html, holder=out_list)
    if num_block < 10:
        driver.close()
        return
    print("page",page,"done")
    page +=1
    link1, link2 = url.split('.htm?')
    link1 = link1 + '_P'
    link2 = ".htm?" + link2
    while True:
        try:
#            button = driver.find_element_by_css_selector("#NodeReplace > main > div > div:nth-child(1) > div > div.eiReviews__EIReviewsPageStyles__pagination.noTabover.mt > div > div.pageContainer > button.nextButton.css-sed91k > span > svg")
 #           button.click()
            link = link1 + str(page) + link2
            driver.get(link)
            html = driver.page_source
            num_block = parse_page(html, holder=out_list)
            if num_block < 10:
                break
            print("page",page,"done")
            page +=1  
            try:
                year = out_list[-1][1].split(', ')[1].split(' -')[0]
                print(year)
            except:
                break
            if year in ['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']:
 #           if year in ['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010','2020']:    
                break
            time.sleep(1.5)
        except:
            print("Last Page Reached.")
            break
    driver.close()
    return        

def write_data(out_list, out_file):
    with open(out_file, "w", encoding = 'utf-8') as f:
        for item in out_list:
            f.write('\t'.join(item)+'\n')
    return

with open('comp_controll.csv', 'r', encoding = 'utf-8') as f:
    for line in f:
        line = line.strip().split(',')
        name = line[0]
        review_link = line[1]
        if 'eng' in review_link:
            l = []
            get_company_reviews(review_link, out_list = l)
            write_data(l, '.\\data2\\'+ name +'.txt')
        elif len(review_link) < 10:
            continue
        else:
            link = review_link + '?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng'
            l = []
            get_company_reviews(link, out_list = l)
            write_data(l, '.\\data_control\\'+ name +'.txt')            