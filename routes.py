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

@app.route('/', methods=['GET'])
def home():
    # Count of businesses
    count_data = db.queryDB("SELECT COUNT(*) FROM Business")
    count = count_data[0][0] if count_data else 0

    # Helper to get the top business for a specific column
    def get_top_biz(column):
        query = f"""
            SELECT b.Name, m.{column} 
            FROM Metrics m 
            JOIN Business b ON m.business_id = b.business_id 
            ORDER BY m.{column} DESC LIMIT 1
        """
        result = db.queryDB(query)
        return result[0] if result else ("N/A", 0)

    # Fetching winners for each category
    winners = {
        "overall": get_top_biz("ovr"),
        "carbon": get_top_biz("carbon_intensity"),
        "materials": get_top_biz("sustainable_materials"),
        "supply_chain": get_top_biz("supply_chain"),
        "waste": get_top_biz("waste"),
        "water": get_top_biz("water_use")
    }

    return render_template('index.html', count=count, winners=winners)

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    # calculate average
    db.updateDB("""
        UPDATE Metrics 
        SET ovr = ROUND((carbon_intensity + sustainable_materials + supply_chain + waste + water_use) / 5.0, 1)
    """)

    data = db.queryDB("""
        SELECT Business.Name, Metrics.ovr
        FROM Metrics
        JOIN Business ON Metrics.business_id = Business.business_id
        ORDER BY Metrics.ovr DESC
    """)
    
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

@app.route('/logout')
@admin_required
def logout():
    session.pop('admin')
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/admin_add_company', methods=['GET', 'POST'])
@admin_required
def admin_add_company():
    if request.method == "POST":
        name = request.form["name"]
        physical = request.form.get("phys")
        long = request.form["long"]
        lat = request.form["lat"]

        tick = 1 if physical else 0

        if name and long and lat:
            db.updateDB('INSERT INTO Business (Name,is_physical,long,lat) VALUES (?,?,?,?)', (name,tick,long,lat))

    return render_template('admin.html')

@app.route('/find_stores', methods=['GET'])
def find_stores():
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

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    # Fetch all businesses for the dropdown menus
    businesses = db.queryDB("SELECT business_id, Name FROM Business")
    
    biz1_data = None
    biz2_data = None
    id1 = None
    id2 = None

    if request.method == 'POST':
        id1 = request.form.get('biz1')
        id2 = request.form.get('biz2')

        if id1 and id2:
            # Fetch latest metrics for the selected businesses
            query = "SELECT * FROM Metrics WHERE business_id = ? ORDER BY date DESC LIMIT 1"
            res1 = db.queryDB(query, [id1])
            res2 = db.queryDB(query, [id2])
            
            if res1 and res2:
                biz1_data = res1[0]
                biz2_data = res2[0]
            
            # Convert IDs to integers so they match the database values in the template check
            id1 = int(id1)
            id2 = int(id2)

    return render_template('compare.html', businesses=businesses, b1=biz1_data, b2=biz2_data, id1=id1, id2=id2)