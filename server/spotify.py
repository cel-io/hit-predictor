from flask import Blueprint, jsonify, request, abort
from requests import post, Request, Session
import base64
import os
import pickle
import pandas as pd
from itertools import combinations

spotify = Blueprint('spotify', __name__)

auth_token = None

script_dir = os.path.dirname(__file__)

predict_model = pickle.load(
    open(os.path.join(script_dir, "./models/finalized_model.sav"), "rb"))
polynomial_features_model = pickle.load(
    open(os.path.join(script_dir, "./models/poly_features.sav"), "rb"))

SELECTED_COLS = ['danceability', 'loudness', 'instrumentalness', 'danceability_energy', 'danceability_instrumentalness', 'danceability_tempo', 'danceability_time_signature', 'energy_instrumentalness', 'key_instrumentalness', 'loudness_acousticness', 'loudness_instrumentalness',
                 'mode_instrumentalness', 'speechiness_instrumentalness', 'instrumentalness_liveness', 'instrumentalness_valence', 'instrumentalness_tempo', 'instrumentalness_duration_ms', 'instrumentalness_time_signature', 'instrumentalness_chorus_hit', 'instrumentalness_sections']


def predict_hit(features):
    features_to_transform = {
        "danceability": [features['danceability']],
        "energy": [features['energy']],
        "key": [features['key']],
        "loudness": [features['loudness']],
        "mode": [features['mode']],
        "speechiness": [features['speechiness']],
        "acousticness": [features['acousticness']],
        "instrumentalness": [features['instrumentalness']],
        "liveness": [features['liveness']],
        "valence": [features['valence']],
        "tempo": [features['tempo']],
        "duration_ms": [features['duration_ms']],
        "time_signature": [features['time_signature']],
        "chorus_hit": [features['chorus_hit']],
        "sections": [features['sections']],
    }

    df = pd.DataFrame.from_dict(features_to_transform)

    combos = list(combinations(list(df.columns), 2))
    colnames = list(df.columns) + ['_'.join(x) for x in combos]

    print(colnames)

    global polynomial_features_model
    df = polynomial_features_model.transform(df)
    df = pd.DataFrame(df)
    df.columns = colnames

    global SELECTED_COLS

    return True if predict_model.predict(df[SELECTED_COLS]) == 1 else False


def auth_spotify():
    global auth_token

    if auth_token == None:
        auth_credentials = base64.b64encode(
            (os.environ["SPOTIFY_CLIENT_ID"] + ":" + os.environ["SPOTIFY_CLIENT_SECRET"]).encode("ascii")).decode("ascii")

        response = post("https://accounts.spotify.com/api/token", headers={
            "Authorization": "Basic " + auth_credentials, }, data={"grant_type": "client_credentials"})

        auth_token = response.json()


def make_spotify_request(req):
    global auth_token

    response = None

    attempts = 0
    success = False

    s = Session()
    prepped = req.prepare()

    while attempts < 2 and success == False:
        auth_spotify()

        prepped.headers["Authorization"] = "Bearer " + \
            auth_token["access_token"]

        response = s.send(prepped)

        if (response.status_code == 401):
            auth_token = None
            attempts += 1
        else:
            success = True

    return response


@spotify.route('/search', methods=['GET'])
def search():

    query = request.args.get("q")
    query += " year:2020-2022"

    response = make_spotify_request(Request('GET', 'https://api.spotify.com/v1/search',
                                            params={"type": "track", "q": query}))

    return response.json()


@spotify.route('<track_id>/hit-prediction', methods=['GET'])
def hit_prediction(track_id):
    features = {
        "danceability": 0,
        "energy": 0,
        "key": -1,
        "loudness": 0,
        "mode": 0,
        "speechiness": 0,
        "acousticness": 0,
        "instrumentalness": 0,
        "liveness": 0,
        "valence": 0,
        "tempo": 0,
        "duration_ms": 0,
        "time_signature": 0,
        "chorus_hit": 0,  # Analysis
        "sections": 0,  # Analysis
    }

    track_id = str(track_id)

    responseFeatures = make_spotify_request(
        Request('GET', 'https://api.spotify.com/v1/audio-features/' + track_id))

    if responseFeatures.status_code != 200:
        abort(400)

    responseFeaturesJSON = responseFeatures.json()

    for key in responseFeaturesJSON:
        if key in features.keys():
            features[key] = responseFeaturesJSON[key]

    responseAnalysis = make_spotify_request(
        Request('GET', 'https://api.spotify.com/v1/audio-analysis/' + track_id))

    if responseAnalysis.status_code != 200:
        abort(400)

    responseAnalysisJSON = responseAnalysis.json()
    num_sections = len(responseAnalysisJSON["sections"])

    features["sections"] = num_sections

    if num_sections == 0:
        features["chorus_hit"] = 0
    else:
        features["chorus_hit"] = responseAnalysisJSON["sections"][2]["start"] if num_sections >= 3 else responseAnalysisJSON["sections"][num_sections - 1]["start"]

    hit = predict_hit(features)

    return jsonify({"features": features, "hit": hit})


@spotify.route('hit-prediction/manual', methods=['POST'])
def hit_prediction_manual():
    hit = predict_hit(request.get_json())

    return jsonify({"hit": hit})
