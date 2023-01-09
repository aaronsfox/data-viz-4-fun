# Triple J's Hottest 100s



## Code

The following list outlines the relevant code/scripts used to collate and process data. A basic description is provided here, while the comments throughout the code provide more detail as to what is happening

- **collateTrackData.py**: Scrapes the track and artist data from the Spotify playlists.



## Data



***[TODO: clean up notes]***

- Track, artist and audio feature data extracted from Spotify API
- Artist data from MusicBrainz?



### Data Dictionary

**hottestID:** An id for which years Hottest 100 the song came from.

**artist:** Name of the artist responsible for the track.

**artistURI:** Spotify URI ID for artist.

**artistLink:** Spotify web link for the artist.

**track:** Name of the track.

**trackLink:** Spotify web link to the track.

**duration:** Duration of the track in seconds.

**explicit:** True or False for whether the track is listed as 'explicit' on Spotify.

**acousticness:** A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.

**danceability:** Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.

**energy:** Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.

**instrumentalness:** Predicts whether a track contains no vocals. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.

**liveness:** Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.

**speechiness:** Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.

**valence:** A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

**key:** Estimated key of the track.

**tempo:** Estimated tempo in beats per minute of the track.

**timeSignature:** Estimated time signature of the track.