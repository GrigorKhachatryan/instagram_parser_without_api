import time
import json
from flask import Flask, render_template,request, jsonify
import os
import redis
import psycopg2.extras
from rq import Queue
from rq.job import Job
from tasks import insta_tasks
from settings import PASSWORD, DATABASE, USER
from worker import conn

connection = psycopg2.connect(user=USER,
                              password=PASSWORD,
                              host="ec2-52-72-65-76.compute-1.amazonaws.com",
                              port="5432",
                              database=DATABASE)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
q = Queue(connection=conn)
app = Flask(__name__)


@app.route("/api/v1/task", methods=['GET'])
def info():
    login = request.args.get('instagram')
    cursor.execute('select * from resorts where login=%s', (login,))
    user = cursor.fetchone()
    if user == None:
        cursor.execute('insert into resorts(login) values(%s)', (login,))
        connection.commit()
    a = q.enqueue(insta_tasks, login)

    return a.key

@app.route("/get_word_count_result/<job_key>", methods=['GET'])
def get_word_count_result(job_key):
    job_key = job_key.replace("rq:job:", "")
    job = Job.fetch(job_key, connection=conn)

    if(not job.is_finished):
        return "Not yet", 202
    else:
        return str(job.result), 200

@app.route("/api/v1/user", methods=['GET'])
def user_api():
    login = request.args.get('instagram')
    country = []
    cursor.execute('select * from resorts where login=%s', (login,))
    user_country = cursor.fetchone()
    if user_country['country1'] is None:
        return jsonify({'result': []})
    country_code = [user_country['country1'], user_country['country2'], user_country['country3']]
    with open('../analysis/clastering/country_code.json', 'r') as file:
        code = json.load(file)
    for i in country_code:
        cursor.execute('select url from Country where name=%s',(code['code'][i],))
        url_photo = cursor.fetchone()['url']
        country.append([code['code'][i], url_photo])
    return jsonify({'result': country})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
