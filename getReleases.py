import os
import sys

import io
import time
import datetime

import discogs_client

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
                'uri',
                'title',
                'labels',
                'master_id',
                'country',
                'year',
                'released',
                'genres',
                'styles',
                'artists',
                'tracklist']

track_keys = ['position', 'title', 'duration', 'artists']

TICK = 5 # 450
SLEEP_TIME = 1 # 120

def writeReleases(d, encoding='utf-8'):
    results = d.search('*', type='release', country="chile|Chile")
    print("Count: ", results.count)
    # print(results)
    with io.open("data/releases.csv", 'wb') as fd_r:
        header = ""

        with io.open("data/tracks.csv", 'wb+') as fd_t:
            # fd = open("data/releases.csv", "w")
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
            finally:
                fd_t.close()
                fd_r.close()


def writeResults(fd_releases, fd_tracks, release, encoding='utf-8'):
    if release.country.lower() == "chile":
        for track in release.tracklist:
            s_artists = ""
            print(track.artists)
            for artist in track.artists:
                s_artists += str(artist.id) + ","
            s_tracks = "{}\t{}\t{}\t{}\t{}\n".format(release.id, track.title, track.position, track.duration, s_artists[:-1])
            fd_tracks.write(s_tracks.encode(encoding))
        s_release = ""
        for key in release_keys:
            print("{}: {}".format(key, release.data[key]))
        # print(release.data.keys())
        #s = "{}\t{}\t{}\t{}\n".format(release.country, release.id, release.title, release.tracklist)
        #print(s)
    # print(s.encode(encoding))
    # fd.write(s.encode(encoding))


d = discogs_client.Client('ExampleApplication/0.1', user_token=MY_TOKEN)

# getReleases(d)
# printSample(d, 'release', keys=release_keys)
writeReleases(d)



