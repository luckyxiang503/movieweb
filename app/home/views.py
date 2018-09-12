from . import home
from flask import render_template, redirect, url_for


@home.route('/login/')
def login():
    return render_template('home/login.html')


@home.route('/logout/')
def logout():
    return redirect(url_for('home.login'))


@home.route("/")
def home():
    return render_template('home/index.html')
