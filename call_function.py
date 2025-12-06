from google.genai import types

from config import WORKING_DIR
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

#This function handles the call of one of the function from the LLM

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    function_args = function_call_part.args

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

    try:
        if function_name == "write_file":
            function_result = write_file(WORKING_DIR,**function_args)
        elif function_name == "run_python_file":
            function_result = run_python_file(WORKING_DIR,**function_args)
        elif function_name == "get_file_content":
            function_result = get_file_content(WORKING_DIR,**function_args)
        elif function_name == "get_files_info":
            function_result = get_files_info(WORKING_DIR,**function_args)
        else:
            #If the function name is not valid
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ]
            )
    except Exception as e:
        function_result = f"Error executing tool: {e}"

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