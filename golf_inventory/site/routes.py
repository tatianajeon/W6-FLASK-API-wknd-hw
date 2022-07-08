# Original
from flask import Blueprint, render_template
from golf_inventory.models import GolfClub, golf_schema
site = Blueprint('site', __name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    try: 
        clubs = GolfClub.query.all()
        return render_template('profile.html', clubs = clubs)
        
    except Exception as error:
        error_text = '<p>The error: <br>' + str(error) + '</p>'
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

