from . import admin
from flask import render_template, redirect, url_for


@admin.route("/")
def admin():
    return render_template('admin/index.html')