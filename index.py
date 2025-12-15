import base64
import requests
from dotenv import load_dotenv
import os
import json


load_dotenv('.env')
CLIENT_ID= os.getenv('CLIENT_ID')
CLIENT_SECRET= os.getenv('CLIENT_SECRET')

# CREATING A TOKEN FOR SPOTIFY
def access_token():
    try:
        credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        response=requests.post(
            'https://accounts.spotify.com/api/token',
            headers={"Authorization":f'Basic {encoded_credentials}'},
            data={'grant_type':'client_credentials'})
        # print(response.json())
        # print(response.json()['access_token'])

        # print('Token generated Successfully')
        return response.json()['access_token']
    except Exception as e:
        print('Error in token generation',e)

# print(access_token())

# combine client id and client_secret  ----> credentials
#  #Converts the credentials string into bse63 format,This is required for HTTP Basic Authentication  -----encoded credentials
# URL is This is Spotify's token endpoint - the URL where you request access tokens
# Headers are ised for Tells Spotify who you are, Basic indicates we're using Basic Authentication
# Data : Tells Spotify which OAuth flow you're using, client_credentials means : "I'm an app requesing access to public data" (not user-specific data)


# Latest release in spotify
def get_new_release():
    try:
        token = access_token()
        header = {'Authorization':f'Bearer {token}'}
        Param = {'limit':50}
        response = requests.get('https://api.spotify.com/v1/browse/new-releases',
                      headers=header,params=Param)
        # print(response)
        if response.status_code==200:
            # print(response.json())
            data = response.json()
            albums = data['albums']['items']
            for album in albums:
                info = {
                    'album_name':album['name'],
                    'artist_name' : album['artists'][0]['name'],
                    'release_date' : album['release_date'],
                    'album_type' : album['album_type'],
                    'total_tracks' : album['total_tracks'],
                    'spotify_url' : album['external_urls']['spotify'],
                    'album_image': album['images'][0]['url'] if album['images'] else None
                }
                print(json.dumps(info, indent=2))
    except Exception as e:
        print('Error in latest release data fetching',e)
#
get_new_release()