# Field List Comparator
### Problem:
1. Take two files and compare the lines that exist in the files.
The two files provided are: old_file.txt and new_file.txt.

The files have lines that look like this:
    TAG : field-list

### Solution:
You should create an Python program that compares each tag
and for tags that match, compares each space-separated field.
The output should be a list of the tags that are in both files
and a comparison of the fields that are common, only in the old
or only in the new.

Suppress tags where there is an exact match.

### For example, given the two lines:
````
   C_LINK_CMD: lnk2000 -q -c -w -x --heap=0x800 --stack=0x400 -m link.map
   
   C_LINK_CMD: cl2000 -g -z -w -x --heap=0x800 --stack=0x400 -m link.map
````

Your output should look like this:
````
Tag Name: C_LINK_CMD
   
Existing Values:  lnk2000 -q -c -w -x --heap=0x800 --stack=0x400 -m link.map
   
New Values:  cl2000 -g -z -w -x --heap=0x800 --stack=0x400 -m link.map
   
Fields Ommitted: lnk2000 -q -c 
   
Fields Added: cl2000 -g -z 
````
   
### Please sort the output by tag name

# How to run:
1. Clone repo
2. Ensure Python 3+ is installed
3. run main.py as follows:


- MacOS / Linux
```bash
python3 main.py inputs/Old_File.txt inputs/Old_File.txt
```

- Windows
```bash
python main.py inputs/Old_File.txt inputs/Old_File.txt
```

3a. You may also pass in different input files by modifying the first and second CLI arguments to refer to a different file.
