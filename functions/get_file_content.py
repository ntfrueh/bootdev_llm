import os
from google.genai import types

def get_file_content(working_directory, file_path):
    parent_working_dir = os.path.abspath(working_directory)
    file_to_check = os.path.normpath(os.path.join(parent_working_dir,file_path))
    if not file_to_check.startswith(parent_working_dir):
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    elif not os.path.isfile(file_to_check):
        print(f'Error: File not found or is not a regular file: "{file_path}"')
    else:
        try:
            MAX_CHARS = 10000
            with open(file_to_check, 'r') as file:
                content = file.read(MAX_CHARS)
            if len(content) == 10000:
                content = content + f'[...File "{file_path}" truncated at 10000 characters]'
            print(content)
        except Exception as e:
            print(f"Error: {e}")

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets contents of file in the specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to analyze, relative to the working directory.",
            ),
        },
    ),
)