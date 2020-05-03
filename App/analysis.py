import aiohttp
import asyncio
import psycopg2.extras
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


cursor.execute('select locations from publication where locations is not null')
a = cursor.fetchall()[0][0]


print(a)
print(a['id'])