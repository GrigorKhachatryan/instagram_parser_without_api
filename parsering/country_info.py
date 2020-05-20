import requests
import json
import re
import psycopg2.extras
from settings import PASSWORD

connection = psycopg2.connect(user="lybtbdynxmmspu",
                              password=PASSWORD,
                              host="ec2-35-169-254-43.compute-1.amazonaws.com",
                              port="5432",
                              database="d34stkoqrtmabb")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

url = 'https://yandex.ru/images/search?text={}&isize=eq&iw=560&ih=560'
img_country = []
while True:
    cursor.execute('select name from Country where url is null')
    country = cursor.fetchone()
    header = {
        'user-agent': 'Mozilla / 5.0(Macintosh;Intel Mac OS X 10_15_3) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 81.0.4044.129Safari / 537.36'
    }
    response = requests.get(url.format(country['name']), headers=header)

    json_user = response.text

    text = re.findall('"img_href":"(.+?)"', json_user)
    print(country['name'])
    cursor.execute('update Country set url=%s where name=%s',(text[0],country['name']))
    connection.commit()

print(img_country)