from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "🚀 SpaceX Tunes is online and flying!"

def run():
    # Run the server on port 8080 (default for Render web services)
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
