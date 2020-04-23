import psycopg2.extras
from pprint import pprint
from Parser.Instagram_all import InstaParser
from settings import PASSWORD
connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


number = int(input('С какого id начать:  '))

for instagram_id in range(number, number+100000):
    a = InstaParser(user_id=instagram_id)
    t = a.instagram_parser()
    if t == []:
        print('Аккаунт - ' + str(instagram_id) + ' пустой или закрытый')
        continue
    cursor.execute('insert into Client (id) values (%s)', (instagram_id,))
    connection.commit()
    short_code = []
    count = 0
    t = set(t)
    for i in t:
        if count < 400:
            short_code.append((i, instagram_id))
            count += 1
        else:
            sql_query_insert = "insert into Publication (code,client_id) values (%s,%s)"
            cursor.executemany(sql_query_insert, short_code)
            connection.commit()
            count = 0
            short_code = []
    if count > 0:
        sql_query_insert = "insert into Publication (code,client_id) values (%s,%s)"
        cursor.executemany(sql_query_insert, short_code)
        connection.commit()
    pprint('Аккаунт - ' + str(instagram_id) + ', данные получены')

