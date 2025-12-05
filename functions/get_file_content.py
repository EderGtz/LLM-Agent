import os
from google.genai import types

def get_file_content(working_directory, file_path):

    path_to_wd = os.path.abspath(working_directory)
    path_to_file = os.path.abspath(os.path.join(working_directory, file_path))

    #guardrail
    if not path_to_file.startswith(path_to_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(path_to_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    try:
        with open(path_to_file, "r") as f:
            file_content_string = f.read(MAX_CHARS+1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_content = types.FunctionDeclaration(
    name = "get_file_content",
    description="Read the content of a file at the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)
#get_file_content({'file_path': 'main.py'})