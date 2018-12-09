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
release_keys = ['id',
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

track_keys = ['position', 'title', 'duration', 'artists']

TICK = 50
SLEEP_TIME = 120

def writeReleases(d, encoding='utf-8'):
    year = 2008
    for i in range(10):
        print("Release for year " + str(year + i))
        writeInfo(d, "release", str(year + i) ,encoding)

def writeEncoded(fd, s, encoding):
    fd.write(s.encode(encoding))

def writeInfo(d, search_type, search_year, encoding):
    results = d.search('*', type=search_type, country="Chile", year=search_year)
    print("Count: ", results.count)
    # print(results)
    with io.open("data/releases" + search_year + ".csv", 'wb') as fd_r:
        header_r = ""
        for column in release_keys:
            header_r += column + '\t'
        header_r = header_r[:-1] + '\n'
        writeEncoded(fd_r, header_r, encoding)
        with io.open("data/tracks" + search_year + ".csv", 'wb+') as fd_t:
            header_t = "release_id\t"
            for column in track_keys:
                header_t += column + '\t'
            header_t = header_t[:-1] + '\n'
            writeEncoded(fd_t, header_t, encoding)
            count = 0
            try:
                for element in results:
                    writeResults(fd_r, fd_t, element, encoding)
                    print("read ...{} lines".format(count))
                    count += 1
                    if count % TICK == 0:
                        print("Get to sleep for {}s at: {}".format(SLEEP_TIME, datetime.datetime.now()))
                        time.sleep(SLEEP_TIME)
                        print("Wake up at {} ...".format(datetime.datetime.now()))
                        return
            except Exception as e:
                print("ups")
                print(e)
                traceback.print_exc()
            finally:
                fd_t.close()
                fd_r.close()

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


def writeResults(fd_releases, fd_tracks, release, encoding='utf-8'):
    # Para los lanzamientos en Chile
    if release.country.lower() == "chile":
        # Obtener lista de canciones de dicho lanzamiento
        for track in release.tracklist:
            s_artists = ""
            for artist in track.artists:
                s_artists += str(artist.id) + ","
            # Si no habian artistas, solo se deja en null
            s_tracks = "{}\t{}\t{}\t{}\t{}\n".format(release.id, track.position, track.title, track.duration, s_artists[:-1])
            # Escribir en archivos de canciones
            writeEncoded(fd_tracks, s_tracks, encoding)
        s_release = ""
        # Escribir informacion de lanzamiento
        my_keys = release.data.keys()
        for key in release_keys:
            if key not in my_keys:
                s_release += "" + '\t'
            elif key in ["labels", "artists"]:
                s_release += stringList(release.data[key], list_key="id") + '\t'
            elif key in ["genre", "style"]:
                s_release += stringList(release.data[key]) + '\t'
            elif key == "tracklist":
                s_release += stringList(release.data[key], list_key="tracklist") + '\t'
            else:
                s_release += str(release.data[key]) + "\t"
            # print("{}: {}".format(key, release.data[key]))
        writeEncoded(fd_releases, s_release[:-1] + "\n", encoding)


d = discogs_client.Client('ExampleApplication/0.1', user_token=MY_TOKEN)

# getReleases(d)
# printSample(d, 'release', keys=release_keys)
writeReleases(d)



