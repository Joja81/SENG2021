import os
import config
from app import init_app, email
from flask import Flask
import signal

if 'ON_HEROKU' not in os.environ: # Checks if running on 
    import enviro

def graceful_exit(*args):
    email.exit()
    exit(0)

app = init_app()

if __name__ == "__main__":
    print(os.environ.get("ON_HEROKU"))
    
    signal.signal(signal.SIGINT, graceful_exit)
    app.run(port = config.port, debug = True)