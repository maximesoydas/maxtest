import json
from pprint import pprint as p
from conftest import client
from flask import url_for, request


def test_should_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200
    
def test_login_ok(client):
    # we are trying to check if the response we get from login with a correct email is ok  
    data = {'email': 'john@simplylift.co'}
    url = '/showSummary'

    # here we need to use the client.post() function to be able to pass data to our url
    response = client.post(url,data=data)
    # to see prints in pytest simply cmd --> py.test -s
    # response.data contains the response of our post method
    # print(response.data)
    assert response.status_code == 200
    # check that the email is not invalid
    assert 'not a valid email' not in str(response.data)
    
def test_login_ko(client):
    # we are trying to check if the response we get from login with an incorrect email is ok  
    data = {'email': 'fakemail@fake.co'}
    url = '/showSummary'

    response = client.post(url,data=data)

    assert response.status_code == 200
    # check that the email is not valid
    assert 'not a valid email' in str(response.data)
    
def test_purchase_places_ok(client):
    data = {'club': 'Iron Temple', 'competition': 'Winter Fitness','places':2}
    url = '/purchasePlaces'
    response = client.post(url, data=data)
    # print(response.data.decode())
    assert "Great-booking complete!" in str(response.data)
    assert response.status_code == 200
    
def test_purchase_places_ok_db_sync(client):
    data = {'club': 'Simply Lift', 'competition': 'Winter Fitness','places':2}
    with open('clubs.json',"r") as clubjson:
        cl = json.load(clubjson)
        club = [c for c in cl['clubs'] if c['name'] == data['club']][0]
        before_request_club_points = club['points']
        
    with open('competitions.json', "r") as competitionjson:
        cp1 = json.load(competitionjson)
        competition = [cp for cp in cp1['competitions'] if cp['name'] == data['competition']][0]
        before_request_competition_places = competition['numberOfPlaces']
        
    url = '/purchasePlaces'
    response = client.post(url, data=data)
    
    with open('clubs.json', "r") as clubjson:
        cl = json.load(clubjson)
        club = [c for c in cl['clubs'] if c['name'] == data['club']][0]
        after_request_club_points = club['points']

    with open('competitions.json', "r") as competitionjson:
        cp1 = json.load(competitionjson)
        competition = [cp for cp in cp1['competitions'] if cp['name'] == data['competition']][0]
        after_request_competition_places = competition['numberOfPlaces']
    
    # check that the requested amount of places has been removed from the competition's available places in the db
    assert int(after_request_club_points) == int(before_request_club_points) - data['places']
    assert int(after_request_competition_places) == int(before_request_competition_places) - data['places']
    assert "Great-booking complete!" in str(response.data)
    assert response.status_code == 200
    
def test_purchase_places_expired(client):
    data = {'club': 'Simply Lift', 'competition': 'Spring Festival','places':2}
    url = '/purchasePlaces'
    response = client.post(url, data=data)
    assert "This Competition has expired" in str(response.data)
    assert response.status_code == 200
    
def test_purchase_places_zero_points(client):
    data = {'club': 'NO POINTS NO GAIN', 'competition': 'Spring Festival','places':2}
    url = '/purchasePlaces'
    response = client.post(url, data=data)
    assert "You do not have enough club points" in str(response.data)
    assert response.status_code == 200

def test_purchase_places_no_places(client):
    data = {'club': 'She Lifts', 'competition': 'Summer Madness','places':2}
    url = '/purchasePlaces'
    response = client.post(url, data=data)
    assert "This Competition has no more places" in str(response.data)
    assert response.status_code == 200
    
def test_display_points_ok(client): 
    data = {'email': 'john@simplylift.co'}
    url = '/displayPoints'
    response = client.post(url,data=data)
    # print(response.data.decode())
    with open('clubs.json',"r") as clubjson:
        cl = json.load(clubjson)
        for c in cl['clubs']:
            # print(c['name'])
            assert str(c['name']) in str(response.data)
    assert response.status_code == 200
    
def test_display_points_ko_redirect_index(client):
    # check redirection to index if email is wrong/ not in db 
    data = {'email': 'fakemail@fake.co'}
    url = '/displayPoints'
    
    response = client.post(url,data=data,follow_redirects=True)
    # confirm redirection to login form (index) if email is not valid
    assert 'Please enter your secretary email to continue:' in str(response.data) 
    assert response.status_code == 200