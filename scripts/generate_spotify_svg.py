import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import svgwrite
from datetime import datetime

OUTPUT = "assets/spotify.svg"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ["fb783c391d274280b3fb1f811f688a89"],
        client_secret=os.environ["479181a6d7fe47e7a2841c5823b4f63a"],
        redirect_uri="http://127.0.0.1:80/callback",
        scope="user-read-currently-playing user-read-playback-state",
        cache_path=".spotify_cache"
    )
)

current = sp.current_playback()

dwg = svgwrite.Drawing(OUTPUT, size=("400px", "80px"))

# Background
dwg.add(dwg.rect(insert=(0, 0), size=("400px", "80px"), rx=12, fill="#121212"))

if current and current.get("item"):
    track = current["item"]["name"]
    artist = ", ".join(a["name"] for a in current["item"]["artists"])
    status = "▶ Now Playing"
else:
    track = "Nothing playing"
    artist = ""
    status = "⏸ Spotify"

dwg.add(dwg.text(status, insert=(15, 28), fill="#1DB954", font_size="14"))
dwg.add(dwg.text(track, insert=(15, 52), fill="white", font_size="16"))
dwg.add(dwg.text(artist, insert=(15, 70), fill="#b3b3b3", font_size="12"))

# cache-buster comment
dwg.add(dwg.comment(f"updated {datetime.utcnow().isoformat()}"))

dwg.save()
print("spotify.svg updated")
