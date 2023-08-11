import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth



past = input(" What year you would like to travel to? Type in YYY-MM-DD format: ") #to get the date of the billboards top 100 needes
URL = f"https://www.billboard.com/charts/hot-100/{past}"
#Initializing object of Spotify class
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id="YOUR ID",
        client_secret="YOUR CLIENT SECRET",
        show_dialog=True,
        cache_path="token.txt",
        username="YOUR USERNAME"
    )
)
user_id = sp.current_user()["id"]
#Accessing the source code
r = requests.get(URL)
website = r.text
#Parsing HTML
soup = BeautifulSoup(website, "html.parser")
song_names=[song.getText().strip() for song in soup.find_all(name="h3", class_="a-no-trucate")]

song_uris = []
year = past.split("-")[0]
for song in song_names:
    finds = sp.search(q= f"track:{song} year:{year} ", type="track")

    #raise exception if song is not found in spotify
    try:
        uri = finds["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} is not found in Spotify")
#Create new playlist
playlist = sp.user_playlist_create(user=user_id, name= f"Billboard Top 100 on {past}", public= False)
id = playlist['id']
#Add the songs from the list to the playlist
sp.playlist_add_items(playlist_id=id,items=song_uris)





