from locust import HttpUser, task


class TestAPI(HttpUser):

    @task
    def index_page(self):
        self.client.get('/')

    @task
    def generate_post(self):
        self.client.post('/generate')

    @task
    def retrieve_get(self):
        self.client.get('/retrieve/1')
