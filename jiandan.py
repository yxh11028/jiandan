# coding: utf-8

import os
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver

file_dir = "D:/IMG/jiandan/"

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

index_url = 'http://jandan.net/ooxx'
driver = webdriver.Chrome('D:\\chromedriver.exe')
driver.get(index_url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
page_count = int(soup.find("span", class_="current-comment-page").get_text().strip('\[\]'))

while page_count >= 1:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_urls = soup.find_all("a", class_="view_img_link")

    if os.path.exists(file_dir + str(page_count)):
        print str(page_count) + " 已采集过\n"

        driver.find_element_by_xpath('//a[@class="previous-comment-page"]').click()
        page_count = page_count - 1
        continue
    else:
        os.makedirs(file_dir + str(page_count))

        for tag in img_urls:
            img = "http:" + tag['href']
            request = urllib2.Request(img, headers=header)
            response = urllib2.urlopen(request)
            with open(file_dir + str(page_count) + "/" + img.split("/")[4], "wb") as f:
                f.write(response.read())
                print img + "  " + "Done"

        driver.find_element_by_xpath('//a[@class="previous-comment-page"]').click()
        page_count = page_count - 1
