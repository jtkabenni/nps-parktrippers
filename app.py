from flask import Flask, render_template, redirect, jsonify, request, session, flash, g
from dotenv import load_dotenv
import json
import os
import requests
from datetime import datetime
from models import User, Visit, Activity, Park, db, connect_db
from forms import UserAddEditForm, LoginForm
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"
NPS_BASE_URL = "https://developer.nps.gov/api/v1"

app = Flask(__name__)
load_dotenv()
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

@app.before_request
def add_image_to_session():
    if 'background_img' not in session:
        try:
            response = requests.get(f'https://api.unsplash.com/photos/random?client_id={os.getenv("UNSPLASH_API_KEY")}&collections=2471561&orientation=landscape')
            if response.status_code == 200:
                data = response.json()
                session['background_img'] = data['urls']['raw']
       
        except requests.exceptions.RequestException as err:
            print(err)
            return 'Error fetching background image.'



@app.route('/fetch-parks')
def fetch_parks():
    try:
        response = requests.get(f'{NPS_BASE_URL}/parks?api_key={os.getenv("NPS_API_KEY")}&limit=500')
        if response.status_code == 200:
            data = response.json()
            print(f"<<<<<<<<<<<<<<<<<<<<<<<<<{data}")
            return data
    except requests.exceptions.RequestException as err:
        print(err)

@app.route('/fetch-updated-park')
def fetch_updated_park():
    park_id = request.args.get("parkId")
    print(f"<<<<<<<<<<<<<<<<<<<<<<<<<{park_id}")
    try:
        response = requests.get(f'{NPS_BASE_URL}/parks?api_key={os.getenv("NPS_API_KEY")}&parkCode={park_id}')
        if response.status_code == 200:
            data = response.json()
            print(f"<<<<<<<<<<<<<<<<<<<<<<<<<{data}")
            return data
    except requests.exceptions.RequestException as err:
        print(err)

@app.route('/fetch-park-activities')
def fetch_park_activities():
    endpoint = request.args.get("endpoint")
    park_id = request.args.get("parkId")
    print(f"<<<<<<<<<<<<<<<<<<<<<<<<<{endpoint, park_id}")
    try:
        response = requests.get(f'{NPS_BASE_URL}/{endpoint}?api_key={os.getenv("NPS_API_KEY")}&limit=500&parkCode={park_id}')
        if response.status_code == 200:
            data = response.json()

            return data
    except requests.exceptions.RequestException as err:
        print(err)


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.username

def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = UserAddEditForm()
    if form.validate_on_submit():
        try:
            user = User.register(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data  
            )        
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/sign-up.html', form=form)
        do_login(user)
        return redirect("/")
    else:
        return render_template('users/sign-up.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        flash("Invalid credentials.", 'danger')
    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/')
def home():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return render_template('unauth-home.html')
    return render_template('home.html')


@app.route('/<username>')
def users_show(username):
    """Show user profile."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(username)
    visits = (Visit.query.filter(Visit.username == user.username).order_by(Visit.start_date).all())
    for visit in visits:
        visit.start_date = visit.start_date.strftime("%A %B %d, %Y")
        visit.end_date = visit.end_date.strftime("%A %B %d, %Y")
    return render_template('users/profile.html', user=user, visits=visits)


@app.route('/add-visit')
def display_add_visit_form():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    return render_template('users/add-visit.html')


@app.route('/add-visit', methods=['POST']  )
def add_visit():
    """Add visit and activities"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    park = request.json["park"]
    # query park with that park_code, if it exists, do nothing, if not, save new park with code and name
    doesPark = Park.query.filter(Park.park_code == park["park_code"]).first()
    if not doesPark:
      newPark = Park(park_code=park["park_code"], park_name=park["park_name"])
      db.session.add(newPark)
      db.session.commit()
    visit = request.json["visit"]
    activities = request.json["activities"]
    newVisit = Visit(start_date=visit['start_date'],end_date=visit['end_date'], park_code=visit['park_code'],username = g.user.username)
    db.session.add(newVisit)
    db.session.commit()
    for activity in activities:
      newActivity = Activity(name=activity["name"], description=activity["description"], activity_type=activity["activity_type"], duration=activity["duration"], location=activity["location"], visit_id=newVisit.id)
      db.session.add(newActivity)
      db.session.commit()
    return redirect(f'/{g.user.username}')

@app.route('/<username>/visits/<int:visit_id>' )
def show_visit_page(username,visit_id):
    """Display visit detail page"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    visit = Visit.query.get_or_404(visit_id)
    visit.start_date = visit.start_date.strftime("%A %B %d, %Y")
    visit.end_date = visit.end_date.strftime("%A %B %d, %Y")
    return render_template('visit.html', visit=visit)

@app.route('/<username>/visits/<int:visit_id>/save-activity-note', methods=['POST'])
def save_activity_note(username,visit_id):
    """Save activity note"""
    note = request.form.get('note')
    activity_id = request.form.get('activity-id')
    activity = Activity.query.get_or_404(activity_id)
    activity.notes = note
    db.session.commit()
    return redirect (f"/{username}/visits/{visit_id}")

@app.route('/<username>/visits/<int:visit_id>/delete-visit', methods=['POST'])
def delete_visit(username,visit_id):
    """Delete visit"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    visit = Visit.query.filter_by(id=visit_id).first()
    db.session.delete(visit)
    db.session.commit()
    return redirect (f'/{username}')


@app.route('/<username>/visits/<int:visit_id>/activities/<int:activity_id>/delete-activity', methods=['POST'])
def delete_activity(username, visit_id, activity_id):
    """Delete activity"""
    activity = Activity.query.filter_by(id=activity_id).first()
    db.session.delete(activity)
    db.session.commit()
    return redirect (f'/{username}/visits/{visit_id}')


@app.route('/<username>/visits/<int:visit_id>/update-visit')
def display_update_visit(username,visit_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    visit = Visit.query.filter_by(id=visit_id).first()
    return render_template('users/update-visit.html', visit = visit)

@app.route('/<username>/visits/<int:visit_id>/update-visit', methods=['POST'])
def update_visit(username, visit_id):
    """Add visit and activities"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    visit = Visit.query.filter_by(id=visit_id).first()
    updatedVisit = request.json["visit"]
    visit.start_date = updatedVisit['start_date']
    visit.end_date = updatedVisit['end_date']
    db.session.commit()
    activities = request.json["activities"]
    for activity in activities:
      newActivity = Activity(name=activity["name"], description=activity["description"], activity_type=activity["activity_type"], duration=activity["duration"], location=activity["location"], visit_id=visit_id)
      db.session.add(newActivity)
      db.session.commit()
    return redirect(f'/{username}')

