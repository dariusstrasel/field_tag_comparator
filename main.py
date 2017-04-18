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
from models import Engine

OLD_FILE_PATH = path.abspath(r"./inputs/Old_File.txt")
NEW_FILE_PATH = path.abspath(r"./inputs/New_File.txt")
OUTPUT_FILE_PATH = path.abspath(r"./outputs/")

example_tag = """C_LINK_CMD:  -g -z -w -x --heap=0x800 --stack=0x400 -m link.map """

example_tag1 = """C_LINK_CMD: lnk2000 -q -c -w -x --heap=0x800 --stack=0x400 -m link.map"""
example_tag2 = """C_LINK_CMD: cl2000 -g -z -w -x --heap=0x800 --stack=0x400 -m link.map"""


def main():
    compare = Engine(r"./inputs/Old_File.txt", r"./inputs/New_File.txt", r"./outputs/")
    # compare.start()
    compare.save_output()

if __name__ == "__main__":
    main()

# TODO: Hook up all the functions
# TODO: change output_results_to_stdout() to use input as list
# TODO: finish pass_input_to_output()
# TODO: refactor get_shared_tags() to be DRY
# TODO: Add Tag class?
