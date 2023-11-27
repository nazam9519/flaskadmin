from flask import Blueprint
from flask import jsonify
from flask import request
from pathlib import Path
import os
import subprocess 
import json
from requests import session
import re
from bs4 import BeautifulSoup
#from feedgen.feed import FeedGenerator
from modules.setlogs import setlogger
match_imdb = re.compile(r"^https?://www.imdb.com")
match_tmdb = re.compile(r"^https?://www.themoviedb.org")
fp = '/opt/rest/currentfiles'
base_url = "https://letterboxd.com"

MATCH_TOTAL_MOVIES = re.compile(r"to see (\d+)")
s = session()
letterboxd_c = Blueprint('letterboxd',__name__)

@letterboxd_c.route('/rss',methods=['GET'])
def rss():
    logger = setlogger("letterboxd_app")
    logger.info(f"shutting down app: hit")
    user = request.args.get('user')
    watchlist_url = f"{base_url}/{user}/watchlist"
    
    # Get first page, gather general data
    r = s.get(watchlist_url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    jsoon = None
    watchlist_title = soup.find("meta", attrs={"property": "og:title"})
    page_title = watchlist_title.attrs["content"]
    if Path(f"{fp}/spliff_db.json").exists():
        jsoon = handlejson(fp+"/spliff_db.json")
        
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
            check = False
            if jsoon is not None:
                check = any(d['slug'] == movie.div.attrs['data-film-slug'] for d in jsoon)
            else:
                jsoon = []
            if check == True:
                continue
            else:
                added = extract_metadata(movie)
                jsoon.append(added)
                #jsoon.append({'url':movie.div.attrs['data-film-slug']})
            #added.append(extract_metadata(movie))# = extract_metadata(movie, feed)
            # Update total counter
            print(len(added))
            #movies_added += 1
            print(f"count added: {movies_added}")
        with open(f"{fp}/spliff_db.json",'w',encoding='utf-8') as f:
            json.dump(jsoon,f,ensure_ascii=False, indent=4)
    return jsonify(handlejson(f"{fp}/spliff_db.json"))



def extract_metadata(movie):
    movie_url = base_url +"/film/"+ movie.div.attrs["data-film-slug"]
    movie_slug = movie.div.attrs["data-film-slug"]
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
        movie_tm = movie_soup.find("body").attrs['data-tmdb-id']
        if movie_link.endswith("/maindetails"):
            movie_link = movie_link[:-11]
        movie_description = movie_soup.find(
            "meta", attrs={"property": "og:description"}
        )
        if movie_description is not None:
            movie_description = movie_description.text.strip()
        return {
            'title':movie_title,
            'tmdb_id':movie_tm,
            'slug':movie_slug
        }
    except Exception:
        print("Parsing failed on", movie_url)

    return 0
def handlejson(path: str):
    with open(path) as f:
        d = json.load(f)
        return d