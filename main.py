"""
Take two files and compare the lines that exist in the files.
The two files provided are: old_file.txt and new_file.txt.

The files have lines that look like this:
    TAG : field-list

1. Compare each file and extract shared tags
2. Save tag as dictionary to output Python list
3. Process saved tags and find omissions/additions
4. Sort output Python list according to tag name
5. Decode Python list and child objects, and send to stdout processor
6. Save output from step 5 according to output schema
"""
import os
from os import path
from models import Engine
import argparse


def argument_file_exists(*input_path):
    for file_path in input_path[0]:
        file = str(file_path)
        if os.path.isfile(file):
            print("%s exists" % file)
            pass
        else:
            print("File not found: %s" % (file))
            raise FileNotFoundError
    return True


def main():
    """Invoke Engine() class by passing in the input filepath and the directory
    will the final output file will be pushed."""
    parser = argparse.ArgumentParser(prog='Field Tag Comparator', description='Accept input directories for files.')
    parser.add_argument('string1', metavar='input file #1', type=str,
                        help='a file directory for holding the first input')
    parser.add_argument('string2', metavar='input file #2', type=str,
                        help='a file directory for holding the second input')
    args = vars(parser.parse_args())
    file_one = args['string1']
    file_two = args['string2']
    if argument_file_exists([file_one, file_two]):
        compare = Engine(file_one, file_two, r"./outputs/")
        compare.save_output()



if __name__ == "__main__":
    main()
