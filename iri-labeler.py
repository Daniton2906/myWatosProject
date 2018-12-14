import os

OLD_TYPE = "<http://example.org/Class>"
OLD_URI = "<http://>"
NEW_URI = "<https://www.discogs.com/>"
OLD_PREFIX = "ns1:"
NEW_PREFIX = "dcgs:"


def prefix_setter(line, old_prefix, new_prefix, old_uri, new_uri):
    return line.replace(old_prefix, new_prefix).replace(old_uri, new_uri)


def type_setter(line, old_prefix, new_prefix, old_type,  new_type):
    return line.replace(old_prefix, new_prefix).replace(old_type, new_type)


def save_uri(line):
    pass


def first_setter(file, old_prefix, new_prefix,old_uri, new_uri, old_type, new_type):
    with open(file, 'r', encoding='UTF-8') as ttlfile:
        ttlreader = ttlfile.readlines()
        with open(file, 'w+', encoding='UTF-8') as new_ttlfile:
            for line in ttlreader:
                if "@prefix " + old_prefix in line:
                    new_ttlfile.write(prefix_setter(line, old_prefix, new_prefix, old_uri, new_uri))
                elif (old_prefix in line) and ("<http://example.org/Class>" in line):
                    new_ttlfile.write(type_setter(line, old_prefix, new_prefix, old_type, new_type))
                elif (old_prefix in line) and ("uri" in line):
                    save_uri(line)
                    new_line = line.replace(old_prefix, new_prefix)
                    new_ttlfile.write(new_line)
                elif old_prefix in line:
                    new_line = line.replace(old_prefix, new_prefix)
                    new_ttlfile.write(new_line)
                else:
                    new_ttlfile.write(line)


def file_opener(path, old_prefix, new_prefix, old_uri, new_uri, old_type, new_type):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
    for file in files:
        first_setter(path+file, old_prefix, new_prefix, old_uri, new_uri, old_type, new_type)


if __name__ == '__main__':
    file_opener('./turtle_files/labels/', OLD_PREFIX, NEW_PREFIX, OLD_URI, NEW_URI, OLD_TYPE, "ex:Label")
    file_opener('./turtle_files/artists/', OLD_PREFIX, NEW_PREFIX, OLD_URI, NEW_URI, OLD_TYPE, "ex:Artist")
    file_opener('./turtle_files/tracks/', OLD_PREFIX, NEW_PREFIX, OLD_URI, NEW_URI, OLD_TYPE, "ex:Track")
    file_opener('./turtle_files/releases/', OLD_PREFIX, NEW_PREFIX, OLD_URI, NEW_URI, OLD_TYPE, "ex:Release")
