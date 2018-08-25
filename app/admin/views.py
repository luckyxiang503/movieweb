from . import admin

@admin.route("/")
def admin():
    return "welcome to admin"