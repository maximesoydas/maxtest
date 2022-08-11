def test_load_clubs():
    with open('clubs.json', 'r') as jsonfile:
        return jsonfile.read()
    
print(test_load_clubs())    
