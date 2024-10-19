# Importing necessary libraries
import pickle  # For loading serialized objects from files
import streamlit as st  # For building interactive web applications
import spotipy  # For interacting with the Spotify API
from spotipy.oauth2 import SpotifyClientCredentials  # For handling Spotify API authentication

# Define your Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"  # Your Spotify client ID
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"  # Your Spotify client secret

# Initialize the Spotify client using client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)  # Create a credentials manager
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # Create a Spotify client instance

# Function to get the album cover URL for a given song and artist
def get_song_album_cover_url(song_name, artist_name):
    # Formulate the search query for the Spotify API
    search_query = f"track:{song_name} artist:{artist_name}"  # Combine song and artist into a query string
    results = sp.search(q=search_query, type="track")  # Search for the track using the Spotify API

    # Check if any results were returned
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]  # Get the first track from the results
        album_cover_url = track["album"]["images"][0]["url"]  # Extract the URL of the album cover
        print(album_cover_url)  # Print the URL to the console (for debugging)
        return album_cover_url  # Return the album cover URL
    else:
        # If no results were found, return a default image URL
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to recommend songs based on a given song
def recommend(song):
    # Find the index of the selected song in the music DataFrame
    index = music[music['song'] == song].index[0]  # Get the index of the song
    # Calculate sorted distances for recommendations
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])  # Sort the distances based on similarity
    recommended_music_names = []  # List to hold the names of recommended songs
    recommended_music_posters = []  # List to hold the URLs of recommended song posters (album covers)

    # Loop through the top 5 recommendations (excluding the first one, which is the selected song)
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist  # Get the artist name of the recommended song
        print(artist)  # Print the artist name to the console (for debugging)
        print(music.iloc[i[0]].song)  # Print the recommended song name to the console (for debugging)
        # Fetch the album cover URL for the recommended song
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))  # Get album cover URL and append to the list
        recommended_music_names.append(music.iloc[i[0]].song)  # Append the song name to the recommendations list

    return recommended_music_names, recommended_music_posters  # Return the lists of recommended song names and their album cover URLs

# Streamlit application header
st.header('Music Recommender System')  # Display the header for the app

# Load the music dataset and similarity matrix from pickle files
music = pickle.load(open('df.pkl', 'rb'))  # Load the music DataFrame from a pickle file
similarity = pickle.load(open('similarity.pkl', 'rb'))  # Load the similarity matrix from a pickle file

# Create a list of song names from the music DataFrame
music_list = music['song'].values  # Get the song names as a NumPy array

# Create a dropdown selection box for users to choose a song
selected_movie = st.selectbox(
    "Type or select a song from the dropdown",  # Prompt text for the selection box
    music_list  # The list of song names to be displayed in the dropdown
)

# If the user clicks the "Show Recommendation" button
if st.button('Show Recommendation'):
    # Get recommended music names and posters based on the selected song
    recommended_music_names, recommended_music_posters = recommend(selected_movie)  # Call the recommend function
    # Create columns for displaying the recommended songs and their album covers
    col1, col2, col3, col4, col5 = st.columns(5)  # Create 5 columns

    # Display the recommended songs and their album covers in the columns
    with col1:
        st.text(recommended_music_names[0])  # Show the first recommended song name
        st.image(recommended_music_posters[0])  # Show the first recommended song album cover

    with col2:
        st.text(recommended_music_names[1])  # Show the second recommended song name
        st.image(recommended_music_posters[1])  # Show the second recommended song album cover

    with col3:
        st.text(recommended_music_names[2])  # Show the third recommended song name
        st.image(recommended_music_posters[2])  # Show the third recommended song album cover

    with col4:
        st.text(recommended_music_names[3])  # Show the fourth recommended song name
        st.image(recommended_music_posters[3])  # Show the fourth recommended song album cover

    with col5:
        st.text(recommended_music_names[4])  # Show the fifth recommended song name
        st.image(recommended_music_posters[4])  # Show the fifth recommended song album cover
