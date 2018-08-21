import json
import object_flattening.flattener as flattener
import os


def flatten_json_file(file_name):
    """
    Root function to call to create the directory of files of flatten objects
    :param file_name: name of target file to parse and create flatten objects from
    """
    with open(file_name) as f:
        d = json.load(f)
        json_flattener = flattener.ObjectFlattener()
        json_flattener.flatten(d)
        write_new_json_files(file_name, json_flattener.flatten_dict_list)


def write_new_json_files(file_name, dict_list):
    """
    Writes the actual files
    :param file_name: name of file for root file name
    :param dict_list: dict of file_names and their corresponding lists of flatten objects
    """
    directory = file_name.strip(".json")
    smart_directories(directory)
    for k, v in dict_list.items():
        json.dump(v, open("%s/%s.json" % (directory, k), 'w'))


def smart_directories(directory):
    """
    Creates multiple layers of folders if necessary.
    :param directory: path to extract folder names to create
    """
    path_list = directory.split("/")
    if len(path_list) == 1:
        return directory
    for i in range(1, len(path_list)+1):
        current_dictory = "/".join(path_list[:i])
        if not os.path.isdir(current_dictory):
            os.makedirs(current_dictory)
