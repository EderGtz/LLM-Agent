from google.genai import types

from config import WORKING_DIR
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

#This function handles the call of one of the function from the LLM

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    function_args = dict(function_call_part.args)

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map = {
        "get_files_info":get_files_info,
        "get_file_content":get_file_content,
        "run_python_file":run_python_file,
        "write_file":write_file
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    function_args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**function_args)
    #The tool role is defined to identify the responses from the system to the functions
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )