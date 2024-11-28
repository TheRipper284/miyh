from flask import Blueprint, redirect, render_template, session

principal = Blueprint('principal', __name__)

@principal.route('/index')
def index():
    if 'user_id' not in session:
        return redirect('/')  
    return render_template('index.html')