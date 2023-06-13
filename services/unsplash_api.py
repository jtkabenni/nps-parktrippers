from dotenv import load_dotenv
import os
import requests

load_dotenv()

DEFAULT_IMG = "https://images.unsplash.com/photo-1483737849322-38a4b98bb9aa?ixid=M3w0NDk5ODF8MHwxfHJhbmRvbXx8fHx8fHx8fDE2ODY2MDY3NDN8&ixlib=rb-4.0.3"


def api_get_image():
        try:
            response = requests.get(f'https://api.unsplash.com/photos/random?client_id={os.getenv("UNSPLASH_API_KEY")}&collections=2471561&orientation=landscape')
            if response.status_code == 200:
                data = response.json()
                return data['urls']['raw']
    
        except requests.exceptions.RequestException as err:
            print(err)
            return DEFAULT_IMG
