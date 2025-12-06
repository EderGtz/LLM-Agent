import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from available_functions import available_functions
from call_function import call_function
from config import LIMIT_OF_ITERATIONS_FOR_GENERATE_CONTENT

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
    number_of_iterations = 0

    while number_of_iterations < LIMIT_OF_ITERATIONS_FOR_GENERATE_CONTENT:
        number_of_iterations += 1
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=messages,
                    #model configuration parameters
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt))
        except Exception as e:
            print(f"Error calling API: {e}")
            break

        #Verifying if the model has finished 
        if not response.function_calls and response.text:
            print("Response:")
            print(response.text)
            break

        #Security validation
        if not response.usage_metadata:
            raise RuntimeError("API call request failed")

        #Adding candidates content to the messages list - This exercise
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)


        if not response.usage_metadata:
            raise RuntimeError("API call request failed")
            
        if verbose:
            print(f"--- Iteration {number_of_iterations} ---")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            
        if response.function_calls:
            function_responses_history = []

            for function_call_part in response.function_calls:
                name = function_call_part.name
                args = function_call_part.args
                print(f"Calling function: {name}({args})")

                function_call_result = call_function(function_call_part, verbose)
                
                try:
                        #If the object does not have this, the function call failed
                    test_access = function_call_result.parts[0].function_response.response
                except Exception:
                    raise RuntimeError("Fatal: call_function did not return a valid function_response object")
                
                response_part = function_call_result.parts[0]
                function_responses_history.append(response_part)

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            #Appending the function responses converted into a message into messages list
            messages.append(types.Content(role="user", parts=function_responses_history))

if __name__ == "__main__":
    main()