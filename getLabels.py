import os
import sys

import io
import time
import datetime

import discogs_client

import traceback

from discogs_client.exceptions import HTTPError

from utils import printSample

if not os.path.isdir("data"):
    os.mkdir("data")

if not os.path.exists("data/token.txt"):
    print("Agrega tu token fren ...")
    sys.exit(0)

tk = open("data/token.txt", "r")
MY_TOKEN = tk.readline()

# LABEL_KEYS = ['id', 'resource_url', 'profile', 'releases_url', 'name', 'contact_info', 'parent_label', 'uri', 'sublabels', 'urls', 'images', 'data_quality']
LABEL_KEYS = ['id', 'name', 'parent_label', 'uri', 'sublabels']

TICK = 5 # 10
SLEEP_TIME = 65

COLUMN_SEPARATOR = '\t'
LIST_SEPARATOR = ','
LINE_SEPARATOR = '\n'

def writeLabels(d, encoding='utf-8'):
    year = 2008
    visited_labels = []
    for i in range(10):
        print("Label for year " + str(year + i) + " in Chile.")
        writeInfo(d, visited_labels, str(year + i), encoding)
        nap()
    print("Total labels: " + str(len(visited_labels)))
    return len(visited_labels)


def writeEncoded(fd, s, encoding):
    fd.write(s.encode(encoding))


def nap():
    print("Get to sleep for {}s at: {}".format(SLEEP_TIME, datetime.datetime.now()))
    time.sleep(SLEEP_TIME)
    print("Wake up at {} ...".format(datetime.datetime.now()))


def writeInfo(d, visited_labels, search_year, encoding):
    # results = d.search('*', type=search_type)
    # count_results = results.count
    # print("Count: ", count_results)
    # print(results)
    with io.open("data/releases" + search_year + ".csv", 'rb') as fd_r:
        with io.open("data/labels" + search_year + ".csv", 'wb+') as fd_a:
            header_a = ""
            for column in LABEL_KEYS:
                header_a += column + COLUMN_SEPARATOR
            header_a = header_a[:-1] + LINE_SEPARATOR
            writeEncoded(fd_a, header_a, encoding)
            count = 0
            fd_r.readline()
            for line in fd_r:
                line = line.decode(encoding)
                labels = line.split(COLUMN_SEPARATOR)[2].split(LIST_SEPARATOR)
                for label_id in labels:
                    count += 1
                    written = False
                    while not written:
                        try:
                            writeResults(fd_a, d, label_id, visited_labels, encoding)
                            written = True
                        except HTTPError as e:
                            print("tranka m3n")
                            traceback.print_exc()
                            nap()
                        except Exception as e:
                            print("Otro error feo")
                            traceback.print_exc()
                            written = True
                    print("read ...{} lines".format(count))
                    if count % TICK == 0:
                        nap()
    return

def writeParentLabel(data, write):
    write(data['id'])
    return str(data['id'])


def writeSubLabels(data, write):
    s = ""
    for entity in data:
        write(entity['id'])
        s += str(entity['id']) + LIST_SEPARATOR
    # Escribir en archivo la informacion
    s = s[:-1]
    # print(s)
    return s


def writeResults(fd_labels, d, label_id, visited_labels, encoding='utf-8'):
    if label_id in visited_labels:
        return
    else:
        visited_labels.append(label_id)
    written = False
    label = None
    while not written:
        try:
            label = d.label(label_id)
            written = True
        except HTTPError as e:
            print("tranka m3n")
            traceback.print_exc()
            nap()
    # Para los lanzamientos en Chile
    s_label = ""
    # Escribir informacion de lanzamiento
    my_keys = label.data.keys()
    print(label.name)
    # print(my_keys)
    for key in LABEL_KEYS:
        # print("{}: {}".format(key, label.data[key]))
        if key not in my_keys:
            s_label += "" + '\t'
            continue
        elif key == "parent_label":
            f = lambda x: writeResults(fd_labels, d, x, visited_labels)
            s_label += writeParentLabel(label.data[key], f) + COLUMN_SEPARATOR
        elif key == "sublabels":
            f = lambda x: writeResults(fd_labels, d, x, visited_labels)
            s_label += writeSubLabels(label.data[key], f) + COLUMN_SEPARATOR
        else:
            s_label += str(label.data[key]) + COLUMN_SEPARATOR

    # print("################################################################################")
    writeEncoded(fd_labels, s_label[:-1] + LINE_SEPARATOR, encoding)


d = discogs_client.Client('ExampleApplication/0.1', user_token=MY_TOKEN)

# getReleases(d)
# printSample(d, 'release', keys=release_keys)
writeLabels(d)
