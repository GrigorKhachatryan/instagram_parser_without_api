import psycopg2.extras
import json
from settings import PASSWORD

connection = psycopg2.connect(user="lybtbdynxmmspu",
                              password=PASSWORD,
                              host="ec2-35-169-254-43.compute-1.amazonaws.com",
                              port="5432",
                              database="d34stkoqrtmabb")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

with open('../analysis/clastering/country_code.json', 'r') as file:
    code = json.load(file)

country = tuple((i,) for i in code['code'].values())

cursor.executemany('insert into Country (name) values(%s)', country)
connection.commit()
