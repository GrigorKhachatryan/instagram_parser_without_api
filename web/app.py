import time
import json
from flask import Flask, render_template,request, jsonify
from user_data import Information
import psycopg2.extras
from settings import PASSWORD

connection = psycopg2.connect(user="lybtbdynxmmspu",
                              password=PASSWORD,
                              host="ec2-35-169-254-43.compute-1.amazonaws.com",
                              port="5432",
                              database="d34stkoqrtmabb")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

app = Flask(__name__)


@app.route("/", methods=['GET'])
def info():
    return render_template('index.html')


@app.route("/api/v1/user", methods=['GET'])
def user_api():
    login = request.args.get('instagram')
    country=[]
    obj = Information(nickname=login)
    country_code = obj.similar_users()
    with open('../analysis/clastering/country_code.json', 'r') as file:
        code = json.load(file)
    for i in country_code:
        cursor.execute('select url from Country where name=%s',(code['code'][i],))
        url_photo = cursor.fetchone()['url']
        country.append([code['code'][i], url_photo])
    return jsonify({'result': country})


if __name__ == '__main__':
    app.run()
