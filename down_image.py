from bs4 import BeautifulSoup
import urllib3
import os
import urllib.request
import re
def down_img(url,path):
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

    #url = ("https://wiki.biligame.com/blhx/%E6%96%87%E4%BB%B6:Bg_430.png")

    http = urllib3.PoolManager()
    request = http.request('GET', url, headers=headers, retries=3)
    soup = BeautifulSoup(request.data, "html.parser")
    body_tag= soup.find("body")
    container=body_tag.find('div', attrs={'class': 'game-bg container'})
    content=container.find('div', attrs={'id': 'content'})
    bodyContent=content.find('div', attrs={'id': 'bodyContent'})
    mw_content_text=bodyContent.find('div', attrs={'id': 'mw-content-text'})
    fullMedia=mw_content_text.find('div', attrs={'class': 'fullMedia'})
    a_tag = fullMedia.find('a', class_='internal')
    href = a_tag.get('href')
    filename = os.path.basename(href)
    urllib.request.urlretrieve(href, os.path.join(path, filename))
    print("Download Success: " + href)