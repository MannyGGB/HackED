from __main__ import app
from flask import Flask,render_template,url_for,session,request,redirect,flash
from db_connector import database
import hashlib
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            flash("You must be logged in to view this page","warning")
            return redirect(url_for('login'))
        elif not session.get('admin'):
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