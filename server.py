from api import exchange_code, get_info
from flask import Flask, request, redirect
import threading, asyncio, json, os

app = Flask(__name__)
bot_link = 'https://discord.com/channels/@me'
auth_link = os.environ['oauth_link']

class Server:
    def __init__(self):
      pass
      
    @app.route('/access')
    def main():
        print(request.args)
        try:
            code = exchange_code(request.args['code'])
        except Exception as e:
            print(e)
            return redirect(bot_link, code=302)

        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']

        ip = ip.split(',')[0]
          
        print(ip)
        jsonfile = json.load(open("auths.json", "r+"))

        try:
            jsonfile[id] = [code['access_token'], code['refresh_token'], ip]
            with open("auths.json", "w+") as file:
                json.dump(jsonfile, file, indent=2)
        except Exception as e:
            print(e)
            pass
        
      

        return redirect(bot_link, code=302)

    @app.errorhandler(404)
    def not_found(e):
        return redirect(auth_link, code=302)
def run():
    app.run(host='0.0.0.0', port=80)