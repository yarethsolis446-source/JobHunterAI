import requests


class HttpClient:

    def __init__(self, timeout=15):

        self.timeout = timeout

        self.headers = {

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            ),

            "Accept": "application/json"

        }

    def get(self, url, params=None):

        try:

            response = requests.get(

                url,

                params=params,

                headers=self.headers,

                timeout=self.timeout

            )

            response.raise_for_status()

            return response

        except requests.exceptions.RequestException as e:

            print(f"HTTP GET ERROR: {e}")

            return None

    def get_json(self, url, params=None):

        response = self.get(url, params)

        if response is None:

            return None

        try:

            return response.json()

        except Exception:

            print("La respuesta no es JSON.")

            return None

    def get_text(self, url, params=None):

        response = self.get(url, params)

        if response is None:

            return None

        return response.text