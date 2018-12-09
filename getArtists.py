import os
import sys

import io
import time
import datetime

import discogs_client

import traceback

from utils import printSample

if not os.path.isdir("data"):
    os.mkdir("data")

if not os.path.exists("data/token.txt"):
    print("Agrega tu token fren ...")
    sys.exit(0)

tk = open("data/token.txt", "r")
MY_TOKEN = tk.readline()

# release_keys = ['user_data', 'community', 'catno', 'year', 'id', 'style', 'thumb', 'title', 'label', 'master_id', 'type', 'format', 'barcode', 'master_url', 'genre', 'country', 'uri', 'cover_image', 'resource_url', 'status', 'videos', 'series', 'labels', 'artists', 'images', 'format_quantity', 'artists_sort', 'genres', 'num_for_sale', 'date_changed', 'lowest_price', 'styles', 'released_formatted', 'formats', 'estimated_weight', 'released', 'date_added', 'extraartists', 'tracklist', 'notes', 'identifiers', 'companies', 'data_quality']
artists_keys = ['id',
                'title',
                'labels',
                'master_id',
                'country',
                'year',
                'released',
                'genre',
                'style',
                'artists',
                'tracklist',
                'uri']

TICK = 5 # 50
SLEEP_TIME = 1 # 120

def writeArtists(d, encoding='utf-8'):
    year = 2008
    suma = 0
    for i in range(10):
        print("Artist for year " + str(year + i) + "in Chile.")
        suma += writeInfo(d, "artist", str(year + i) ,encoding)
        print("Get to sleep for {}s at: {}".format(SLEEP_TIME, datetime.datetime.now()))
        time.sleep(SLEEP_TIME)
        print("Wake up at {} ...".format(datetime.datetime.now()))
    print("Total artists: " + str(suma))
    return suma

def writeEncoded(fd, s, encoding):
    fd.write(s.encode(encoding))

def writeInfo(d, search_type, search_year, encoding):
    results = d.search('*', type=search_type)
    count_results = results.count
    print("Count: ", count_results)
    # print(results)
    with io.open("data/artists" + search_year + ".csv", 'wb+') as fd_a:
        header_a = ""
        for column in artists_keys:
            header_a += column + '\t'
        header_a = header_a[:-1] + '\n'
        writeEncoded(fd_a, header_a, encoding)
        count = 0
        try:
            for element in results:
                writeResults(fd_a, element, encoding)
                count += 1
                print("read ...{} lines".format(count))
                if count % TICK == 0:
                    print("Get to sleep for {}s at: {}".format(SLEEP_TIME, datetime.datetime.now()))
                    time.sleep(SLEEP_TIME)
                    print("Wake up at {} ...".format(datetime.datetime.now()))
        except Exception as e:
            print("ups")
            print(e)
            traceback.print_exc()
        finally:
            fd_a.close()
    return count_results

def stringList(data, list_key=None):
    s = ""
    for entity in data:
        if list_key == "tracklist":
            s += "<{} {}>,".format(entity['position'], entity['title'])
        elif list_key is not None:
            s += str(entity[list_key]) + ","
        else:
            s += str(entity) + ","
    # Escribir en archivo la informacion
    s = s[:-1]
    # print(s)
    return s


def writeResults(fd_artists, artist, encoding='utf-8'):
    # Para los lanzamientos en Chile
    s_artist = ""
    # Escribir informacion de lanzamiento
    my_keys = artist.data.keys()
    print(my_keys)
    for key in my_keys: #artists_keys:
        print("{}: {}".format(key, artist.data[key]))
        continue
        if key not in my_keys:
            s_artist += "" + '\t'
        elif key in ["labels", "artists"]:
            s_artist += stringList(artist.data[key], list_key="id") + '\t'
        elif key in ["genre", "style"]:
            s_artist += stringList(artist.data[key]) + '\t'
        elif key == "tracklist":
            s_artist += stringList(artist.data[key], list_key="tracklist") + '\t'
        else:
            s_artist += str(artist.data[key]) + "\t"
    print("################################################################################")
    # writeEncoded(fd_artists, s_artist[:-1] + "\n", encoding)


d = discogs_client.Client('ExampleApplication/0.1', user_token=MY_TOKEN)

# getReleases(d)
# printSample(d, 'release', keys=release_keys)
writeArtists(d)



