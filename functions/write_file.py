import os
from google.genai import types

def write_file(working_directory, file_path, content):

    path_to_wd = os.path.abspath(working_directory)
    path_to_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not path_to_file.startswith(path_to_wd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(path_to_file, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description="Writes over a file in the specified path, constrained to the working directory. If the file does not exist, it is created. Returns the number of characters written",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            ),
        },
        required=["file_path"]
    ), 
)
#write_file({'file_path': 'main.txt', 'content': 'hello'})