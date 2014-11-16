import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CSV_FILE_PATH = "/home/yogesh/Coursera/DataScience/aamir_khan_analysis/aamir_movie_imdb.csv"

def read_csv():
    movie_file = pd.read_csv(CSV_FILE_PATH)
    return movie_file

def process_csv(pandas_csv_obj):
    data_tuple_list = []
    year_data = pandas_csv_obj.groupby("Year")
    for name, group in year_data:
        #data_dict[name] = [group["Name"].count()]
        hit_count = 0
        for rating in group.Rating:
            if rating >= 7.0:
                hit_count += 1
        data_tuple = (name, group["Name"].count(), hit_count)
        data_tuple_list.append(data_tuple)
    return data_tuple_list

def plot_graph(data_tuple_list):
    d = pd.DataFrame(data_tuple_list, columns=["Year", "Count", "Hits"])
    d.describe()
    d.groupby("Year").plot(kind="bar")
    #plt.show()
    return

def start():
    movie_file = read_csv()
    data_tuple_list = process_csv(movie_file)
    plot_graph(data_tuple_list)

if __name__ == "__main__":
    start()
