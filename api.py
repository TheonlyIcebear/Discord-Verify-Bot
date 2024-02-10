import requests, os

API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = os.environ['client_id']
CLIENT_SECRET = os.environ['client_secret']
REDIRECT_URI = 'https://9af33324-4c5c-4a6b-b804-f0a21284bad6-00-fnny5x7l1njt.worf.replit.dev/access'

def exchange_code(code):
    data = {
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': REDIRECT_URI
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    return r.json()

def add_to_guild(access_token, userID, guildID):
    url = f"{API_ENDPOINT}/guilds/{guildID}/members/{userID}"
    botToken = os.environ['token']
    data = {
    "access_token" : access_token,
    }
    headers = {
    "Authorization" : f"Bot {botToken}",
    'Content-Type': 'application/json'
    }
    response = requests.put(url=url, headers=headers, json=data)
    print(response.text)
    response.raise_for_status()
    return response
    
def refresh_token(refresh_token):
    data = {
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    print(r, r.json())
    return r.json()

def get_info(access_token):
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Bearer '+access_token
    }

    r = requests.get('https://discordapp.com/api/users/@me', headers=headers)
    return r.json()