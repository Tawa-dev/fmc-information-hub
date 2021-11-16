from app import app          
from app.database import Database      

from flask import render_template, request, url_for, redirect, session

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/corporate')
def corporate():
    return render_template('corporate.html')

@app.route('/uniform')
def uniform():
    return render_template('uniform.html')