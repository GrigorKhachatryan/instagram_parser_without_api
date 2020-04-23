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
start = 33816

t = 34578


print(a['posts'][0])

loop = asyncio.get_event_loop()


async def main(ids):
    async with aiohttp.ClientSession() as session:
        for i in ids:
            print(None)
            response = await session.get(f'https://www.instagram.com/p/{i}/?__a=1',ssl=False)
            try:
                json = await response.json()

                if json['graphql']['shortcode_media']['location'] is  None:
                    print(i)
                    cursor.execute('delete from publication where code=%s', (i,))
                    connection.commit()
            except:
                print(i)
                cursor.execute('delete from publication where code=%s', (i,))
                connection.commit()





async def start():
    chunk = len(a['posts']) // 15
    start, stop = 0, chunk

    futures = []
    while stop <= len(a['posts']):
        futures.append(loop.create_task(main(a['posts'][start:stop])))
        start += chunk
        stop += chunk


    await asyncio.gather(*futures)
starts = time.time()
loop.run_until_complete(start())
print(time.time()-starts)
