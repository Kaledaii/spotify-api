from dotenv import load_dotenv
import os,json
import base64
from requests import get, post
load_dotenv()

client_id=os.getenv('CLIENT_ID')
client_secret=os.getenv('CLIENT_SECRET')


def get_token():
    url='https://accounts.spotify.com/api/token'
    auth_str=f"{client_id}:{client_secret}"
    auth_bytes=auth_str.encode('utf-8')
    auth_b64=base64.b64encode(auth_bytes).decode('utf-8')

    headers={
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data={
        'grant_type': 'client_credentials'
    }
    result=post(url,headers=headers,data=data)
    json_result=json.loads(result.content)
    token=json_result['access_token']
    return token

token=get_token()

def authorization_header(token):
    return {'Authorization': f'Bearer {token}'}
def search_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = authorization_header(token)
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }
    response = get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error fetching artist:", response.text)
        return

    data = response.json()
     
    if data['artists']['items']:
        artist = data['artists']['items'][0]
        artist_id= data['artists']['items'][0]['id']
        name = artist['name']
        followers = artist['followers']['total']
        popularity = artist['popularity']
        print(f"Name: {name}\nFollowers: {followers}\nPopularity: {popularity}")
        return artist_id
    else:
        print("No artist found.")

def get_artist_top_tracks(token, artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers=authorization_header(token)
    response=get(url,headers=headers)
    if response.status_code != 200:
        print("Error fetching top tracks:", response.text)
        return
    data=response.json()
    tracks = data['tracks']

    for idx, track in enumerate(tracks[:10], start=1):
        name = track['name']
        popularity = track['popularity']
        link = track['external_urls']['spotify']
        print(f"{idx}. {name} (Popularity: {popularity})\n   {link}")


id=search_artist(token,'Adele')
get_artist_top_tracks(token,id)
