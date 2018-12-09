import io
import time
import datetime

TICK = 450
SLEEP_TIME = 120

def printSample(d, type):
    print("################################################################################")
    results = d.search('*', type=type)
    print("About " + type + "s")
    print("Count: ", results.count)
    print("Pages: ", results.pages)
    printInfo(results)

def writeResults(fd, my_list, encoding='utf-8'):
    count = 0
    for release in my_list:
        count += 1
        if count % TICK == 0:
            print("write ...{} lines".format(count))
        s = "{},{},{}\n".format(release[0], release[1], release[2])
        # print(s.encode(encoding))
        fd.write(s.encode(encoding))

def getReleases(d, encoding='utf-8'):
    results = d.search('*', type='release')
    # print(results)
    with io.open("data/releases.txt", 'wb') as fd:
        # fd = open("data/releases.txt", "w")
        count = 0
        release_list = []
        try:
            for element in results:
                count += 1
                if count % TICK == 0:
                    time.time()
                    writeResults(fd, release_list, encoding)
                    release_list = []
                    print("Get to sleep for {}s at: {}".format(SLEEP_TIME, datetime.datetime.now()))
                    time.sleep(SLEEP_TIME)
                    print("Wake up at {} ...".format(datetime.datetime.now()))
                print("read ...{} lines".format(count))
                release_list.append([element.id, element.title, element.year])
        except Exception as e:
            print("ups")
            print(e)
        finally:
            fd.close()

def printInfo(results, n=10):
    for i in range(n):
        entity = results[i]
        print(entity.tracklist)
        print(entity.data.keys())
        for key in entity.data.keys():
            if key == "tracklist":
                for track in entity.data[key]:
                    print(track)
            else:
                print("{}: {}".format(key, entity.data[key]))
        print("------------------------------------------------------------------")

def getLine(entity):
    for key in entity.data.keys():
        print("{}: {}".format(key, entity.data[key]))