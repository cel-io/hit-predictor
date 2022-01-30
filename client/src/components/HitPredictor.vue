<template>
  <div class="container">
    <section class="hero is-success mb-4">
      <div class="hero-body">
        <p class="title">
          &#127925; Spotify Hit Predictor and Playlist Builder
        </p>
        <p class="subtitle">
          Determine if a song is an hit based on its
          <a
            class="has-text-info"
            href="https://developer.spotify.com/discover/"
            target="_blank"
            >Spotify features</a
          >
          using AI and build playlists around it.
        </p>
      </div>
    </section>
    <section class="mb-5">
      <h1 class="title">Hit Predict</h1>
      <div class="columns">
        <div class="column is-flex is-align-items-center">
          <b-button
            icon-left="spotify"
            size="is-large"
            :focused="manualInsert != null && !manualInsert"
            expanded
            outlined
            @click="chooseInsertMethod('spotify')"
            >Choose a Song on Spotify</b-button
          >
        </div>
        <div class="column is-1 has-text-centered">
          <span class="is-size-2">OR</span>
        </div>
        <div class="column is-flex is-align-items-center">
          <b-button
            size="is-large"
            :focused="manualInsert != null && manualInsert"
            expanded
            outlined
            @click="chooseInsertMethod('manual')"
            >Enter Feature Values Manually</b-button
          >
        </div>
      </div>
    </section>
    <template v-if="manualInsert != null && !predictionAvailable">
      <b-loading :is-full-page="false" v-model="isLoading"></b-loading>
      <section v-if="manualInsert">
        <div class="columns mb-4">
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'danceability'" :name="'Danceability'" />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => Math.round(val * 100).toString()"
                  size="is-medium"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  v-model="currentFeatures.danceability"
                >
                  <b-slider-tick :value="0">0</b-slider-tick>
                  <b-slider-tick :value="1">100</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'energy'" :name="'Energy'" />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => Math.round(val * 100).toString()"
                  size="is-medium"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  v-model="currentFeatures.energy"
                >
                  <b-slider-tick :value="0">0</b-slider-tick>
                  <b-slider-tick :value="1">100</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'key'" :name="'Key'" />
              <b-field>
                <b-select v-model="currentFeatures.key">
                  <option
                    v-for="index in 12"
                    :value="index - 1"
                    :key="`${index}-key`"
                  >
                    {{ index - 1 }}
                  </option>
                </b-select>
              </b-field>
            </div>
          </div>
        </div>
        <div class="columns">
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'loudness'" :name="'Loudness'" />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => `${val} dB`"
                  size="is-medium"
                  :min="-60"
                  :max="0"
                  v-model="currentFeatures.loudness"
                >
                  <b-slider-tick :value="-60">-60 dB</b-slider-tick>
                  <b-slider-tick :value="0">0 dB</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'mode'" :name="'Mode'" />
              <b-field>
                <b-radio-button
                  v-model="currentFeatures.mode"
                  :native-value="0"
                  expanded
                >
                  Minor
                </b-radio-button>

                <b-radio-button
                  v-model="currentFeatures.mode"
                  :native-value="1"
                  expanded
                >
                  Major
                </b-radio-button>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'speechiness'" :name="'Speechiness'" />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => Math.round(val * 100).toString()"
                  size="is-medium"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  v-model="currentFeatures.speechiness"
                >
                  <b-slider-tick :value="0">0</b-slider-tick>
                  <b-slider-tick :value="1">100</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
        </div>
        <div class="columns">
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'acousticness'" :name="'Acousticness'" />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => Math.round(val * 100).toString()"
                  size="is-medium"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  v-model="currentFeatures.acousticness"
                >
                  <b-slider-tick :value="0">0</b-slider-tick>
                  <b-slider-tick :value="1">100</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title
                :feature="'instrumentalness'"
                :name="'Instrumentalness'"
              />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => Math.round(val * 100).toString()"
                  size="is-medium"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  v-model="currentFeatures.instrumentalness"
                >
                  <b-slider-tick :value="0">0</b-slider-tick>
                  <b-slider-tick :value="1">100</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'liveness'" :name="'Liveness'" />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => Math.round(val * 100).toString()"
                  size="is-medium"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  v-model="currentFeatures.liveness"
                >
                  <b-slider-tick :value="0">0</b-slider-tick>
                  <b-slider-tick :value="1">100</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
        </div>
        <div class="columns">
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'valence'" :name="'Valence'" />
              <b-field>
                <b-slider
                  :custom-formatter="(val) => Math.round(val * 100).toString()"
                  size="is-medium"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  v-model="currentFeatures.valence"
                >
                  <b-slider-tick :value="0">0</b-slider-tick>
                  <b-slider-tick :value="1">100</b-slider-tick>
                </b-slider>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'tempo'" :name="'Tempo'" />
              <div class="columns">
                <div class="column is-10">
                  <b-field>
                    <b-numberinput v-model="currentFeatures.tempo" :min="0" />
                  </b-field>
                </div>
                <div class="column is-2">BPM</div>
              </div>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title
                :feature="'duration_ms'"
                :name="'Duration in Seconds'"
              />
              <b-field>
                <b-numberinput v-model="currentFeatures.duration_ms" :min="0" />
              </b-field>
            </div>
          </div>
        </div>
        <div class="columns">
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title
                :feature="'time_signature'"
                :name="'Time Signature'"
              />
              <b-field>
                <b-select v-model="currentFeatures.time_signature">
                  <option
                    v-for="index in 5"
                    :value="index + 2"
                    :key="`${index}-signature`"
                  >
                    {{ index + 2 }}
                  </option>
                </b-select>
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title
                :feature="'chorus_hit'"
                :name="'Chorus Hit in Seconds'"
              />
              <b-field>
                <b-numberinput v-model="currentFeatures.chorus_hit" :min="0" />
              </b-field>
            </div>
          </div>
          <div class="column is-4 has-text-centered">
            <div class="box">
              <feature-title :feature="'sections'" :name="'Sections'" />
              <b-field>
                <b-numberinput v-model="currentFeatures.sections" :min="0" />
              </b-field>
            </div>
          </div>
        </div>
        <div class="columns">
          <div class="column is-4 is-offset-4">
            <b-button expanded type="is-primary" @click="hitPredict('')"
              >Hit or Not?</b-button
            >
          </div>
        </div>
      </section>
      <section v-else>
        <div class="columns">
          <div class="column is-9">
            <b-field label="Spotify Search (songs from 2020-2022)">
              <b-input v-model="query"></b-input>
            </b-field>
          </div>
          <div class="column is-3 is-flex is-align-items-end">
            <b-button
              type="is-primary"
              :disabled="query == '' || isLoading"
              expanded
              @click="spotifySearch"
              >Search</b-button
            >
          </div>
        </div>
        <template v-if="spotifyResults.length > 0">
          <div
            v-for="(result, index) in spotifyResults"
            :key="index"
            class="box columns mb-5"
          >
            <div class="column is-1">
              <b-image :src="result.album.images[1].url" />
            </div>
            <div class="column is-4">
              <div
                v-for="(artist, indexArtits) in result.artists"
                :key="`${indexArtits}-artists`"
              >
                {{ artist.name }}
              </div>
            </div>
            <div class="column is-4">
              <strong>{{ result.name }}</strong>
            </div>
            <div class="column is-3">
              <b-button type="is-primary" @click="hitPredict(index)"
                >Hit or Not?</b-button
              >
            </div>
          </div>
        </template>
      </section>
    </template>
    <template v-else-if="predictionAvailable">
      <section>
        <div class="columns">
          <div class="column is-2 has-text-centered">
            <div v-if="manualInsert"><strong>Manual Insert</strong></div>
            <div v-else>
              <b-image :src="currentTrackImageURL" />
              <div>
                <strong>{{ currentTrackName }}</strong>
              </div>
              <div
                v-for="(artist, index) in currentArtists"
                :key="`${index}-currentArtists`"
              >
                {{ artist.name }}
              </div>
            </div>
          </div>
          <div class="column is-10">
            <div class="columns">
              <div class="column is-one-fifth">
                <feature
                  :feature="'danceability'"
                  :name="'Danceability'"
                  :value="
                    Number.parseFloat(
                      currentFeatures.danceability * 100
                    ).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'energy'"
                  :name="'Energy'"
                  :value="
                    Number.parseFloat(currentFeatures.energy * 100).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'key'"
                  :name="'Key'"
                  :value="currentFeatures.key"
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'loudness'"
                  :name="'Loudness'"
                  :value="
                    Number.parseFloat(currentFeatures.loudness).toFixed(2) +
                    ' dB'
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'mode'"
                  :name="'Mode'"
                  :value="currentFeatures.mode == 1 ? 'Major' : 'Minor'"
                />
              </div>
            </div>
            <div class="columns">
              <div class="column is-one-fifth">
                <feature
                  :feature="'speechiness'"
                  :name="'Speechiness'"
                  :value="
                    Number.parseFloat(
                      currentFeatures.speechiness * 100
                    ).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'acousticness'"
                  :name="'Acousticness'"
                  :value="
                    Number.parseFloat(
                      currentFeatures.acousticness * 100
                    ).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'instrumentalness'"
                  :name="'Instrumentalness'"
                  :value="
                    Number.parseFloat(
                      currentFeatures.instrumentalness * 100
                    ).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'liveness'"
                  :name="'Liveness'"
                  :value="
                    Number.parseFloat(currentFeatures.liveness * 100).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'valence'"
                  :name="'Valence'"
                  :value="
                    Number.parseFloat(currentFeatures.valence * 100).toFixed(2)
                  "
                />
              </div>
            </div>
            <div class="columns">
              <div class="column is-one-fifth">
                <feature
                  :feature="'tempo'"
                  :name="'Tempo'"
                  :value="Number.parseFloat(currentFeatures.tempo).toFixed(2)"
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'duration_ms'"
                  :name="'Duration in seconds'"
                  :value="
                    Number.parseFloat(
                      currentFeatures.duration_ms * 0.001
                    ).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'time_signature'"
                  :name="'Time Signature'"
                  :value="currentFeatures.time_signature"
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'chorus_hit'"
                  :name="'Chorus Hit in seconds'"
                  :value="
                    Number.parseFloat(currentFeatures.chorus_hit).toFixed(2)
                  "
                />
              </div>
              <div class="column is-one-fifth">
                <feature
                  :feature="'sections'"
                  :name="'Sections'"
                  :value="currentFeatures.sections"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="columns mt-4">
          <div class="column has-text-centered is-size-4">
            <p v-if="manualInsert">
              Prediction: the selected set of features<strong>
                <span v-if="hit" class="has-text-success"> makes a hit!</span
                ><span v-else class="has-text-danger">
                  doesn't make a hit.</span
                ></strong
              >
            </p>
            <p v-else>
              Prediction:
              <strong
                >{{ currentTrackName }}
                <span v-if="hit" class="has-text-success"> is/was a hit!</span
                ><span v-else class="has-text-danger">
                  isn't/wasn't a hit.</span
                ></strong
              >
            </p>
          </div>
        </div>
      </section>
      <hr />
      <section>
        <div class="columns">
          <div class="column">
            <h1 class="title">Playlist Builder</h1>
            <p class="mb-3">Build a playlist based on this song/selection.</p>
            <p class="is-size-3">Criteria:</p>
          </div>
        </div>
        <div class="columns">
          <div class="column">
            <p class="is-size-5">Song Similarity</p>
            <b-field label="Weight">
              <b-slider
                :custom-formatter="(val) => Math.round(val * 100).toString()"
                size="is-medium"
                :min="0"
                :max="1"
                :step="0.01"
                v-model="criteria.songSimilarityWeight"
              >
                <b-slider-tick :value="0">Not Important</b-slider-tick>
                <b-slider-tick :value="1">Important</b-slider-tick>
              </b-slider>
            </b-field>
          </div>
          <div class="column is-1" />
          <div class="column">
            <p class="is-size-5">Hit or Not</p>
            <b-field label="Weight" class="mb-5">
              <b-slider
                class="mb-5"
                :custom-formatter="(val) => Math.round(val * 100).toString()"
                size="is-medium"
                :min="0"
                :max="1"
                :step="0.01"
                v-model="criteria.hitOrNotWeight"
              >
                <b-slider-tick :value="0">Not Important</b-slider-tick>
                <b-slider-tick :value="1">Important</b-slider-tick>
              </b-slider>
            </b-field>
            <br />
            <b-field class="mt-5">
              <b-select expanded v-model="criteria.hit">
                <option :value="true">Prefer hits</option>
                <option :value="false">Prefer not hits</option>
              </b-select>
            </b-field>
          </div>
          <div class="column is-1" />
          <div class="column">
            <p class="is-size-5">Main Feature</p>
            <b-field label="Weight">
              <b-slider
                :custom-formatter="(val) => Math.round(val * 100).toString()"
                size="is-medium"
                :min="0"
                :max="1"
                :step="0.01"
                v-model="criteria.mainFeatureWeight"
              >
                <b-slider-tick :value="0">Not Important</b-slider-tick>
                <b-slider-tick :value="1">Important</b-slider-tick>
              </b-slider>
            </b-field>
            <br />
            <b-field grouped>
              <b-field class="mt-5">
                <b-select v-model="criteria.mainFeatureHigher">
                  <option :value="true">More</option>
                  <option :value="false">Less</option>
                </b-select>
              </b-field>
              <b-field class="mt-5">
                <b-select v-model="criteria.mainFeature">
                  <option :value="'danceability'">Danceability</option>
                  <option :value="'energy'">Energy</option>
                  <option :value="'loudness'">Loudness</option>
                  <option :value="'speechiness'">Speechiness</option>
                  <option :value="'acousticness'">Acousticness</option>
                  <option :value="'instrumentalness'">Instrumentalness</option>
                  <option :value="'liveness'">Liveness</option>
                  <option :value="'valence'">Valence</option>
                  <option :value="'tempo'">Tempo</option>
                  <option :value="'duration_ms'">Duration</option>
                  <option :value="'sections'">Sections</option>
                </b-select>
              </b-field>
            </b-field>
          </div>
        </div>
        <div class="columns mt-2">
          <div class="column is-4 is-offset-4">
            <b-button expanded type="is-primary" @click="buildPlaylist()"
              >Build Playlist</b-button
            >
          </div>
        </div>
        <div v-if="playlistAvailable" class="columns mt-3">
          <div class="column">
            <b-table :data="playlist">
              <b-table-column field="artist" label="Artist" v-slot="props">
                {{ props.row.artist }}
              </b-table-column>
              <b-table-column field="track" label="Track" v-slot="props">
                {{ props.row.track }}
              </b-table-column>
              <b-table-column field="uri" label="Play" v-slot="props">
                <b-button
                  icon-left="play"
                  type="is-primary"
                  @click="openTrack(props.row.uri)"
                  >Play</b-button
                >
              </b-table-column>
            </b-table>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script>
import axios from "axios";

import Feature from "./Feature.vue";
import FeatureTitle from "./FeatureTitle.vue";

const apiBaseURL = "http://localhost:5000";

export default {
  components: {
    Feature,
    FeatureTitle,
  },
  data() {
    return {
      manualInsert: null,
      query: "",
      isLoading: false,
      spotifyResults: [],
      currentFeatures: {
        acousticness: 0,
        chorus_hit: 0,
        danceability: 0,
        duration_ms: 0,
        energy: 0,
        instrumentalness: 0,
        key: 0,
        liveness: 0,
        loudness: -6,
        mode: 0,
        sections: 0,
        speechiness: 0,
        tempo: 0,
        time_signature: 3,
        valence: 0,
      },
      currentTrackName: "",
      currentArtists: [],
      currentTrackImageURL: "",
      predictionAvailable: false,
      hit: true,
      criteria: {
        songSimilarityWeight: 0.75,
        hit: true,
        hitOrNotWeight: 0.25,
        mainFeature: "danceability",
        mainFeatureHigher: true,
        mainFeatureWeight: 0.25,
      },
      playlist: [],
      playlistAvailable: false,
    };
  },
  methods: {
    chooseInsertMethod(method) {
      this.predictionAvailable = false;
      this.playlistAvailable = false;
      this.currentFeatures = {
        acousticness: 0,
        chorus_hit: 0,
        danceability: 0,
        duration_ms: 0,
        energy: 0,
        instrumentalness: 0,
        key: 0,
        liveness: 0,
        loudness: -6,
        mode: 0,
        sections: 0,
        speechiness: 0,
        tempo: 0,
        time_signature: 3,
        valence: 0,
      };

      this.criteria = {
        songSimilarityWeight: 0.75,
        hit: true,
        hitOrNotWeight: 0.25,
        mainFeature: "danceability",
        mainFeatureHigher: true,
        mainFeatureWeight: 0.25,
      };

      if (method == "spotify") {
        this.query = "";
        this.spotifyResults = [];

        this.manualInsert = false;
        return;
      }

      this.manualInsert = true;
    },
    spotifySearch() {
      if (this.query == "") {
        return;
      }

      this.isLoading = true;

      axios
        .get(`${apiBaseURL}/spotify/search`, {
          params: { q: this.query },
        })
        .then((response) => {
          this.spotifyResults = response.data.tracks.items;

          this.isLoading = false;
        });
    },
    hitPredict(trackIndex) {
      this.isLoading = true;

      if (this.manualInsert) {
        this.currentFeatures.duration_ms *= 1000;

        this.currentTrackName = "Manual Insert";
        this.currentArtists = [];
        this.currentTrackImageURL = "Manual Insert";

        axios
          .post(
            `${apiBaseURL}/spotify/hit-prediction/manual`,
            this.currentFeatures
          )
          .then((response) => {
            this.hit = response.data.hit;

            this.predictionAvailable = true;
            this.isLoading = false;
          });
      } else {
        this.currentTrackName = this.spotifyResults[trackIndex].name;
        this.currentArtists = this.spotifyResults[trackIndex].artists;
        this.currentTrackImageURL =
          this.spotifyResults[trackIndex].album.images[1].url;

        axios
          .get(
            `${apiBaseURL}/spotify/${this.spotifyResults[trackIndex].id}/hit-prediction`
          )
          .then((response) => {
            this.currentFeatures = response.data.features;
            this.hit = response.data.hit;

            this.predictionAvailable = true;
            this.isLoading = false;
          });
      }
    },
    buildPlaylist() {
      this.isLoading = true;

      axios
        .post(`${apiBaseURL}/playlist/build`, {
          criteria: this.criteria,
          features: this.currentFeatures,
        })
        .then((response) => {
          this.playlist = response.data.playlist;

          this.playlistAvailable = true;
          this.isLoading = false;
        });
    },
    openTrack(uri) {
      const parts = uri.split(":");
      window.open("https://open.spotify.com/track/" + parts[2], "_blank");
    },
  },
};
</script>

