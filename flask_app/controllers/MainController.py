from flask import render_template, redirect, session, flash
from flask_app import app



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard/')
def dashboard():
    pass
