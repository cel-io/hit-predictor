import json
from flask import Blueprint, jsonify, request, abort
from requests import post, Request, Session
import base64
import os

spotify = Blueprint('spotify', __name__)

auth_token = None


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

    return jsonify({"features": features})
