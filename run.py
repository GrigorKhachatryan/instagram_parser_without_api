import aiohttp
import asyncio
import json
import psycopg2.extras
import time
from settings import PASSWORD


connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# cursor.execute('select code from publication')
# publication = cursor.fetchall()
# json_out = {'posts':[]}
# for i in publication:
#     json_out['posts'].append(i[0])
#
# with open('posts.json','w') as file:
#     json.dump(json_out,file)
with open('posts.json','r') as file:
    a = json.load(file)

nest = a['posts'][:1050000]


async def main(ids):
    async with aiohttp.ClientSession() as session:
        for i in ids:


            try:
                response = await session.get(f'https://www.instagram.com/p/{i}/?__a=1', ssl=False)
                json = await response.json()

                if json['graphql']['shortcode_media']['location'] is  None:

                    short_list.append((str(i),))

            except:
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
print(len(a['posts']))
for i in range(2700000,len(a['posts']),30000):

    short_list = []
    k = a['posts'][i:i+30000]
    print(i,i+30000)
    loop = asyncio.get_event_loop()
    starts = time.time()
    loop.run_until_complete(start())
    print(time.time() - starts)

    cursor.executemany('delete from publication where code=%s', short_list)
    connection.commit()
    cursor.execute('select count(*) from publication')
    print(cursor.fetchone())