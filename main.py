from requests.adapters import HTTPAdapter
from logging import Logger
from modulefinder import LOAD_CONST
from turtle import title
import urllib.request as req
from xml.dom.minidom import Identified
from bs4 import BeautifulSoup
import urllib3
import os
from down_image import down_img
import time
import re

def set_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}
    http = urllib3.PoolManager()
    request = http.request('GET', url, headers=headers, retries=3)
    soup = BeautifulSoup(request.data, "html.parser")
    return soup


def pic_related(soup):
    body_tag= soup.find("body")

    container=body_tag.find('div', attrs={'class': 'game-bg container'})

    content=container.find('div', attrs={'id': 'content'})
    bodyContent=content.find('div', attrs={'id': 'bodyContent'})
    mw_content_text=bodyContent.find('div', attrs={'id': 'mw-content-text'})

    mw_parser_output=mw_content_text.find('div', attrs={'class': 'mw-parser-output'})
    return mw_parser_output

def now_img(mw_parser_output):
    ##---------login_pic--------------------------
    center_element = mw_parser_output.find('center')
    center=center_element.find_all('div', attrs={'class': 'center'})
    image_links = []
    for div in center:
        a_tags = div.find_all('a', class_='image')
        for a in a_tags:
            href = a.get('href')
            image_links.append(href)


    # #--------過場圖------------------
    mw_gallery_traditional = center_element.find('ul', attrs={'class': 'gallery mw-gallery-traditional'})
    gallerybox = mw_gallery_traditional.find_all('li', attrs={'class': 'gallerybox'})
    for div in gallerybox:
        a_tags = div.find_all('a', class_='image')
        for a in a_tags:
            href = a.get('href')
            image_links.append(href)
    #print(image_links)

    if not os.path.exists('当前登录图_过场图'):
        os.makedirs("当前登录图_过场图")
    else:
        pass
    print("Download 当前登录图_过场图")
    for image_link in image_links:
        # with open("当前登录图_过场图/test.txt", 'w', encoding='utf-8') as f:
        #     f.write('Hello, world!')
        time.sleep(5)
        down_img("wiki.biligame.com" + image_link,"当前登录图_过场图")
    print("All 当前登录图_过场图 Download Success")

#-------------old_img------------------
def old_img(mw_parser_output):
    panel_group=mw_parser_output.find('div', attrs={'class': 'panel-group'})
    panel_info=panel_group.find_all('div', attrs={'class': 'panel panel-info'})
    print("Download 其他")
    total_pic=0
    counter=0
    for tmp in panel_info:
        span_tmp=tmp.find('span', attrs={'class': 'panel-title pull-left'})
        span = span_tmp.find('span', attrs={'style': 'font-weight:bold;color: #31708f'})
        span_text= span.text
        span_text=re.sub("\:|\*|\?|\/",",",span_text)
        #print(span_text)
        if not os.path.exists(span_text):
            os.makedirs(span_text)
        else:
            pass
        mw_gallery_traditiona_o = tmp.find('div', attrs={'class': 'panel-body panel-collapse collapse'})
        gallerybox_o = mw_gallery_traditiona_o.find_all('li', attrs={'class': 'gallerybox'})

        url_tag = [img.find('a', class_='image') for img in gallerybox_o]
        urls = [tag.get('href') for tag in url_tag if tag is not None]
        for i in urls:
            time.sleep(5)
            print("Download in :" + span_text)
            down_img("wiki.biligame.com" + i,span_text)
            counter=counter+1
        total_pic += len(urls)
    print(counter)
    print(total_pic)
    print("All Download 其他 Success")


def artist_pic(mw_parser_output):
    mw_gallery_packed_hover = mw_parser_output.find_all('ul', attrs={'class': 'gallery mw-gallery-packed-hover'})
    if not os.path.exists("画师贺图、同人图合集"):
        os.makedirs("画师贺图、同人图合集")
    else:
        pass
    print("Download 画师贺图、同人图合集")
    with open('画师贺图、同人图合集/lost_pic.txt', 'w', encoding='utf-8') as f:
        for i in mw_gallery_packed_hover :
            gallerybox = i.find_all('li', attrs={'class': 'gallerybox'})
            for tmp in gallerybox:
                thumb=tmp.find('div', attrs={'class': 'thumb'})
                image_a = thumb.find("a", {"class": "image"})
                if image_a is not None:
                    urls = image_a["href"]
                    # print(urls)
                    # print("\n")
                else:
                    print("Error: Could not extract URL from the following HTML:\n" + str(thumb) + "\n")
                    f.write("Error: Could not extract URL from the following HTML:\n" + str(thumb) + "\n")
        print("All 画师贺图、同人图合集 Download Success")



def main():
    #---------------------------------------
    url = ("https://wiki.biligame.com/blhx/%E5%BD%B1%E7%94%BB%E7%9B%B8%E5%85%B3")
    soup=set_url(url)
    mw_parser_output= pic_related(soup)
    now_img(mw_parser_output)
    old_img(mw_parser_output)
    #----------------------------------------
    url = ("https://wiki.biligame.com/blhx/%E7%94%BB%E5%B8%88%E8%B4%BA%E5%9B%BE%E3%80%81%E5%90%8C%E4%BA%BA%E5%9B%BE%E5%90%88%E9%9B%86#%E6%97%A5%E6%9C%8D%E4%BA%94%E5%91%A8%E5%B9%B4%E8%B4%BA%E5%9B%BE")
    soup=set_url(url)
    mw_parser_output= pic_related(soup)
    artist_pic(mw_parser_output)

if __name__ == '__main__':
    main()



