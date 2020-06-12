import flask
from flask_cors import CORS
from flask import Flask, redirect, render_template, url_for, request
import os
import json
import numpy as np

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


@app.route('/bmap')
def bmap():
    return render_template('effect_bmap.html')


# dataset routing
@app.route('/dataset1')
def dataset1():
    # input geojson
    path = os.getcwd()
    with open('./data/geo/全国.json', 'r', encoding='utf-8') as f:
        geojson = json.loads(f.read())  # str2dict

    # input earthquake info
    with open('./data/seismic/earthquake_info.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())

    with open('./data/seismic/earthquake.csv', 'r', encoding='utf-8') as f:
        f.readline()
        earthquakes = []
        not_word = ['日本', '俄罗', '巴坦', '吉尔', '印尼', '菲律', '琉球', '克什', '印度', '棉兰', '老挝', '缅甸', '先岛', '蒙古']
        for line in f.readlines():
            earthquake = []
            temp = line.strip().split(',')
            # time,mag,lat,lng,depth,loc -> lng,lat,time,loc,mag,depth
            if temp[-1][:2] not in not_word:
                earthquake.append('%.3f' % float(temp[3]))  # lng
                earthquake.append('%.3f' % float(temp[2]))  # lat
                earthquake.append(temp[0])  # time
                earthquake.append(temp[5])  # loc
                earthquake.append('%.1f' % float(temp[1]))  # mag
                earthquake.append('%.0f' % float(temp[4]))  # depth
                earthquakes.append(earthquake)

    # dumping
    dataset = {'geojson': geojson, 'info': info, 'earthquakes': earthquakes}

    return dataset


@app.route('/dataset2')
def dataset2():
    # input geojson
    geojson = {'type': 'FeatureCollection', 'features': []}
    with open('./data/geo/河北省.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']
    with open('./data/geo/北京市.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']
    with open('./data/geo/天津市.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']

    # input earthquake info
    with open('./data/seismic/earthquake_info.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())

    # input distribution data
    all_station_data = np.loadtxt(
        './data/station_damage/station_damage_all.csv',
        delimiter=",",
        dtype="str",
    )

    damage_frame, damage_shear, damage_un_ma, damage_re_ma, damage_tu_mu, damage_hu_zo, PGA = [], [], [], [], [], [], []
    for damage in all_station_data:
        damage = damage[3:]
        damage_frame.append(damage[0:5].tolist())
        damage_shear.append(damage[5:10].tolist())
        damage_un_ma.append(damage[10:15].tolist())
        damage_re_ma.append(damage[15:20].tolist())
        damage_tu_mu.append(damage[20:25].tolist())
        damage_hu_zo.append(damage[25:30].tolist())
        PGA.append(damage[30:33].tolist())

    def get_damage_idx(damage):
        assert len(damage) == 5
        damage = list(map(float, damage))
        idx = 0 * damage[0] + 1 * damage[1] + 2 * damage[2] + 3 * damage[3] + 4 * damage[4]
        return idx / 4

    # input station info
    with open('./data/seismic/station.txt', 'r') as f:
        f.readline()
        stations = []
        for i, line in enumerate(f.readlines()):
            station = []
            temp = line.strip('\n').split()

            # name,ew,ns,ud,lat,lng -> lng,lat,name,ew,ns,ud
            station.append('%.3f' % float(temp[5]))  # lng
            station.append('%.3f' % float(temp[4]))  # lat
            station.append(temp[0])  # name
            station.append('%.3f' % float(temp[1]))  # ew
            station.append('%.3f' % float(temp[2]))  # ns
            station.append('%.3f' % float(temp[3]))  # ud

            # add damage index
            station.append('%.3f' % float(get_damage_idx(damage_frame[i])))
            station.append('%.3f' % float(get_damage_idx(damage_shear[i])))
            station.append('%.3f' % float(get_damage_idx(damage_un_ma[i])))
            station.append('%.3f' % float(get_damage_idx(damage_re_ma[i])))
            station.append('%.3f' % float(get_damage_idx(damage_tu_mu[i])))
            station.append('%.3f' % float(get_damage_idx(damage_hu_zo[i])))

            stations.append(station)

    stations_array = np.array(stations)
    stations_heat = []
    for i in range(6, 12):  # all the damage index
        idx = [0, 1, i]
        stations_heat.append(stations_array[:, idx].tolist() * 20)  # add data by *n to make visualization more obvious

    # dumping
    dataset = {'geojson': geojson, 'info': info, 'stations': stations, 'stations_heat': stations_heat}

    return dataset


@app.route('/dataset3')
def dataset3():
    # input geojson
    geojson = {'type': 'FeatureCollection', 'features': []}
    with open('./data/geo/河北省.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']
    with open('./data/geo/北京市.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']
    with open('./data/geo/天津市.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']

    # input earthquake info
    with open('./data/station_damage/earthquake_info.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())

    # input distribution data
    all_station_data = np.loadtxt('./data/station_damage/station_damage_all.csv', delimiter=",", dtype="str")
    use_cols = np.arange(3, all_station_data.shape[1], 1)
    stations_inf = all_station_data[:, 0:3]
    all_station_inf = []
    for inf in stations_inf:
        all_station_inf.append(inf.tolist())
    all_station_data = np.loadtxt('./data/station_damage/station_damage_all.csv',
                                  delimiter=",",
                                  dtype="float",
                                  usecols=use_cols)

    damage_frame, damage_shear, damage_un_ma, damage_re_ma, damage_tu_mu, damage_hu_zo, PGA = [], [], [], [], [], [], []
    for damage in all_station_data:
        damage_frame.append(damage[0:5].tolist())
        damage_shear.append(damage[5:10].tolist())
        damage_un_ma.append(damage[10:15].tolist())
        damage_re_ma.append(damage[15:20].tolist())
        damage_tu_mu.append(damage[20:25].tolist())
        damage_hu_zo.append(damage[25:30].tolist())
        PGA.append(damage[30:33].tolist())
    # print(damage_frame, "\n", damage_shear, "\n", damage_un_ma, "\n", damage_re_ma, "\n", damage_tu_mu, "\n", PGA)
    # print(damage_frame, "\n", damage_shear, "\n", damage_un_ma, "\n", damage_re_ma, "\n", damage_tu_mu, "\n", PGA)
    # print(type(all_station_damage), all_station_inf)
    dataset = {
        'geojson': geojson,
        'info': info,
        'station_inf': all_station_inf,
        'damage_frame': damage_frame,
        'damage_shear': damage_shear,
        'damage_un_ma': damage_un_ma,
        'damage_re_ma': damage_re_ma,
        'damage_tu_mu': damage_tu_mu,
        'damage_hu_zo': damage_hu_zo,
        'PGA': PGA
    }
    return dataset


@app.route('/dataset4')
def dataset4():
    # input geojson
    geojson = {'type': 'FeatureCollection', 'features': []}
    with open('./data/geo/河北省.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']
    with open('./data/geo/北京市.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']
    with open('./data/geo/天津市.json', 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())  # str2dict
        geojson['features']+=temp['features']

    # input earthquake info

    with open('./data/station_damage/earthquake_info.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())

    # input distribution data
    all_station_data = np.loadtxt('./data/station_damage/station_damage_all.csv', delimiter=",", dtype="str")
    use_cols = np.arange(3, all_station_data.shape[1], 1)
    all_station_data = np.loadtxt('./data/station_damage/station_damage_all.csv',
                                  delimiter=",",
                                  dtype="float",
                                  usecols=use_cols)

    damage_frame_d, damage_shear_d, damage_un_ma_d, damage_re_ma_d, damage_tu_mu_d, damage_hu_zo_d = [], [], [], [], [], []
    for damage in all_station_data:
        damage_frame_d.append(damage[0:5].tolist())
        damage_shear_d.append(damage[5:10].tolist())
        damage_un_ma_d.append(damage[10:15].tolist())
        damage_re_ma_d.append(damage[15:20].tolist())
        damage_tu_mu_d.append(damage[20:25].tolist())
        damage_hu_zo_d.append(damage[25:30].tolist())

    dataset_d = {
        'damage_frame': damage_frame_d,
        'damage_shear': damage_shear_d,
        'damage_un_ma': damage_un_ma_d,
        'damage_re_ma': damage_re_ma_d,
        'damage_tu_mu': damage_tu_mu_d,
        'damage_hu_zo': damage_hu_zo_d,
    }
    all_station_data = np.loadtxt('./data/station_damage/station_damage_all_+1.csv', delimiter=",", dtype="str")
    use_cols = np.arange(1, all_station_data.shape[1], 1)
    all_station_inf = all_station_data[:, 0].tolist()
    all_station_data = np.loadtxt('./data/station_damage/station_damage_all_+1.csv',
                                  delimiter=",",
                                  dtype="float",
                                  usecols=use_cols)

    damage_frame, damage_shear, damage_un_ma, damage_re_ma, damage_tu_mu, damage_hu_zo = [], [], [], [], [], []
    for damage in all_station_data:
        damage_frame.append(damage[0:5].tolist())
        damage_shear.append(damage[5:10].tolist())
        damage_un_ma.append(damage[10:15].tolist())
        damage_re_ma.append(damage[15:20].tolist())
        damage_tu_mu.append(damage[20:25].tolist())
        damage_hu_zo.append(damage[25:30].tolist())

    dataset_p = {
        'station_inf': all_station_inf,
        'damage_frame': damage_frame,
        'damage_shear': damage_shear,
        'damage_un_ma': damage_un_ma,
        'damage_re_ma': damage_re_ma,
        'damage_tu_mu': damage_tu_mu,
        'damage_hu_zo': damage_hu_zo
    }

    all_station_data = np.loadtxt('./data/station_damage/station_damage_all_-1.csv',
                                  delimiter=",",
                                  dtype="float",
                                  usecols=use_cols)

    damage_frame_m, damage_shear_m, damage_un_ma_m, damage_re_ma_m, damage_tu_mu_m, damage_hu_zo_m = [], [], [], [], [], []
    for damage in all_station_data:
        damage_frame_m.append(damage[0:5].tolist())
        damage_shear_m.append(damage[5:10].tolist())
        damage_un_ma_m.append(damage[10:15].tolist())
        damage_re_ma_m.append(damage[15:20].tolist())
        damage_tu_mu_m.append(damage[20:25].tolist())
        damage_hu_zo_m.append(damage[25:30].tolist())

    dataset_m = {
        'station_inf': all_station_inf,
        'damage_frame': damage_frame_m,
        'damage_shear': damage_shear_m,
        'damage_un_ma': damage_un_ma_m,
        'damage_re_ma': damage_re_ma_m,
        'damage_tu_mu': damage_tu_mu_m,
        'damage_hu_zo': damage_hu_zo_m
    }

    dataset = {'geojson': geojson, 'info': info, "dataset_p": dataset_p, "dataset_m": dataset_m, "dataset_d": dataset_d}
    return dataset


@app.route('/dataset_GM')
def GM_data():
    station_name = dict(request.args)
    station_name = list(station_name.keys())[0]
    # print(station_name)
    assert os.path.exists("./data/ground motion/%s" % station_name)
    EW = np.loadtxt("./data/ground motion/%s/EW.txt" % station_name, skiprows=1, delimiter="	", dtype="float")
    NS = np.loadtxt("./data/ground motion/%s/NS.txt" % station_name, skiprows=1, delimiter="	", dtype="float")
    UD = np.loadtxt("./data/ground motion/%s/UD.txt" % station_name, skiprows=1, delimiter="	", dtype="float")
    EW_time = EW[:, 0].tolist()
    NS_time = NS[:, 0].tolist()
    UD_time = UD[:, 0].tolist()
    EW_ACCE = EW[:, 1].tolist()
    NS_ACCE = NS[:, 1].tolist()
    UD_ACCE = UD[:, 1].tolist()

    dataset = {
        'station_name': station_name,
        'EW_time': EW_time,
        'NS_time': NS_time,
        'UD_time': UD_time,
        'EW_ACCE': EW_ACCE,
        'NS_ACCE': NS_ACCE,
        'UD_ACCE': UD_ACCE
    }

    return dataset


@app.route('/dataset_Spectrum')
def Spectrum_data():
    station_name = dict(request.args)
    station_name = list(station_name.keys())[0]
    # print(station_name)
    assert os.path.exists("./data/ground motion/%s" % station_name)
    EW = np.loadtxt("./data/ground motion/%s/EW_Spectrum.txt" % station_name, skiprows=0, delimiter=" ", dtype="float")
    NS = np.loadtxt("./data/ground motion/%s/NS_Spectrum.txt" % station_name, skiprows=0, delimiter=" ", dtype="float")
    UD = np.loadtxt("./data/ground motion/%s/UD_Spectrum.txt" % station_name, skiprows=0, delimiter=" ", dtype="float")
    EW_Spectrum = EW.tolist()
    NS_Spectrum = NS.tolist()
    UD_Spectrum = UD.tolist()
    time = np.arange(0, 6.05, 0.05)
    time = time.tolist()

    dataset = {
        'station_name': station_name,
        "time": time,
        'EW_Spectrum': EW_Spectrum,
        'NS_Spectrum': NS_Spectrum,
        'UD_Spectrum': UD_Spectrum
    }

    return dataset


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
