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
from models import Engine


def main():
    """Invoke Engine() class by passing in the input filepath and the directory
    will the final output file will be pushed."""
    compare = Engine(r"./inputs/Old_File.txt", r"./inputs/New_File.txt", r"./outputs/")
    compare.save_output()

if __name__ == "__main__":
    main()
