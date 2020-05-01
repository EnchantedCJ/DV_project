import flask
from flask_cors import CORS
from flask import Flask, redirect, render_template, url_for

import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

# page routing
@app.route('/')
def index():
    return redirect('/level1')


@app.route('/level1')
def level1():
    return render_template('level1.html')


@app.route('/level2')
def level2():
    return render_template('level2.html')


@app.route('/level3')
def level3():
    return render_template('level3.html')


@app.route('/level4')
def level4():
    return render_template('level4.html')

# dataset routing
@app.route('/dataset1')
def dataset1():
    # input geojson
    with open('./data/geo/全国.json', 'r', encoding='utf-8') as f:
        geojson = json.loads(f.read())  # str2dict

    # input earthquake info
    with open('./data/seismic/earthquake_info.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())

    # dumping
    dataset = {
        'geojson': geojson,
        'info': info
    }

    return dataset


@app.route('/dataset2')
def dataset2():
    # input geojson
    with open('./data/geo/Hebei_county.geojson', 'r', encoding='utf-8') as f:
        geojson = json.loads(f.read())  # str2dict

    # input earthquake info
    with open('./data/seismic/earthquake_info.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())

    # input distribution data
    # TODO
    # features = geojson['features']
    # data = [{
    #     'name': feature['properties']['name'],
    #     'value':float(feature['properties']['AREA'])  # testing!!!!
    # } for feature in features]

    # input station info
    with open('./data/seismic/station.txt', 'r', encoding='utf-8') as f:
        f.readline()
        stations = []
        for line in f.readlines():
            station = []
            temp = line.strip('\n').split()
            # name,ew,ns,ud,lat,lng -> lng,lat,name,ew,ns,ud
            station.append('%.3f' % float(temp[5]))  # name
            station.append('%.3f' % float(temp[4]))  # name
            station.append(temp[0])  # name
            station.append('%.3f' % float(temp[1]))  # name
            station.append('%.3f' % float(temp[2]))  # name
            station.append('%.3f' % float(temp[3]))  # name
            stations.append(station)
    # TODO: station damage

    # dumping
    dataset = {
        'geojson': geojson,
        'info': info,
        'stations': stations
        # 'data': data
    }

    return dataset


@app.route('/dataset3')
def dataset3():
    pass


@app.route('/dataset4')
def dataset4():
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
