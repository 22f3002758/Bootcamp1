from flask import current_app as app, render_template, request, redirect
from backend.models import *


@app.route("/")
def home():
    return render_template("home.html")

