import json
import psycopg2
import psycopg2.extras
from Instagram_all import InstaParser
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
start = 30548
t = 30548
for i in a['posts'][start:]:
    a = InstaParser()
    location = a.pars_code(i)['graphql']['shortcode_media']['location']
    if location is None:
        cursor.execute('delete from publication where code=%s',(i[0],))
        connection.commit()
    print(i,t)
    t += 1


