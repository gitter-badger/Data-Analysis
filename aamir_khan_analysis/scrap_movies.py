import requests
from BeautifulSoup import BeautifulSoup
import csv

URL = "http://www.movieslistdb.com/aamir-khan-movies-list"

def openSiteAndParse():
    handle = requests.get(URL)
    html = handle.text

    soup = BeautifulSoup(html)
    movie_tag_list = soup.find("ul", {"class": "movies-list-mobile"}).findAll("li")
    with open("aamir_khan_movie_list.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Movie_Name", "Movie_Year"])
        for movie_tag in movie_tag_list:
            try:
                movie_name = movie_tag.find("span", {"class": "name-span"}).text
                movie_year = movie_tag.find("span", {"class": "year-span"}).text
                print "Adding Name %s and year %s"%(movie_name, movie_year)
                csvwriter.writerow([movie_name, movie_year])
            except:
                continue


if __name__ == "__main__":
    openSiteAndParse()


