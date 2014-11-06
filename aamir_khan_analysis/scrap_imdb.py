import requests
from bs4 import BeautifulSoup
import csv
import re
import time

URL = "http://www.imdb.com/name/nm0451148/?ref_=nv_sr_1"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0"

HEADERS={"User-Agent": USER_AGENT}

def get_rating(url):
    handle = requests.get(url, headers=HEADERS)
    html = handle.text
    soup = BeautifulSoup(html)
    rating_star_tag = soup.find("div", {"class": "titlePageSprite star-box-giga-star"})
    rating = rating_star_tag.text.strip()
    return rating

def parse_movie(html):
    soup = BeautifulSoup(html)
    f = open("aamir_movie_imdb.csv", "w")
    writer = csv.writer(f)
    writer.writerow(["Name", "Year", "Rating"])
    div_movie_tag_list = soup.find("div", {"class": "filmo-category-section"}).find_all("div", recursive=False)
    for div_movie_tag in div_movie_tag_list:
        # Don't hit server too fast
        time.sleep(2)
        movie_name = None
        #Get Year
        year_tag = div_movie_tag.find("span", {"class": "year_column"})
        year = year_tag.text.strip()
        year = year.replace("&nbsp;", "")

        #Get Movie name
        name_tag = div_movie_tag.find("b")
        full_tag_text = " ".join(div_movie_tag.findAll(text=True))
        if not re.search("(\s|\()(TV|filming)(\s|\))", full_tag_text, re.I):
            movie_name = name_tag.a.text.strip()
            #Get rating for movie
            url = "http://www.imdb.com"+name_tag.a["href"]
            rating = get_rating(url)
            print "#####"
            print "Movie Name--->%s"%movie_name
            print "Rating---->%s"%rating
            print "Year---->%s"%year
            print "#####"
            writer.writerow([movie_name, year, rating])
    f.close()

def get_imdb_page():
    handle = requests.get(URL, headers=HEADERS)
    return handle.text

if __name__ == "__main__":
    html = get_imdb_page()
    parse_movie(html)


