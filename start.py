import os
import config
from app import init_app
from flask import Flask
import signal

# Import environ if not on server where enviorment variables already saved
if "ON_SERVER" not in os.environ:     
    import enviro # pylint: disable=import-error

from app.functions import emailSystem

def graceful_exit(*args):
    emailSystem.exit()
    exit(0)

app = init_app()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, graceful_exit)
    app.run(port = config.port, debug = True)