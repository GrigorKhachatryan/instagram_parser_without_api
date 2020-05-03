import aiohttp
import asyncio
import psycopg2.extras
from psycopg2.extras import Json
import time
import json
import hashlib
from settings import PASSWORD


connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)




async def main(ids):
    async with aiohttp.ClientSession() as session:
        for i in ids:
            response = await session.get(f'https://www.instagram.com/p/{i}/?__a=1', ssl=False)
            if response.status != 200:
                if response.status == 404:
                    short_list.append((str(i),))
                continue
            try:
                json_res = await response.json()
            except BaseException as err:
                print(err)
            try:
                if json_res['graphql']['shortcode_media']['location'] is None:
                    short_list.append((str(i),))
                    continue

                text_list.append((json_res['graphql']['shortcode_media']["edge_media_to_caption"]["edges"][0]["node"]["text"], Json(json_res['graphql']['shortcode_media']['location']), str(i)))
            except IndexError as err:
                print(err, json_res['graphql']['shortcode_media']["edge_media_to_caption"]["edges"])
                short_list.append((str(i),))


async def start():
    chunk = len(k) // 30
    start, stop = 0, chunk

    futures = []
    while stop <= len(k):
        futures.append(loop.create_task(main(k[start:stop])))
        start += chunk
        stop += chunk

    await asyncio.gather(*futures)


while True:

    cursor.execute('select code from publication where locations is null')
    publication = cursor.fetchall()
    a = {'posts': []}
    for i in publication:
        a['posts'].append(i[0])
    print(len(a['posts']))
    short_list = []
    text_list = []
    k = a['posts'][0:300]
    loop = asyncio.get_event_loop()
    starts = time.time()
    try:
        loop.run_until_complete(start())
    except BaseException as err:
        print(err)
    print(time.time() - starts)

    cursor.executemany('delete from publication where code=%s', short_list)
    connection.commit()

    cursor.executemany('update publication set posts=%s, locations=%s where code=%s',text_list)
    connection.commit()

    print(f'Удалено {len(short_list)} постов.')
    print(f'Текст добавлен у {len(text_list)} постов.')

