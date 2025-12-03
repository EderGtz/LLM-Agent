import os
import argparse
from dotenv import load_dotenv
from google import genai

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
    args = parser.parse_args()

    #Response from the AI returns an object. If I want to see the
    #answer I should use the .text property
    contents = args.prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=contents
    )

    #Keeping track of tokens usage
    if response.usage_metadata == None:
        raise RuntimeError("API call request failed")

    print(f"""User prompt: {contents}
    Prompt tokens: {response.usage_metadata.prompt_token_count}
    Response tokens: {response.usage_metadata.candidates_token_count}
    Response:
    {response.text}
""")


if __name__ == "__main__":
    main()