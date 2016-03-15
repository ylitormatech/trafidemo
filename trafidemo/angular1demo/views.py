"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user


blueprint = Blueprint('trafiangular', __name__, static_folder='../static')

@blueprint.route('/trafiangular/')
def trafiangular():
    """View Trafidata with Angular 1"""
    return render_template("angular1demo/index.html")