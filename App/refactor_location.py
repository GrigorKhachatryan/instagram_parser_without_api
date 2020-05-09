import psycopg2.extras
from settings import PASSWORD

connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("select locations, code from publication where id_location is null")
locations = cursor.fetchall()
data = []
print('загрузил')
for location in locations:

    data.append((location['locations']['id'], location['code']))
print('обработал')
for i in range(0, len(data), 400):
    cursor.executemany("update publication set id_location=%s where code=%s",data[i:i+400])
    connection.commit()
print('усе')