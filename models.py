from os import path
import os
from datetime import datetime


class IO:
    """Abstracts logic surrounding the use and manipulation of input data."""
    def __init__(self, old_file_path, new_file_path, output_file_path):
        self.OLD_FILE_PATH = path.abspath(old_file_path)
        self.NEW_FILE_PATH = path.abspath(new_file_path)
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
        with open(self.OLD_FILE_PATH, 'r') as old_file:
            for old_line in old_file:
                with open(self.NEW_FILE_PATH, 'r') as new_file:
                    for new_line in new_file:
                        current_tag = Tag(old_line, new_line)
                        if current_tag.is_shared_tag():
                            self.total_fields += len(current_tag.existing_field_value)
                            self.field_changes += (
                                len(current_tag.added_field_values) - len(current_tag.omitted_field_values))
                            result.append(current_tag)
        sorted_result = sorted(result, key=lambda k: k.left_tag_name)
        return sorted_result

    def save_tags_to_output(self):
        """Writes the individual Tag objects __str__ definition to an output file"""
        #print("Exporting file.")
        if not os.path.isdir(self.OUTPUT_FILE_PATH):
            os.mkdir(self.OUTPUT_FILE_PATH)
        with open(path.join(self.OUTPUT_FILE_PATH, 'output.txt'), 'w') as output_file:
            header_schema = """Date: {}, New_File: {}, Old_File: {}, Total Shared Tags: {}, Tag Differences: {}\n"""
            header_output = header_schema.format(
                str(datetime.now()),
                self.NEW_FILE_PATH,
                self.OLD_FILE_PATH,
                len(self.shared_tags),
                "% " + str((((self.total_fields + self.field_changes) - self.total_fields) / self.total_fields) * 100)
            )
            output_file.write(header_output)
            for tag in self.shared_tags:
                print(tag)
                output_file.write(str(tag))


class Tag:
    """Abstracts logic surrounding the parsing and data structure of a tag element."""
    def __init__(self, left_tag_line, right_tag_line):
        self.left_tag_name = self.extract_tag(left_tag_line)
        self.right_tag_name = self.extract_tag(right_tag_line)
        self.existing_field_value = self.extract_field(left_tag_line)
        self.new_field_value = self.extract_field(right_tag_line)
        if self.is_shared_tag():
            self.omitted_field_values = self.get_field_omissions()
            self.added_field_values = self.get_field_additions()

    def __str__(self):
        """Used to format sane schema for stdout."""
        output_schema = """
Tag Name: {}
Existing Values: {}
New Values: {}
Fields Omitted: {}
Fields Added: {}
"""
        output_tag_name = self.left_tag_name
        output_existing_field_value = " ".join(self.existing_field_value)
        output_new_field_value = " ".join(self.new_field_value)
        output_omitted_field_values = " ".join(self.omitted_field_values)
        output_added_field_values = " ".join(self.added_field_values)

        output = output_schema.format(output_tag_name, output_existing_field_value, output_new_field_value,
                                      output_omitted_field_values, output_added_field_values)

        return str(output)

    def is_shared_tag(self) -> bool:
        """Evaluates a bool to determine if two input tags have the same name."""
        if self.left_tag_name == self.right_tag_name:
            if self.existing_field_value != self.new_field_value:
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
        result = []
        for field in self.existing_field_value:
            if field not in self.new_field_value:
                result.append(field)
        return result

    def get_field_additions(self) -> list:
        """Evaluates a tag objects field additions by comparing existing and new
                field values."""
        result = []
        for field in self.new_field_value:
            if field not in self.existing_field_value:
                result.append(field)
        return result


class Engine:
    """Simple abstraction used to define easy source of program manipulation."""
    def __init__(self, old_file_path, new_file_path, output_file_path):
        self.input_output = IO(old_file_path, new_file_path, output_file_path)

    def start(self):
        self.input_output.get_shared_tags()

    def save_output(self):
        self.input_output.save_tags_to_output()
