import os
from google.genai import types

def write_file(working_directory, file_path, content):
    parent_working_dir = os.path.abspath(working_directory)
    file_to_write = os.path.normpath(os.path.join(parent_working_dir,file_path))
    if not file_to_write.startswith(parent_working_dir):
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    else:
        if not os.path.exists(os.path.dirname(file_to_write)):
            print("File path doesn't exist, creating it now")
            try:
                os.makedirs(file_path)
            except Exception as e:
                print(f"Exception: {e}")
        try:
            with open(file_to_write, "w") as file:
                    file.write(content)
            print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        except Exception as e:
            print(f"Exception: {e}")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents we want to write to file."
            )
        },
    ),
)