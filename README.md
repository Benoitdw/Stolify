# Stolify
Stolify is a free and open source Flask App to download Spotify's playlist trough Youtube.

## Disclaimer
This application is based on youtube-dl, is it legal to use youtube-dl? It's a grey area that I will not
discuss here. However you can find more informations here:  

* [Is it legal to use youtube-dl?](https://www.reddit.com/r/youtubedl/comments/k4rq23/is_it_legal_to_use_youtubedl/)

* [American Laws](https://www.eff.org/deeplinks/2020/11/github-youtube-dl-takedown-isnt-just-problem-american-law)

* [Does youtube-dl face any legal issues?](https://www.quora.com/Does-youtube-dl-face-any-legal-issues?share=1)

## Know bugs
*   There is a issue for wrapping youtube. It leads the app to not find any music on youtube.

## Quick start






## Run 
```bash
flask run
```

## FAQ

*No informations from youtube ?*
Update your youtube_dl version, this is appening very often. 
In your venv : `pip3 youtube_dl -U`

*Flask not found*
Be sure to launch your venv
```bash
cd <path to your flask application>
source venv/bin/activate
```
