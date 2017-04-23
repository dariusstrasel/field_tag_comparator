from os import path
import os
from datetime import datetime


class IO:
    """Abstracts logic surrounding the use and manipulation of input data."""
    def __init__(self, left_file_path, right_file_path, output_file_path):
        self.LEFT_FILE_PATH = path.abspath(left_file_path)
        self.RIGHT_FILE_PATH = path.abspath(right_file_path)
        self.OUTPUT_FILE_PATH = path.abspath(output_file_path)
        self.total_omitted = 0
        self.total_added = 0
        self.file_difference = 0
        self.total_fields = 0
        self.field_changes = 0
        self.shared_tags = self.get_shared_tags()

    def get_shared_tags(self):
        """Returns a sorted list of Tag objects that pass is_shared() inspection."""
        result = []
        with open(self.LEFT_FILE_PATH, 'r') as left_file:
            for left_line in left_file:
                with open(self.RIGHT_FILE_PATH, 'r') as right_file:
                    for right_line in right_file:
                        combined_tag = Tag(left_line, right_line)
                        if combined_tag.is_shared_tag():
                            self.total_fields += len(combined_tag.left_fields)
                            self.field_changes += (
                                len(combined_tag.added_field_values) - len(combined_tag.omitted_field_values))
                            result.append(combined_tag)
        sorted_result = sorted(result, key=lambda k: k.left_tag_name)
        return sorted_result

    def save_tags_to_output(self):
        """Writes the individual Tag objects __str__ definition to an output file"""
        #print("Exporting file.")
        if not os.path.isdir(self.OUTPUT_FILE_PATH):
            os.mkdir(self.OUTPUT_FILE_PATH)
        with open(path.join(self.OUTPUT_FILE_PATH, 'output.txt'), 'w') as output_file:
            header_schema = """Date: {}, Left_File: {}, Right_File: {}, Total Shared Tags: {}, Tag Differences: {}\n"""
            header_rendered = header_schema.format(
                str(datetime.now()),
                self.RIGHT_FILE_PATH,
                self.LEFT_FILE_PATH,
                len(self.shared_tags),
                "% " + str((((self.total_fields + self.field_changes) - self.total_fields) / self.total_fields) * 100)
            )
            output_file.write(header_rendered)
            for tag in self.shared_tags:
                print(tag)
                output_file.write(str(tag))


class Tag:
    """Abstracts logic surrounding the parsing and data structure of a tag element."""
    def __init__(self, left_tag_line, right_tag_line):
        self.left_tag_name = self.extract_tag(left_tag_line)
        self.right_tag_name = self.extract_tag(right_tag_line)
        self.left_fields = self.extract_field(left_tag_line)
        self.right_fields = self.extract_field(right_tag_line)
        if self.is_shared_tag():
            self.omitted_field_values = self.get_field_omissions()
            self.added_field_values = self.get_field_additions()

    def __str__(self):
        """Used to format sane schema for stdout."""
        output_schema = """
Tag Name: {}
Left File Fields: {}
Right File Fields: {}
Fields Omitted: {}
Fields Added: {}
"""
        output_tag_name = self.left_tag_name
        output_left_fields = " ".join(self.left_fields)
        output_right_fields = " ".join(self.right_fields)
        output_omitted_field_values = " ".join(self.omitted_field_values)
        output_added_field_values = " ".join(self.added_field_values)

        output_rendered = output_schema.format(output_tag_name, output_left_fields, output_right_fields,
                                      output_omitted_field_values, output_added_field_values)

        return str(output_rendered)

    def is_shared_tag(self) -> bool:
        """Evaluates to a bool to determine if two input tags have the same name."""
        if self.left_tag_name == self.right_tag_name:
            if self.left_fields != self.right_fields:
                return True
        else:
            return False

    @staticmethod
    def extract_tag(input_line) -> str:
        """Returns the tag name by splicing an input line."""
        FIRST_CHILD = 0
        if input_line is not "":
            tag = input_line.split(":")[FIRST_CHILD]
            return tag

    @staticmethod
    def extract_field(input_line) -> list:
        """Returns the field values from an input_line."""
        SECOND_CHILD = 1
        NULL_VALUES = ('', '\n')
        if input_line not in NULL_VALUES:
            fields = input_line.split(":")[SECOND_CHILD].replace('\n', '')
            fields_delimited = fields.split(" ")
            return [field_value for field_value in fields_delimited if field_value not in NULL_VALUES]

    def get_field_omissions(self) -> list:
        """Evaluates a tag objects field omissions by comparing existing and new
        field values."""
        field_omissions = []
        for field in self.left_fields:
            if field not in self.right_fields:
                field_omissions.append(field)
        return field_omissions

    def get_field_additions(self) -> list:
        """Evaluates a tag objects field additions by comparing existing and new
                field values."""
        field_additions = []
        for field in self.right_fields:
            if field not in self.left_fields:
                field_additions.append(field)
        return field_additions


class Engine:
    """Simple abstraction used to define easy source of program manipulation."""
    def __init__(self, left_file_path, right_file_path, output_file_path):
        self.file_mapping = IO(left_file_path, right_file_path, output_file_path)

    def start(self):
        self.file_mapping.get_shared_tags()

    def save_output(self):
        self.file_mapping.save_tags_to_output()
