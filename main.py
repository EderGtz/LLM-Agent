import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from system_prompt import system_prompt
from functions.get_files_info import schema_get_files_info

#read the key-value pairs from the .env file and set them in the environment
load_dotenv()

def main():

    #Reading the API key and connecting to Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #Module for analyzing an user input at the cmd
    parser = argparse.ArgumentParser(
        description = "Send the text to Gemini AI") #What the program does
    parser.add_argument("prompt",type=str,help="The user prompt")
    #Optional cm argument. store_true means the argument is parsed as True
    # if the flag is set. Otherwise is False
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    #Tool details of a tool that the model may use to generate a response.
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info],
)

    #Storing a list of messages of the conversation as key:value. Now the 
    #conversation has a history, so the model respond within a context
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    #Response from the AI returns an object. If I want to see the
    #answer I should use the .text property
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        #model configuration parameters
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )

    #Keeping track of tokens usage
    if response.usage_metadata is None:
        raise RuntimeError("API call request failed")
    
    #Using --verbose flag
    if args.verbose:
        print(f'''
        User prompt: {args.prompt}
        Prompt tokens: {response.usage_metadata.prompt_token_count}
        Response tokens: {response.usage_metadata.candidates_token_count}
''')
    print(f"Response: {response.function_calls}")

    #list of function calls in the response
    #if is not empty, it is a list
    if response.function_calls is not None:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")

if __name__ == "__main__":
    main()