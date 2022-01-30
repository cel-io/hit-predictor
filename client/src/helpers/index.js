export function getFeatureDescription(featureType) {
  switch (featureType) {
    case "danceability":
      return "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0 is least danceable and 100 is most danceable.";
    case "energy":
      return "Energy is a measure from 0 to 100 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.";
    case "key":
      return "The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C?/D?, 2 = D, and so on.";
    case "loudness":
      return "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.";
    case "mode":
      return "Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived.";
    case "speechiness":
      return "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 100 the attribute value. Values above 66 describe tracks that are probably made entirely of spoken words. Values between 33 and 66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 33 most likely represent music and other non-speech-like tracks.";
    case "acousticness":
      return "A confidence measure from 0 to 100 of whether the track is acoustic. 100 represents high confidence the track is acoustic.";
    case "instrumentalness":
      return "Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 100, the greater likelihood the track contains no vocal content. Values above 50 are intended to represent instrumental tracks, but confidence is higher as the value approaches 100.";
    case "liveness":
      return "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 80 provides strong likelihood that the track is live.";
    case "valence":
      return "A measure from 0 to 100 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).";
    case "tempo":
      return "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.";
    case "duration_ms":
      return "The duration of the track in seconds.";
    case "time_signature":
      return "An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).";
    case "chorus_hit":
      return "This the the author's best estimate of when the chorus would start for the track.";
    case "sections":
      return "The number of sections the particular track has.";
  }
}
