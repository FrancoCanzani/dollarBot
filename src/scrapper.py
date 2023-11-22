import requests


class Scrapper:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get_data(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
