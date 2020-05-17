import psycopg2.extras
import json
from settings import PASSWORD

connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("select locations, code from publication where length(country)<1 and locations is not null ")
locations = cursor.fetchall()
save_city = []
drop_city = []
print('загрузил')
r = 0
for location in locations:

    if location['locations']['address_json'] is not None:
        if json.loads(location['locations']['address_json'])["country_code"] == '':
            drop_city.append((location['code'],))
            r += 1
        else:
            save_city.append((json.loads(location['locations']['address_json'])["country_code"], location['code']))
    else:
        r += 1
        drop_city.append((location['code'],))
print('обработал')


print(r)
for i in range(0, len(save_city), 400):
    cursor.executemany("update publication set country=%s where code=%s",save_city[i:i+400])
    connection.commit()
for i in range(0, len(drop_city), 400):
    cursor.executemany("delete from publication where code=%s",drop_city[i:i+400])
    connection.commit()
print('усе')