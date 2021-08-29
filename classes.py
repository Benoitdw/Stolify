from youtube_scraping_api import YoutubeAPI
from youtube_scraping_api.utils import getThumbnail

class SpotifyTrack:
    """
    input :
        track_info
    Permet d'avoir les informations propres au morceau récupéré auprès de
    spotify.
    """

    def __init__(self, track_info):
        self.title = track_info["name"]
        self.artist = track_info.get("artists")[0]["name"]
        self.time = track_info["duration_ms"]
        self.min = int(self.time / 60000)
        self.sec = int((self.time / 1000) % 60)
        self.cover = None
        print("{} - {} - {}:{}".format(self.artist, self.title, self.min, self.sec))


class YoutubePage:
    """
    input :
        title
        artist
    Permet d'avoir la première vidéo youtube lors de la recherche de title + artist
    (dans un premier temps, on peut voir après si on ne peut pas faire en fonction du temps
    avec une matrice de Poids.)
    """

    def __init__(self, title, artist):
        api = YoutubeAPI()
        research_query = (
            "https://www.youtube.com/results?search_query="
            + title.replace(" ", "+")
            + "+"
            + artist.replace(" ", "+")
        )
        first_video = api.search(research_query)[1]
        print(first_video)

        try:  # Test because may be no results
            self.id = first_video.id
            self.URL = "https://www.youtube.com/watch?v=" + first_video.id
            self.title = first_video.title
            self.image = getThumbnail(self.id)
            self.time = first_video.length
            print("{}".format(self.title))
        except:
            self.title = "NaN"
            self.id = None
            self.URL = "#"


class Track:
    """
    input :
        track id
    Permet d'associer les classes propres au morceau dans une classe mère
    """

    def __init__(self, track_info):
        self.SpotifyTrack = SpotifyTrack(track_info)
        self.YoutubePage = YoutubePage(
            self.SpotifyTrack.title, self.SpotifyTrack.artist
        )
