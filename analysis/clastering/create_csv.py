import pandas as pd
import numpy as np
import asyncio
import time
import json
import psycopg2.extras
from settings import PASSWORD
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import csv

dsn = f'dbname=postgres user=postgres password={PASSWORD} host=localhost port=5434'
connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres"
                              )
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
starts = time.time()

cursor.execute('select distinct client_id from publication where point is not null and country is not null and language=%s ',('en',))
instagram_user_id = cursor.fetchall()
data_pars_location = tuple(str(i['client_id']) for i in instagram_user_id)
len_data_user = len(data_pars_location)
print('sdelal')



cursor.execute('select client_id,country,avg(point) as point from publication where client_id in %s and language=%s and country is not null and point is not null group by client_id,country',[data_pars_location,'en'])
user_location = cursor.fetchall()
print(f'poluchil user_location {len(user_location)}')


print(time.time() - starts)


with open('country_code.json','r') as file:
    country_code = json.load(file)
country_code = country_code['code'].keys()
print(country_code)

print(len(instagram_user_id), len(country_code))

zero_data = np.zeros(shape=(len_data_user,len(country_code)))

df = pd.DataFrame(zero_data,columns=country_code, index=data_pars_location)

del(zero_data)
del(instagram_user_id)
del(data_pars_location)
print('удалил')
    # df[int(data['id_location'])][str(data['client_id'])] = int(data['point'])+1

print(df)
def save_data(data):
    for i in data:
        try:
            df[i['country']][str(i['client_id'])] = int(i['point'])+1
        except KeyError as err:
            print(err)
            print('вот чего не хватает')
            print(i)



for j in range(0, len(user_location), 50):
    k = user_location[j:j+50]
    save_data(k)

print(df)
# km = KMeans()
# visualizer = KElbowVisualizer(km, k=(35,100))
# predicted = visualizer.fit(df)
# visualizer.show()

km = KMeans(n_clusters=49, init='k-means++', random_state=0)

predicted = km.fit_predict(df)

cluster_centers = km.labels_
prd = pd.DataFrame(predicted, index=df.index)
print('центроиды')
a = km.cluster_centers_
print('-----')
with open('centroid.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(a)
print(cluster_centers)
prd.to_csv('app.csv')

df.to_csv('roo.scv')
print(predicted)



