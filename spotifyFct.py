import spotipy.util as util
import spotipy
import json

scope = "user-library-read"


def identificationSpotify(username):
    token = util.prompt_for_user_token(
        username,
        scope,
        client_id="25f213e47b4e4c348e603e2147efaa0a",
        client_secret="35cbc40cf21d4e2a9af00729ead6d910",
        redirect_uri="https://github.com/",
    )
    return token


def list_featured_playlist(token):
    sp = spotipy.Spotify(auth=token)
    results = sp.featured_playlists(limit=20)
    return results


def list_current_user_playlist(token):
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playlists(limit=20)
    return results


def isPlaylist(token, id_to_check):
    """Check if the id is correct or not"""
    sp = spotipy.Spotify(auth=token)
    try:
        sp.playlist(id_to_check, fields=None)
        print("ok")
        return True
    except:
        print("not ok")
        return False
