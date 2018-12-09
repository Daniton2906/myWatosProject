
def printSample(d, type, keys=None):
    print("################################################################################")
    results = d.search('*', type=type)
    print("About " + type + "s")
    print("Count: ", results.count)
    print("Pages: ", results.pages)
    printInfo(results, keys=keys)

def printInfo(results, n=10, keys=None):
    for i in range(n):
        entity = results[i]
        print(entity.tracklist)
        print(entity.data.keys())
        for key in entity.data.keys():
            if keys != None and key not in keys:
                continue
            if key == "tracklist":
                for track in entity.data[key]:
                    print(track)
            else:
                print("{}: {}".format(key, entity.data[key]))
        print("------------------------------------------------------------------")

def getLine(entity):
    for key in entity.data.keys():
        print("{}: {}".format(key, entity.data[key]))