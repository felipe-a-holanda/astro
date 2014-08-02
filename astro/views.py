from astro import app
from flask import Flask, jsonify, render_template, request

import swisseph as swe
import subprocess
from datetime import datetime
from collections import namedtuple

from make_svg_chart import get_chart

@app.route('/_calc_planets')
def calc_planets():
    Planet = namedtuple('Planet', ['name', 'angle', 'sign'])
    planet_names = ['Sol', 'Lua', 'Mercurio', 'Venus', 'Marte', 'Jupiter','Saturno', 'Urano', 'Netuno' ,'Plutao']
    signs = ['Aries', 'Touro', 'Gemeos', 'Cancer', 'Leao', 'Virgem', 'Libra', 'Escorpiao', 'Sagitario', 'Capricornio', 'Aquario', 'Peixes']
    d = datetime.utcnow()
    t = list(d.timetuple()[:5])
    t[3] += t[4]/60.0
    t = t[:4]
    j = swe.julday(*t)
    result = {}
    result['date'] = d
    planets = []
    for i in range(10):
        a = swe.calc_ut(j,i)[0]
        s = signs[int(a/30)]
        
        d = {}
        d['index'] = i
        d['name'] = planet_names[i]
        d['angle'] = a
        d['sign'] = s
        planets.append(d)
    result['planets'] = planets
    return jsonify(result=result)




@app.route("/")
def index():
    #subprocess.call(['python', 'astro/make_svg_chart.py'])
    chart = get_chart()
    return render_template('chart.html', chart=chart)
