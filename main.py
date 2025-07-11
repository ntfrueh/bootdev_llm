import os
import sys
from dotenv import load_dotenv
from google.genai import types
from google import genai

from call_functions import available_functions, call_function

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # test_part = types.Part.from_text(text="This is a test string.")
    # print(test_part) # You can print it to see if it works

    all_messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]),
    ]
    # input_prompt = types.Content(
    #             role="user",
    #             parts=[
    #                 types.Part.from_text(text=sys.argv[1])
    #             ]
    #         )

    # all_messages = [input_prompt]

    generate_content(client, all_messages, verbose=None)


def generate_content(client, all_messages, verbose):

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    # Limit the agent to 20 messages
    for i in range(1,20):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=all_messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt)
            )
            
            # Check the response candidates and add the .content to the message list
            for content in response.candidates:
                all_messages.append(content.content)

        except Exception as e:
                print(f"Ran into an error: {e}")

        if None != response.function_calls:
            # Simple testing output
            # print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
            response = call_function(response.function_calls[0])

            all_messages.append(response)

        else:
            print(response.text)
            break

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
