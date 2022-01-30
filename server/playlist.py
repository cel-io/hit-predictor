from collections import OrderedDict
from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors
from topsis import Topsis

playlist = Blueprint('playlist', __name__)

script_dir = os.path.dirname(__file__)

normalized_tracks = pd.read_csv(os.path.join(
    script_dir, './data/normalized_tracks.csv'))
tracks_info = pd.read_csv(os.path.join(
    script_dir, './data/track_artist_url.csv'))
track_targets = np.loadtxt(open(os.path.join(
    script_dir, "./data/y.csv")), delimiter=",", skiprows=1)


@playlist.route('/build', methods=['POST'])
def build_playlist():
    features = request.get_json()['features']
    criteria = request.get_json()['criteria']

    features_ordered = OrderedDict(
        {
            "danceability": [features['danceability']],
            "energy": [features['energy']],
            "key": [features['key']],
            "loudness": [features['loudness'] + 60],
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
        })

    feature_names = list(features_ordered.keys())
    selected_features = pd.DataFrame.from_dict(features_ordered)

    norm_selected_features = normalize(selected_features)

    print(norm_selected_features)

    neigh = NearestNeighbors(n_neighbors=5, radius=0.01)
    samples = normalized_tracks.to_numpy()
    neigh.fit(samples)

    index_neighbors = neigh.kneighbors(
        norm_selected_features, n_neighbors=100, return_distance=False)
    distance_neighbors = neigh.kneighbors(
        norm_selected_features, n_neighbors=100, return_distance=True)

    query_samples = samples[index_neighbors][0]
    main_feature_values = []
    main_feature_index = feature_names.index(criteria['mainFeature'])

    for row in query_samples:
        main_feature_values.append(row[main_feature_index])

    topsis_items = []
    i = 0

    for index in index_neighbors[0]:
        topsis_items.append([distance_neighbors[0][0][i],
                            track_targets[index], main_feature_values[i]])
        i += 1

    weights = [criteria['songSimilarityWeight'],
               criteria['hitOrNotWeight'], criteria['mainFeatureWeight']]

    '''
    if higher value is preferred - True
    if lower value is preferred - False
    '''
    criterias = np.array(
        [False, criteria['hit'], criteria['mainFeatureHigher']])

    t = Topsis(np.array(topsis_items), weights, criterias)
    t.calc()

    final_indexes = []

    for i in range(20):
        final_indexes.append(t.rank_to_best_similarity()[i])

    final_indexes = [index - 1 for index in final_indexes]

    best_tracks_indexes = []

    for i in final_indexes:
        best_tracks_indexes.append(index_neighbors[0][i])

    return jsonify({'playlist': tracks_info.iloc[best_tracks_indexes].to_dict(orient='records')})
