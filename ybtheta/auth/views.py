from flask import Blueprint, render_template, abort


blueprint = Blueprint('auth', 'ybtheta.auth', template_folder='templates')
