import json
from flask import Flask,render_template,request,redirect,flash,url_for,session


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

# called by the login form,
# if request.form is valid we then render the welcome.html page with the data of our current club 
# and list competitions
@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form['email']
    try:
        # list all clubs, if the club requested in the form corresponds to our json file's clubs we add corresponding clubs to a list,
        # we then define our current club variable to the the first club in the list
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        # session['club'] = club
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        return f"<h3 style='color:red;'> {email} is not a valid email (does not belong to any registered clubs)</h3><a href='/'>return</a>"
        

# called by the "book places" button on the welcome.html page. 
# loads the booking.html page of selected competition
# contains a form that calls the purchasePlaces function
@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    # foundClub = 'd'
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club='k',competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


# digest the booking.html form
# deduct available places by the requested form number
# 
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    
    
    placesRequired = int(request.form['places'])
    
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))