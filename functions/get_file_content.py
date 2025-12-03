import os

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