from google.genai import types

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

    try:
        if function_name == "write_file":
            function_result = write_file("./calculator",**function_args)
        elif function_name == "run_python_file":
            function_result = run_python_file("./calculator",**function_args)
        elif function_name == "get_file_content":
            function_result = get_file_content("./calculator",**function_args)
        elif function_name == "get_files_info":
            function_result = get_files_info("./calculator",**function_args)
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

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )