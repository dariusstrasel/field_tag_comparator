import models
import unittest
import os

OLD_FILE_PATH = r"./inputs/Old_File.txt"
NEW_FILE_PATH = r"./inputs/New_File.txt"
OUTPUT_FILE_PATH = r"./outputs/"

example_tag = """C_LINK:  -g -z -w -x --heap=0x800 --stack=0x400 -m link.map """

example_tag1 = """C_LINK_CMD: lnk2000 -q -c -w -x --heap=0x800 --stack=0x400 -m link.map"""
example_tag2 = """C_LINK_CMD: cl2000 -g -z -w -x --heap=0x800 --stack=0x400 -m link.map"""


class TestTagMethods(unittest.TestCase):

    def test_extract_tag(self):
        self.assertEqual(models.Tag.extract_tag(example_tag), "C_LINK")

    def test_extract_field(self):
        self.assertEqual(models.Tag.extract_field(example_tag2), ['cl2000', '-g', '-z', '-w', '-x', '--heap=0x800', '--stack=0x400', '-m', 'link.map'])

    def test_is_shared_tag(self):
        tag = models.Tag(example_tag1, example_tag2)
        self.assertEquals(tag.is_shared_tag(), True)

    def test_get_field_omissions(self):
        tag = models.Tag(example_tag1, example_tag2)
        self.assertEquals(tag.get_field_omissions(), ['lnk2000', '-q', '-c'])

    def test_get_field_additions(self):
        tag = models.Tag(example_tag1, example_tag2)
        self.assertEquals(tag.get_field_additions(), ['cl2000', '-g', '-z'])

if __name__ == '__main__':
    unittest.main()

