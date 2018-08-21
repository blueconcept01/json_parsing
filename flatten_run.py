import sys
import object_flattening.flatten_file as flatten_file

if __name__ == '__main__':
    flatten_file.flatten_json_file(sys.argv[1])
