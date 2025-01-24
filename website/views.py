from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import  Fahrtenbuch, Ausgaben
from . import db
from datetime import datetime
import json, requests

views = Blueprint('views', __name__)

# Öffnen der Konfigurationsdatei in der die Keys gespeichert werden, um diese zu Schützen

with open('config.json', 'r') as f:
    config = json.load(f)


api_key_geo = config['api_key_geo']

api_key_tank = config['api_key_tank']


@views.route('/')
def home():
    return render_template("home/home.html", user=current_user)


@views.route('/fahrtenbuch', methods=['GET', 'POST'])
@login_required
def fahrtenbuch_view():
    if request.method == 'POST':
        start = request.form.get('street_start_form')
        start_hnr = request.form.get('street_start_hnr_form')
        start_plz = request.form.get('street_start_plz_form')
        start_ort = request.form.get('street_start_ort_form')
        start_km = int(request.form.get('street_start_km_form'))

        end = request.form.get('street_end_form')
        end_hnr = request.form.get('street_end_hnr_form')
        end_plz = request.form.get('street_end_plz_form')
        end_ort = request.form.get('street_end_ort_form')
        end_km = int(request.form.get('street_end_km_form'))

        route_diff = end_km - start_km

        new_route = Fahrtenbuch(street_start= start, street_start_hnr = start_hnr, street_plz_start = start_plz, street_start_ort = start_ort, street_end= end, street_end_hnr = end_hnr, street_plz_end = end_plz, street_end_ort = end_ort,  km_start=start_km, km_end=end_km, km_diff = route_diff,  user_id=current_user.id)
        db.session.add(new_route)
        db.session.commit()

        flash('Fahrt erfolgreich hinzugefügt', category='success')
        return redirect(url_for('views.fahrtenbuch_view'))


    # Schritt 2 hinzufügen
    fahrten = Fahrtenbuch.query.filter_by(user_id=current_user.id).all()

    # Schritt 3 hinzufügen
    return render_template("fahrzeug/fahrtenbuch.html", user=current_user, fahrten=fahrten)

@views.route('/ausgaben', methods=['GET', 'POST'])
@login_required
def ausgaben_view():
    if request.method == 'POST':
        ausgabe_desc = request.form.get('ausgabe_form_title')
        ausgabe_price =request.form.get('ausgabe_form_value')
        ausgabe_type = request.form.get('ausgabe_form_type')
        ausgabe_date = request.form.get('ausgabe_form_date')

        ausgaben_date = datetime.strptime(ausgabe_date, '%Y-%m-%d').date()

        new_ausgabe = Ausgaben(aus_title = ausgabe_desc, aus_value = ausgabe_price, aus_type = ausgabe_type, aus_date = ausgaben_date, user_id=current_user.id)
        db.session.add(new_ausgabe)
        db.session.commit()
        flash('Ausgabe erfolgreich hinzugefügt', category='success')
        return redirect(url_for('views.ausgaben_view'))
        
    
    ausgaben = Ausgaben.query.filter_by(user_id=current_user.id).all()

    # Summe aller Ausgaben berechnen
    summe = sum([a.aus_value for a in ausgaben])

    return render_template("fahrzeug/ausgaben.html", user=current_user, ausgaben=ausgaben, summe=summe)



@views.route('/delete-ausgabe', methods=['POST'])
def delete_ausgabe():
    ausgabe = json.loads(request.data)
    ausgabeId = ausgabe['ausgabeId']
    ausgabe = Ausgaben.query.get(ausgabeId)
    if ausgabe:
        if ausgabe.user_id == current_user.id:
            db.session.delete(ausgabe)
            db.session.commit()

    return jsonify({})

@views.route('/delete-fahrt', methods=['POST'])
def delete_fahrt():
    fahrt = json.loads(request.data)
    fahrtId = fahrt['fahrtId']
    fahrt = Fahrtenbuch.query.get(fahrtId)
    if fahrt:
        if fahrt.user_id == current_user.id:
            db.session.delete(fahrt)
            db.session.commit()

    return jsonify({})

@views.route("/tank", methods=["POST"])
@login_required
def tank():

    city = request.form.get("city_tank")


    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key_geo}"

    response_geo = requests.get(geo_url)
    geo_data = response_geo.json()

    if geo_data:
        latitude = geo_data[0]["lat"]
        longitude = geo_data[0]["lon"]
    else:
        return render_template("error-handling/404.html", user=current_user)

    rad = request.form.get("tank_rad")
    sort = request.form.get("tank_type")
    dist = request.form.get("tank_sort")

    tank_url = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={latitude}&lng={longitude}&rad={rad}&sort={dist}&type={sort}&apikey={api_key_tank}"

    response_tank = requests.get(tank_url)
    tank_data = response_tank.json()

    stations = tank_data['stations']

    tank_result_length = len(tank_data)

    if sort == 'diesel':
        sort_display = 'Diesel'
    elif sort == 'e5':
        sort_display = 'Super'
    elif sort == 'e10':
        sort_display = 'Super E10'



    return render_template("tank-pages/tank.html", tank_data=tank_data, city = city, tank_result_length=tank_result_length, stations=stations, sort_display =sort_display, user=current_user)

@views.route("/tank_submit")
@login_required
def tank_submit():
    return render_template('tank-pages/tank_submit.html', user=current_user)

@views.route("/error")
def page_error():
    return render_template("error-handling/404.html", user=current_user)
