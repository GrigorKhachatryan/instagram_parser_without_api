from flask import Flask, render_template ,request, jsonify
from Parser.Instagram_all import InstaParser
import requests
import psycopg2
import psycopg2.extras
import json
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    nick = request.args.get('nick')
    if nick == None:
        return render_template('index.html',a=0, name='введите никнейм')
    responses = requests.get(f'https://instagram.com/{nick}/?__a=1').json()
    try:
        response = responses['graphql']['user']['id']
    except:
        return jsonify(responses)
    a = InstaParser(user_id=int(response))
    r = a.instagram_parser()
    r = set(r)
    k = 0
    result = {}
    for i in r:
        json_pars = requests.get(f'https://www.instagram.com/p/{i}/?__a=1').json()
        location = json_pars['graphql']['shortcode_media']['location']
        if location is not None:
            print(location["id"])
            res = json.loads(location["address_json"])
            geo = requests.get(f'https://www.instagram.com/explore/locations/{int(location["id"])}/{res["city_name"]}?__a=1').json()
            result[str(k)]={'lat': geo['graphql']['location']['lat'],'lon': geo['graphql']['location']['lng'], 'name':res['city_name'],'photo':json_pars['graphql']['shortcode_media']["display_url"]}
            result[str(k)]['name'] = result[str(k)]['name'].replace('-',' ')
            result[str(k)]['name'] = result[str(k)]['name'].replace(',', ' ')

            if result[str(k)]['name'] is None:
                result[str(k)]['name']='Непонятно'
            result[str(k)]['name'] = result[str(k)]['name'].split(' ')[0]
            k += 1
            if k>2:
                break

    return render_template('index.html', a=result, name = nick)


if __name__ == '__main__':
    app.run(host='0.0.0.0')