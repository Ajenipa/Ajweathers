from flask import Flask,request,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import psycopg2
app =  Flask(__name__)
ENV = 'dev'
weather_data = []
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:ajenipa1@localhost/ajwet'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI']=''
app.config['SECRET_KEY']='1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
class City(db.Model):
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(99), nullable=False)
    def __init__(self,name):
        self.name = name
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name_obj = request.form['city']
        new_city = City(name = name_obj)
        db.session.add(new_city)
        db.session.commit()
    #city = 'Abuja'
    cities = City.query.all()
    for city in cities:
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=ef6f17146d78fccc79afb5f7d50d454b"
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city':city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
            'coordinate':r['coord']
        }
        #print(r)
        weather_data.append(weather)
        #print(weather_data)
    return render_template('index1.html', weather_data = weather_data,city = city )
@app.route("/city/delete/<int:id>")
def delete(id):
    cities = City.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    return render_template('index1.html', weather_data = weather_data, city = city)

if __name__ == '__main__':
    app.run(debug = True)