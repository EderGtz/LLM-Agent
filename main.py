import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions

def main():

    #Module for analyzing an user input at the cmd
    parser = argparse.ArgumentParser(description = "AI Code Assistant")
    parser.add_argument("prompt",type=str,help="The user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #read the key-value pairs from the .env file and set them
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    #Using --verbose flag
    if args.verbose:
        print(f'User prompt: {args.prompt}\n')

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        #model configuration parameters
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt))

    if not response.usage_metadata:
        raise RuntimeError("API call request failed")
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

if __name__ == "__main__":
    main()