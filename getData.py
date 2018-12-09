import os
import sys

import discogs_client

from utils import printSample

if not os.path.isdir("data"):
    os.mkdir("data")

if not os.path.exists("data/token.txt"):
    print("Agrega tu token fren ...")
    sys.exit(0)

tk = open("data/token.txt", "r")
MY_TOKEN = tk.readline()

release_keys = ['user_data', 'community', 'catno', 'year', 'id', 'style', 'thumb', 'title', 'label', 'master_id', 'type', 'format', 'barcode', 'master_url', 'genre', 'country', 'uri', 'cover_image', 'resource_url', 'status', 'videos', 'series', 'labels', 'artists', 'images', 'format_quantity', 'artists_sort', 'genres', 'num_for_sale', 'date_changed', 'lowest_price', 'styles', 'released_formatted', 'formats', 'estimated_weight', 'released', 'date_added', 'extraartists', 'tracklist', 'notes', 'identifiers', 'companies', 'data_quality']

d = discogs_client.Client('ExampleApplication/0.1', user_token=MY_TOKEN)

# getReleases(d)

# results = d.search('4057031', type=type)
# results = d.search('punk', type="artist")
# printInfo(results)

# print(results[0].tracklist.fetch('title'))
printSample(d, 'release')
# printSample(d, 'artist')
# printSample(d, 'master')
# printSample(d, 'label')



