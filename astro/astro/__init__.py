from flask import Flask
import swisseph as swe
from datetime import datetime
app = Flask(__name__)


def blah():
    planets = ['Sol', 'Lua', 'Mercurio', 'Venus', 'Marte', 'Jupiter','Saturno', 'Urano', 'Netuno' ,'Plutao']
    signs = ['Aries', 'Touro', 'Gemeos', 'Cancer', 'Leao', 'Virgem', 'Libra', 'Escorpiao', 'Sagitario', 'Capricornio', 'Aquario', 'Peixes']
    d=datetime.utcnow()
    t=list(d.timetuple()[:5])
    t[3]+=t[4]/60.0
    t=t[:4]
    j = swe.julday(*t)
    txt=str(d)+"\n<br>\n<br\n<br\n<br\n"
    for i in range(10):
        a = swe.calc_ut(j,i)[0]
        s = signs[int(a/30)]
        txt += "%s %.4f %s\n<br>\n"%(planets[i], a%30,s)

    return txt


@app.route("/")
def hello():
    return blah()
    #return "Hello, I love Digital Ocean!"
if __name__ == "__main__":
    app.run()

