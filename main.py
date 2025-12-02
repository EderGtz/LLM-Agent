import os
from dotenv import load_dotenv
from google import genai

#Reading the API key and connecting to Gemini
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#Response from the AI returns an object. If I want to see the
#answer I should use the .text property
contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(
    model='gemini-2.5-flash', contents=contents
)

def main():
    print(f"This is the content:\n{contents}\nThis is the response:\n")
    print(response.parts)


if __name__ == "__main__":
    main()

