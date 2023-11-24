from flask import Blueprint
from flask import jsonify
from flask import request
import os
import subprocess 
from requests import session
import re
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
match_imdb = re.compile(r"^https?://www.imdb.com")
match_tmdb = re.compile(r"^https?://www.themoviedb.org")

base_url = "https://letterboxd.com"

MATCH_TOTAL_MOVIES = re.compile(r"to see (\d+)")
s = session()
letterboxd_c = Blueprint('letterboxd',__name__)

@letterboxd_c.route('/rss',methods=['GET'])
def rss():
    user = request.args.get('user')
    watchlist_url = f"{base_url}/{user}/watchlist"

    page_title = "The Dude's Watchlist"


    # Get first page, gather general data
    r = s.get(watchlist_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    watchlist_title = soup.find("meta", attrs={"property": "og:title"})
    page_title = watchlist_title.attrs["content"]

    m = soup.find("span", attrs={"class": "js-watchlist-count"})
    if len(m) > 0:
        total_movies = int(m.text.split()[0])
        print(f"Found a total of {total_movies} movies")

    last_page = soup.find_all("li", attrs={"class": "paginate-page"})[-1].text
    last_page = int(last_page)

    movies_added = 0
    added = []
    for page in range(1, last_page):
        if page > 1:
            r = s.get(watchlist_url + "/page/%i/" % page)
            soup = BeautifulSoup(r.text, "html.parser")
            print()

        ul = soup.find("ul", attrs={"class": "poster-list"})
        movies = ul.find_all("li")
        movies_on_page = len(movies)

        print(f"Gathering on page {page} (contains {movies_on_page} movies)\n")

        for movie in movies:
            added.append(extract_metadata(movie))# = extract_metadata(movie, feed)
            # Update total counter
            movies_added += added
    #if user == '':
     #   subprocess.Popen(['sudo','/opt/rest/admin/restart_app.pl',f'{os.getpid()}'])
      #  return jsonify({'msg':f'restarting app: {os.getpid()} please wait 30 seconds...'})
    #else:
     #   return jsonify({'msg':f"unknown admin arg "})


def extract_metadata(movie):
    movie_url = base_url +"film/"+ movie.div.attrs["data-film-slug"]
    movie_page = s.get(movie_url)
    movie_soup = BeautifulSoup(movie_page.text, "html.parser")

    try:
        movie_title = movie_soup.find("meta", attrs={"property": "og:title"}).attrs[
            "content"
        ]
        print("Adding", movie_title)
        movie_link = movie_soup.find(
            "a", attrs={"href": [match_imdb, match_tmdb]}
        ).attrs["href"]
        if movie_link.endswith("/maindetails"):
            movie_link = movie_link[:-11]
        movie_description = movie_soup.find(
            "meta", attrs={"property": "og:description"}
        )
        if movie_description is not None:
            movie_description = movie_description.text.strip()
        return {
            'title':movie_title,
            'imdb_id':movie_link
        }
        #item = feed.add_item()
        #item.title(movie_title)
        #item.description(movie_description)
        #item.link(href=movie_link, rel="alternate")
        #item.guid(movie_link)

        return 1
    except Exception:
        print("Parsing failed on", movie_url)

    return 0