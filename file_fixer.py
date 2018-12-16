import os
import csv

def runFixer():
    files = []
    try:
        os.makedirs('./releases2')
    except OSError as e:
        pass

    for (dirpath, dirnames, filenames) in os.walk('./releases'):
        files.extend(filenames)
        for file in filenames:
            print('./releases/'+file)
            with open('./releases/'+file, 'r', encoding='UTF-8', newline='') as f:
                spamreader = csv.reader(f, delimiter='\t')
                with open('./releases2/' + file, 'w+', encoding='UTF-8') as f2:
                    spamwriter = csv.writer(f2, delimiter='\t')
                    for row in spamreader:
                        if len(row) == 5:
                            spamwriter.writerow(row)
                f2.close()
            f.close()

import glob
def joinFiles(filename, regex):
    header = False
    with open(filename, 'w', encoding='UTF-8') as f:
        for file in glob.glob(regex):
            print(file)
            with open(file, 'r', encoding='UTF-8') as f2:
                first = True
                count = 0
                for line in f2:
                    if first:
                        first = False
                        if not header:
                            header = True
                        else:
                            continue
                    count += 1
                    f.write(line)
                print("Written: " + str(count))

# joinFiles("output/releases.csv", "releases/release*.csv")
# joinFiles("output/tracks.csv", "tracks/tracks*.csv")
# joinFiles("output/labels.csv", "labels/labels*.csv")
# joinFiles("output/artists.csv", "artists/artists*.csv")