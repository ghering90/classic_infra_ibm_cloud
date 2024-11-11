import SoftLayer.API
import SoftLayer.auth
import requests


def cliibm_auth(api_key):
    token_endpoint = "https://iam.cloud.ibm.com/identity/token"
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': "urn:ibm:params:oauth:grant-type:apikey",
        'apikey': api_key
    }
    object_response = requests.post(url=token_endpoint, headers=token_headers, data=data)
    # print(object_response.status_code)
    object_response = object_response.json()
    softlayer_token = object_response['access_token']


    auth = SoftLayer.auth.BearerAuthentication('', softlayer_token)
    return SoftLayer.API.IAMClient(auth = auth)