from __main__ import app
from flask import Flask, render_template, url_for, session, request, redirect, flash, jsonify
from db_connector import database
import hashlib
from functools import wraps
import os
from dotenv import load_dotenv

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            flash("You do not have permission to view this page","danger")
        return f(*args, **kwargs)
    return decorated_function
    

db = database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    data = db.queryDB("SELECT Business.Name, Metrics.ovr FROM Metrics, Business WHERE Metrics.business_id = Business.business_id ORDER BY Metrics.ovr DESC")
    return render_template('leaderboardDisplay.html', data=data)

@app.route('/admin_login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["pass"]

        if "admin" in session:
            print("Already logged in")
            return redirect(url_for('admin'))
        
        found_user = db.queryDB("SELECT * FROM Admin WHERE user = ?", [user])

        if found_user:
            stored_password = found_user[0][2]
            if stored_password == password:
                session['admin'] = user
                print("Login Successful")
                return redirect(url_for("admin"))
            else:
                print("Incorrect Password")
        else:
            print("User Not Found")
        return render_template('adminLogin.html')
    
    
    return render_template('adminLogin.html')

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/find_stores', methods=['GET'])
def map_page():
    # Just return the file. No variables passed here.
    return render_template("mapDisplay.html")

@app.route('/api/stores', methods=['GET'])
def get_stores_api():
    load_dotenv()
    
    # 1. Get the API Key and Store Data
    key = os.getenv("MY_API_KEY")
    query = "SELECT Name, lat, long FROM Business"
    stores_raw = db.queryDB(query)

    stores_list = []
    for row in stores_raw:
        stores_list.append({
            "name": str(row[0]),
            "lat": float(row[2]),
            "lng": float(row[1])
        })

    # 2. Return everything as a JSON object
    return jsonify({"apiKey": key, "stores": stores_list})