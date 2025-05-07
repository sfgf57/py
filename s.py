from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def proxy():
    url = 'https://www.callbomberz.in'
    r = requests.get(url)
    return Response(r.content, content_type=r.headers['Content-Type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
