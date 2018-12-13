import os
import csv

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
