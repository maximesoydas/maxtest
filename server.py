import json
from xml.dom import ValidationErr
from flask import Flask,render_template,request,redirect,flash,url_for
import datetime

from pathlib import Path
from flask_caching import Cache
# Instantiate the cache
cache = Cache()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["CACHE_TYPE"]= 'simple'
    app.secret_key = 'something_special'
    cache.init_app(app)
    
    date_time = datetime.datetime.now()
    date_time = date_time.strftime("%d/%m/%Y")

    @app.route('/')
    def index():
        cache.clear()
        return render_template('index.html')

    # called by the login form,
    # if request.form is valid we then render the welcome.html page with the data of our current club 
    # and list competitions
    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        cache.clear()
        cache.set("email", request.form['email'])
        email = request.form['email']
        try:
            # list all clubs, if the club requested in the form corresponds to our json file's clubs we add corresponding clubs to a list,
            # we then define our current club variable to the the first club in the list
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            return render_template('welcome.html',club=club,competitions=competitions,clubs=clubs)
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
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    # digest the booking.html form
    # deduct available places by the requested form number
    # deduct club's points by the requested form number
    @app.route('/purchasePlaces',methods=['POST','GET'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        # fix bug 
        if int(placesRequired) > int(club['points']):
            flash("You do not have enough club points")
        # fix bug clubs should not be able to use more than 12 places
        elif int(placesRequired) > 12:
            flash("You cannot request more than 12 places for a competition")
        elif int(competition['numberOfPlaces']) < 1:
            flash("This Competition has no more places")
        else:
            # fix bug point updates are not reflected
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points']) - int(placesRequired)
            club['points'] = str(club['points'])
        
            with open('clubs.json', "w") as clubjson:
                clubs_dict = json.dumps({"clubs":clubs}, indent=1)
                clubjson.write(clubs_dict)    
            competition['numberOfPlaces'] = str(competition['numberOfPlaces'])
            with open('competitions.json', "w") as competitionjson:
                competitions_dict = json.dumps({"competitions":competitions}, indent=1)
                competitionjson.write(competitions_dict)
                flash('Great-booking complete!')

        return render_template('welcome.html', club=club, competitions=competitions,clubs=clubs)



    # TODO: Add route for points display
    @app.route('/displayPoints',methods=['GET'])
    def displayPoints():
        print('TESTESTESTSETE')
        email = cache.get("email")
        print(email)
        try:
            club = [club for club in clubs if club['email'] == email][0]
            if club == None:
                return redirect(url_for('index'))
            return render_template('points.html', clubs=clubs, competitions=competitions)

        except IndexError:
            return redirect(url_for('index'))
            
        

    @app.route('/logout')
    def logout():
        cache.clear()
        return redirect(url_for('index'))
    
    @app.route('/showSummary')
    def homepage():
        email = cache.get("email")
        try:
            club = [club for club in clubs if club['email'] == email][0]
            if club == None:
                return redirect(url_for('index'))
            
            return render_template('welcome.html',club=club,competitions=competitions,clubs=clubs)
        except IndexError:
          return redirect(url_for('index'))
            
    return app


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

competitions = loadCompetitions()
clubs = loadClubs()

