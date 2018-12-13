import os
import csv

files = []
try:
    os.makedirs('./turtle_files2')
except OSError as e:
    pass


def turn2rdflist(line):
    a = line.replace(">,", '').replace(">", '').replace('"', '').replace(" ;\n", '').split('<')

    track_list = "( "
    for i in range(1, len(a)):
        track_split = a[i].split(" ")[1:]
        track_name = "<" + ''.join(e + " " for e in track_split)[:-1] + "> "
        track_list += track_name
    track_list += ") ;\n"
    return a[0] + track_list




for (dirpath, dirnames, filenames) in os.walk('./turtle_files'):
    files.extend(filenames)
    for file in filenames:
        with open('./turtle_files/'+file, 'r', encoding='UTF-8', newline='') as f:
            filereader = f.readlines()
            with open('./turtle_files2/' + file, 'w+', encoding='UTF-8') as f2:
                for line in filereader:
                    if "ns1:tracklist" in line:
                        rdflist = turn2rdflist(line)
                        f2.write(rdflist)
                    else:
                        f2.write(line)
            f2.close()
        f.close()
