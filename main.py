import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    #Storing a list of messages of the conversation as key:value. Now the 
    #conversation has a history, so the model respond within a context
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    #Response from the AI returns an object. If I want to see the
    #answer I should use the .text property
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
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
    print(f"Response: {response.text}")

if __name__ == "__main__":
    main()