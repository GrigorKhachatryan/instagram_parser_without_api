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
    country_code = ['aa','vv','cc']
    return country_code
