import os, sys
from dotenv import load_dotenv
from google.genai import types
from google import genai

from call_functions import available_functions, call_function

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

    # First message in our list will be our request to the agent
    all_messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]),
    ]

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
    # START BOOT.DEV CODE
    # Limit the agent to 20 iterations
    for i in range(1,20):
        try:
            # Get one (or many) function calls
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=all_messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)

            if not response.function_calls:
                print(response.text)
                return response.text
            
            # Once we've generated content, append the candidates to the all_messages list
            for content in response.candidates:
                all_messages.append(content.content)

            # Let's go ahead and actually call those functions now
            function_responses = []
            if response.function_calls: # Check if there are any function calls
                print(f"LLM's proposed function call: {response.function_calls[0].name}")
                print(f"LLM's proposed arguments: {response.function_calls[0].args}")

            # Iterate through the functions list
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                
                if verbose:
                    print(f"--{function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
                #all_messages.append(function_call_result.parts[0]) # We don't want to do this yet

                # Create one consolidated tool message with all responses
                if function_responses:
                    tool_message = types.Content(role="tool", parts=function_responses)
                    all_messages.append(tool_message)


            # Do something with all those function_responses

            if not function_responses:
                raise Exception("no function responses generated, exiting.")
        except Exception as e:
            print(f"We ran into an error: {e}")
            return

        # END BOOT.DEV CODE
    return

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
            
            

        except Exception as e:
                print(f"Ran into an error: {e}")

        if response.function_calls: # Check if there are any function calls
            print(f"LLM's proposed function call: {response.function_calls[0].name}")
            print(f"LLM's proposed arguments: {response.function_calls[0].args}")

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
