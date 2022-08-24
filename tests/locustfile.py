from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    @task(10)
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        data = {'email': 'john@simplylift.co'}
        url = '/showSummary'
        self.client.post(url, data)
        
    @task
    def purchase_places_1(self):
        data = {'club': 'Simply Lift', 'competition': 'Winter Fitness','places':2}
        url = '/purchasePlaces'
        self.client.post(url, data)
        
    @task
    def access_display_points_url(self):
        data = {'email': 'john@simplylift.co'}
        url = '/displayPoints'
        self.client.post(url,data)