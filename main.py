#!/usr/bin/python3

"""
Take two files and compare the lines that exist in the files.
The two files provided are: old_file.txt and new_file.txt.

The files have lines that look like this:
    TAG : field-list

1. Compare each file and extract shared tags
1a. Make note of fields which are shared but unchanged.
2. Save tag as dictionary to output Python list
3. Process saved tags and find omissions/additions
4. Sort output Python list according to tag name
5. Decode Python list and child objects, and send to stdout processor
6. Save output from step 5 according to output schema
"""
from os import path


OLD_FILE_PATH = path.abspath(r"./inputs/Old_File.txt")
NEW_FILE_PATH = path.abspath(r"./inputs/New_File.txt")
OUTPUT_FILE_PATH = path.abspath(r"./outputs/")

example_tag = """C_ALT_COMPILE_CMD:  -c -g -q"""


def extract_tag(input_line):
    pass

def extract_fields(input_line):
    pass

print(OLD_FILE_PATH)


