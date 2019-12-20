# -*- coding: utf-8 -*-
import time
import json
import math
from pprint import pprint
from selenium import webdriver

url = 'https://www.instagram.com/'
driver = webdriver.Chrome(executable_path=r"/Users/gg.khachatryan/Desktop/chromedriver")
information = {'user':[]}


# Функция, которая убирает html  теги
def parser_html(html_source):
    html_source = html_source.replace(
        r'<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">',
        '').replace(r'</pre></body></html>', '')
    return json.loads(html_source)


# Забираю данные из страницы /user/?__a=1
def user_id(login):
    user_id_url = url+login+'/?__a=1'
    driver.get(user_id_url)
    json_user = parser_html(driver.page_source)
    user = json_user['graphql']['user']['id']
    count_photo = json_user['graphql']['user']['edge_owner_to_timeline_media']['count']
    return {'user': user, 'count': count_photo}


# Создается url для парсинга shortcode фоток
def generate_url(page,id_user):
    hash_instagram = 'graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables='
    user_data = '{' + f'"id":"{id_user["user"]}","first":50,"after":"{page}"' + '}'
    url_page = url + hash_instagram + user_data
    return url_page


# Непосредственный сбор кодов фоток
def all_user_data(url_page, count):
    driver.get(url_page)
    json_user = parser_html(driver.page_source)
    for i in range(count):
        text = json_user['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['edge_media_to_caption']['edges']
        if len(text) == 0:
            text = ''
        else:
            text = text[0]['node']['text']
        photo_information = {
            'short': json_user['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode'],
            'text': text,
            'photo': json_user['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['display_url'].replace('&amp;', '&')
        }
        information['user'].append(photo_information)
    next_page = json_user['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    return next_page


# Осталось написать тело, которое будет постоянно все вызывать
def instagram_parser(login_user):

    id_user = user_id(login_user)
    end_cursor = ''
    count_all_photo = id_user['count']
    count_page = math.ceil(count_all_photo / 50)
    count_photo_page = 50 if count_all_photo > 50 else count_all_photo
    for _ in range(count_page):

        url_page_user = generate_url(end_cursor, id_user)
        end_cursor = all_user_data(url_page_user, count_photo_page)
        count_all_photo -= count_photo_page
        count_photo_page = 50 if count_all_photo > 50 else count_all_photo

    driver.quit()

    with open('result.json','w') as file:
        json.dump(information, file)

    return information


login_user_inst = input('Введите ваш ник в Instagram.  ')
photo_id = instagram_parser(login_user_inst)
print(photo_id)





