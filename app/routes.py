from flask import render_template, send_from_directory, flash, redirect, url_for, request
from app import app
from app.forms import PlaylistSearchForm
from spotifyFct import identificationSpotify, list_featured_playlist, list_current_user_playlist, isPlaylist
from class_fct import create_track_obj, create_jsonFile, openPlaylistJson, downloadYt
from pathlib import Path
import os.path
import time

tokenSpotify = identificationSpotify("username")


@app.route("/")
@app.route("/index")
@app.route("/index/<error>")
@app.route("/", methods=['GET', 'POST'])
def index(error=False):
    if tokenSpotify:
        featured_playlists = list_featured_playlist(tokenSpotify)
        current_user_playlist = list_current_user_playlist(
            tokenSpotify)
        playlist_search = PlaylistSearchForm()
        if playlist_search.validate_on_submit():
            # Verifie si le champ URI n'est pas vide (default)
            flash(playlist_search.uri.data + " is not a valid URI.")
            if isPlaylist(tokenSpotify, playlist_search.uri.data) == True:
                # Verifie si URI correspond à playlist
                return redirect(url_for('loadingPage', playlist_id=playlist_search.uri.data))
        return render_template(
            "index.html", title="Home", form=playlist_search, featured_playlists=featured_playlists, current_playlist=current_user_playlist
        )
    else:
        print("erreur d'identification spotify")
        # return page d'erreur


@app.route("/create_results/<playlist_id>/<int:renew>")
def create_results(playlist_id, renew):
    json_file = Path("playlist_informations/{}.json".format(playlist_id))
    print(renew)
    print(renew and json_file.is_file() and
          (time.time() - os.path.getmtime(json_file)) < 1000)
    if (json_file.is_file() and ((time.time() - os.path.getmtime(json_file)) < 1000) and not renew):
        # Don't create a new file if it already exist.
        # and was not modified since 1 day.
        print("renew")
        pass
    else:
        results = create_track_obj(playlist_id, tokenSpotify)
        create_jsonFile(results, playlist_id)
    return redirect(url_for('display_results', json_id=playlist_id))


@app.route("/display_results/<json_id>")
def display_results(json_id):
    playlist_data = openPlaylistJson(json_id)
    return render_template("results.html", title="Results", playlist_data=playlist_data)


@app.route("/loadingPage/<playlist_id>")
@app.route("/loadingPage/<playlist_id>/<renew>")
def loadingPage(playlist_id, renew=0):
    return render_template("loadingPage.html", title="Wait please", send=playlist_id, renew=renew)


@app.route("/download/<json_id>/<id>")
def download(json_id, id, multi=False):
    id = [id]
    downloadYt(json_id, id)
    return redirect(url_for('display_results', json_id=json_id))


@app.route("/multiDownload/<json_id>", methods=['GET', 'POST'])
def multiDownload(json_id):
    ids = request.form.getlist('foo')
    downloadYt(json_id, ids)
    if len(ids) > 1:
        flash("{} tracks of the playlist {} has been successfully downloaded !".format(
            len(ids), json_id), 'success')
    return render_template("lobby_after_multidownload.html", title="test", send=id)
