import os
import csv

files = []
try:
    os.makedirs('./clean_releases')
except OSError as e:
    pass


def turn2rdflist(line):
    a = line.replace(">,", '').replace(">", '').replace('"', '').replace(" ;\r\n", '').split('<')

    track_list = "( "
    for i in range(1, len(a)):
        track_split = a[i].split(" ")[1:]
        track_name = "<" + ''.join(e + " " for e in track_split)[:-1] + "> "
        track_list += track_name
        print(track_name)
    track_list += ") ;\n"
    return a[0] + track_list


def divide_list(line):
    separated_line = line.split(' ')
    predicate = "    " + separated_line[4]
    clean_line = separated_line[5].replace('"', '').replace(" ;\r\n", '').split(',')
    list = " ("
    for i in range (0, len(clean_line)):
        quoted_name = ' "' + clean_line[i] + '" '
        list += quoted_name
    list += ") ;\n"
    return predicate + list


for (dirpath, dirnames, filenames) in os.walk('./watosProject/release'):
    files.extend(filenames)
    for file in filenames:
        with open('./watosProject/release/'+file, 'r', encoding='UTF-8', newline='') as f:
            filereader = f.readlines()
            with open('./clean_releases/' + file, 'w+', encoding='UTF-8') as f2:
                for line in filereader:
                    if "dcgs_release:tracklist" in line:
                        rdflist = turn2rdflist(line)
                        f2.write(rdflist)
                    else:
                        f2.write(line)
            f2.close()
        f.close()
