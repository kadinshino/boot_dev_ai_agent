import os
from .config import FILE_CONTENT_LENGTH_LIMIT

def get_file_content(working_directory, file_path):
    try:
        # Ensure the file path is within the working directory
        absolute_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(absolute_working_dir, file_path))

        # Fix the path check to allow files directly in the working directory
        if not (absolute_file_path.startswith(absolute_working_dir + os.sep) or 
                absolute_file_path == absolute_working_dir or
                os.path.dirname(absolute_file_path) == absolute_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the path is a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file content
        with open(absolute_file_path, 'r') as file:
            content = file.read()

        # Truncate the content if it exceeds the limit
        if len(content) > FILE_CONTENT_LENGTH_LIMIT:
            truncated_content = content[:FILE_CONTENT_LENGTH_LIMIT] + f'[...File "{file_path}" truncated at {FILE_CONTENT_LENGTH_LIMIT} characters]'
            return truncated_content

        return content

    except Exception as e:
        return f'Error: {e}'