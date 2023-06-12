from dotenv import load_dotenv
import os
import requests

load_dotenv()
NPS_BASE_URL = "https://developer.nps.gov/api/v1"

def api_fetch_parks():
    try:
        response = requests.get(f'{NPS_BASE_URL}/parks?api_key={os.getenv("NPS_API_KEY")}&limit=500')
        if response.status_code == 200:
            data = response.json()
            return data
    except requests.exceptions.RequestException as err:
        print(err)
        return err

def api_fetch_updated_park(park_id):

    try:
        response = requests.get(f'{NPS_BASE_URL}/parks?api_key={os.getenv("NPS_API_KEY")}&parkCode={park_id}')
        if response.status_code == 200:
            data = response.json()
            return data
    except requests.exceptions.RequestException as err:
        print(err)
        return err

def api_fetch_park_activities(endpoint,park_id):
    try:
        response = requests.get(f'{NPS_BASE_URL}/{endpoint}?api_key={os.getenv("NPS_API_KEY")}&limit=500&parkCode={park_id}')
        if response.status_code == 200:
            data = response.json()
            return data
    except requests.exceptions.RequestException as err:
        print(err)
        return err