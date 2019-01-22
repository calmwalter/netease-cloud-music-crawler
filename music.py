from bs4 import BeautifulSoup
import re
import os
import time
import requests
from selenium import webdriver
# 获得音乐的名字和id
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
url = "https://music.163.com/#/discover/toplist"
browser = webdriver.Firefox()
browser.get(url)
browser.switch_to.frame("contentFrame")
time.sleep(1)
html = BeautifulSoup(browser.page_source, 'html.parser')
rank = str(html.find('tbody'))
regex = re.compile('<span class=\"txt\"><a href=\"/song\?id=(.*?)\"><b title=\"(.*?)\">')
info = regex.findall(rank)

# 把音乐写入到文件
if not os.path.exists('tmp'):
    os.mkdir('tmp')
for music in info:
    songUrl = 'http://music.163.com/song/media/outer/url?id=' + music[0] + '.mp3'
    try:
        print("Writing", music[1], "to file...")
        f = open('./tmp/'+music[1]+'.mp3', 'wb')
        music = requests.get(songUrl, headers=headers)
        f.write(music.content)
        f.close()
        time.sleep(0.1)
    except Exception as error:
        print(error)
