from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv

from spotify import spotify
from playlist import playlist


# configuration
DEBUG = True
load_dotenv()

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(spotify, url_prefix='/spotify')
app.register_blueprint(playlist, url_prefix='/playlist')

if __name__ == '__main__':
    app.run()
