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

# ARTIST_KEYS = ['thumb', 'title', 'user_data', 'master_url', 'uri', 'cover_image', 'resource_url', 'master_id', 'type', 'id', 'name']
ARTIST_KEYS = ['id', 'name', 'realname', 'members', 'uri']

TICK = 15
SLEEP_TIME = 65 #


def writeArtists(d, encoding='utf-8'):
    year = 2008
    visited_artists = []
    for i in range(2): # (10):
        print("Artist for year " + str(year + i) + " in Chile.")
        writeInfo(d, visited_artists, str(year + i), encoding)
        print("Get to sleep for {}s at: {}".format(SLEEP_TIME, datetime.datetime.now()))
        time.sleep(SLEEP_TIME)
        print("Wake up at {} ...".format(datetime.datetime.now()))
    print("Total artists: " + str(len(visited_artists)))
    return len(visited_artists)



def writeEncoded(fd, s, encoding):
    fd.write(s.encode(encoding))


def writeInfo(d, visited_artists, search_year, encoding):
    # results = d.search('*', type=search_type)
    # count_results = results.count
    # print("Count: ", count_results)
    # print(results)
    with io.open("data/releases" + search_year + ".csv", 'rb') as fd_r:
        with io.open("data/artists" + search_year + ".csv", 'wb+') as fd_a:
            header_a = ""
            for column in ARTIST_KEYS:
                header_a += column + '\t'
            header_a = header_a[:-1] + '\n'
            writeEncoded(fd_a, header_a, encoding)
            count = 0
            fd_r.readline()
            for line in fd_r:
                line = line.decode(encoding)
                artists = line.split('\t')[-3].split(',')
                for artist_id in artists:
                    count += 1
                    try:
                        writeResults(fd_a, d, artist_id, visited_artists, encoding)
                    except Exception as e:
                        print("ups")
                        print(e)
                        traceback.print_exc()
                    print("read ...{} lines".format(count))
                    if count % TICK == 0:
                        print("Get to sleep for {}s at: {}".format(SLEEP_TIME, datetime.datetime.now()))
                        time.sleep(SLEEP_TIME)
                        print("Wake up at {} ...".format(datetime.datetime.now()))
                        return
    return

def writeMembers(data, write):
    s = ""
    for entity in data:
        write(entity['id'])
        s += str(entity['id']) + ","
    # Escribir en archivo la informacion
    s = s[:-1]
    # print(s)
    return s


def writeResults(fd_artists, d, artist_id, visited_artists, encoding='utf-8'):
    if artist_id in visited_artists:
        return
    else:
        visited_artists.append(artist_id)
    artist = d.artist(artist_id)
    # Para los lanzamientos en Chile
    s_artist = ""
    # Escribir informacion de lanzamiento
    my_keys = artist.data.keys()
    print(artist.name)
    # print(my_keys)
    for key in ARTIST_KEYS:  # artists_keys:
        if key not in my_keys:
            s_artist += "" + '\t'
            continue
        elif key == "members":
            f = lambda x: writeResults(fd_artists, d, x, visited_artists)
            s_artist += writeMembers(artist.data[key], f) + '\t'
        else:
            s_artist += str(artist.data[key]) + "\t"
        # print("{}: {}".format(key, artist.data[key]))
    # print("################################################################################")
    writeEncoded(fd_artists, s_artist[:-1] + "\n", encoding)


d = discogs_client.Client('ExampleApplication/0.1', user_token=MY_TOKEN)

# getReleases(d)
# printSample(d, 'release', keys=release_keys)
writeArtists(d)
