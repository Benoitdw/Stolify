""" Fonctions which are related to class"""
import spotipy
import classes
import json
from urllib.parse import unquote
from flask import flash
from youtube_dl import YoutubeDL


def create_track_obj(playlist_id, tokenSpotify):
    sp = spotipy.Spotify(auth=tokenSpotify)
    try:
        playlist_name = sp.playlist(playlist_id, fields="name")["name"]
    except:
        return False
    list_track = [
        playlist_name
    ]  # list of the tracks return the name of the list as first element (pas propre, à changer !)
    results = sp.playlist_tracks(playlist_id)
    for info in results["items"]:
        list_track.append(classes.Track(info["track"]))
        print("------------------------------------------------------------------")
    return list_track


def create_jsonFile(results, playlist_id):
    """make a json file from the results of the research
    return the json file name """
    data = {}
    data['playlist'] = {"name": results[0], "id": playlist_id}
    data['tracks'] = []
    for track in results[1:]:
        current_track = {}
        spotifyInfo = {}
        spotifyInfo['title'] = track.SpotifyTrack.title
        spotifyInfo['artist'] = track.SpotifyTrack.artist
        spotifyInfo['time'] = track.SpotifyTrack.time
        spotifyInfo['min'] = track.SpotifyTrack.min
        spotifyInfo['sec'] = track.SpotifyTrack.sec
        youtubeInfo = {}
        youtubeInfo['id'] = track.YoutubePage.id
        youtubeInfo['URL'] = track.YoutubePage.URL
        youtubeInfo['title'] = track.YoutubePage.title

        current_track['spotifyInfo'] = spotifyInfo
        current_track['youtubeInfo'] = youtubeInfo
        data['tracks'].append(current_track)
    path = "playlist_informations/{}.json".format(playlist_id)
    with open(path, "w") as outJsonFile: # TODO: Automatisation of directory playlist_informations creation
        json.dump(data, outJsonFile)


def openPlaylistJson(json_id):
    json_file_path = "playlist_informations/{}.json".format(json_id)
    with open(json_file_path, 'r') as json_file:
        playlist_data = json.load(json_file)
    return playlist_data


def downloadYt(json_id, ids):
    audioFormat = "mp3"  # Future posibilité de choisir son format
    playlist_data = openPlaylistJson(json_id)
    for id in ids:
        id = int(id) - 1  # Jinja iteration start to 1 and no 0
        path = "{}/{} - {}.{}".format(playlist_data['playlist']['name'], playlist_data['tracks']
                                      [id]['spotifyInfo']['title'], playlist_data['tracks'][id]['spotifyInfo']['artist'], audioFormat)

        ydl_opts = {
            'outtmpl': unquote(path),
            'format': 'bestaudio/best',
        }
        ydl = YoutubeDL(ydl_opts)
        try:
            with ydl:
                ydl.download(
                    [playlist_data['tracks'][id]['youtubeInfo']['URL']])
            if len(ids) == 1:
                flash("The file {} - {}.{} has been successfully downloaded in file /{} !".format(playlist_data['tracks']
                                                                                                  [id]['spotifyInfo']['title'], playlist_data['tracks'][id]['spotifyInfo']['artist'], audioFormat, playlist_data['playlist']['name']), 'success')
        except:
            flash("An error occured during download !", 'error')
