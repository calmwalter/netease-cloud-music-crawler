from bs4 import BeautifulSoup
import re
import os
import time
import requests
from selenium import webdriver
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def find_billboard():  # 找到所有榜单
    url = "https://music.163.com/#/discover/toplist"
    browser = webdriver.Firefox()
    browser.get(url)
    browser.switch_to.frame("contentFrame")
    time.sleep(1)
    html = BeautifulSoup(browser.page_source, 'html.parser')
    lst = html.find_all('li', attrs={'data-res-id': True, 'data-res-action': True, 'class': True})
    info = []
    for i in range(len(lst)):
        billboard_id = re.sub(r'/discover/toplist\?id=(.*?)', "",
                              lst[i].find('p', attrs={'class': 'name'}).find('a').get('href'))
        billboard_name = lst[i].find('p', attrs={'class': 'name'}).find('a').get_text()
        print(billboard_id, billboard_name)
        info.append((billboard_id, billboard_name))
    browser.close()
    return info


def find_song(url):  # 获得音乐的名字和id
    browser = webdriver.Firefox()
    browser.get(url)
    browser.switch_to.frame("contentFrame")
    time.sleep(1)
    html = BeautifulSoup(browser.page_source, 'html.parser')
    lst = html.find('tbody').find_all('tr', attrs={'id': True, 'class': True})
    info = []
    for i in range(len(lst)):
        song_id = re.sub(r'/song\?id=(.*?)', "", lst[i].find('span', attrs={'class': 'txt'}).find('a').get('href'))
        song_name = re.sub(r'(.*?)/(.*?)', " ", lst[i].find('span', attrs={'class': 'txt'}).find('b').get('title'))
        singer = re.sub(r'(.*?)/(.*?)', " ", lst[i].find('div', attrs={'class': 'text', 'title': True}).get('title'))
        info.append((song_id, song_name, singer))
        print(song_id, song_name, singer)
    browser.close()
    return info


def download_music(info, billboard):  # 把音乐写入到文件
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if not os.path.exists('./tmp/'+billboard):
        os.mkdir('./tmp/'+billboard)
    for music in info:
        song = 'http://music.163.com/song/media/outer/url?id=' + music[0] + '.mp3'
        try:
            print("Writing", music[1], "to file...")
            f = open('./tmp/'+billboard+'/'+music[1]+'-'+music[2]+'.mp3', 'wb')
            music = requests.get(song, headers=headers)
            f.write(music.content)
            f.close()
        except Exception as error:
            print(error)


for billboard in find_billboard():  # 执行运行操作
    download_music(find_song('https://music.163.com/#/discover/toplist?id='+billboard[0]), billboard[1])

