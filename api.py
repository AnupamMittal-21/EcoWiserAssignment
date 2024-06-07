import requests
from dotenv import load_dotenv
import os


def run_api(PROXYCURL_API_KEY, link):
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    header_dic = {'Authorization': 'Bearer ' + PROXYCURL_API_KEY}
    params = {
        'url': link,
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=header_dic)
    return response.json()
