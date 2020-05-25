from user_data import Information
import psycopg2.extras
from settings import PASSWORD, DATABASE, USER

connection = psycopg2.connect(user=USER,
                              password=PASSWORD,
                              host="ec2-52-72-65-76.compute-1.amazonaws.com",
                              port="5432",
                              database=DATABASE)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def insta_tasks(login):
    # obj = Information(nickname=login)
    # country_code = obj.similar_users()
    cursor.execute('update resorts set country1=%s, country2=%s, country3=%s where login=%s',
                   ('aa', 'vv', 'cc', login))
    connection.commit()
    return 'ok'
