import sys
import object_flattening.flatten_file as flatten_file

if __name__ == '__main__':
    if len(sys.argv) == 2:
        flatten_file.flatten_json_file(sys.argv[1])
    else:
        print("Pass in a file name argument")