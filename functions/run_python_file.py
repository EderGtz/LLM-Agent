import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    path_to_wd = os.path.abspath(working_directory)
    path_to_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not path_to_file.startswith(path_to_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.exists(path_to_file) is False:
        return f'Error: File "{file_path}" not found.'
    
    if path_to_file.endswith(".py") is False:
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        args_new = ["python3",path_to_file] + args
        result = subprocess.run(
            args_new,
            cwd=path_to_wd,
            timeout=30,
            capture_output=True,
            text=True)
        
        if not result.stdout and not result.stderr:
            return "No output produced"
        
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"

        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description="Executes a Python script at the specified path within the working directory. Returns the STDOUT and STDERR output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of command line arguments to pass to the script."
            ),
        },
        required=["file_path"]
    ),
)

#run_python_file({'file_path': 'main.py'})