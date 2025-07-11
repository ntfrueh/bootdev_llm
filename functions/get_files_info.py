# from pathlib import Path
import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    parent_working_dir = os.path.abspath(working_directory)
    directory_to_check = os.path.normpath(os.path.join(parent_working_dir,directory))
    if not directory_to_check.startswith(parent_working_dir):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    elif not os.path.isdir(directory_to_check):
        print(f'Error: "{directory}" is not a directory')
    else:
        file_list = os.listdir(directory_to_check)
        formatted_file_data_list = []
        for file in file_list:
            current_file = os.path.join(directory_to_check,file)
            # print(current_file)
            formatted_file_data_list.append(f"- {file}: file_size={os.path.getsize(current_file)} bytes, is_dir={os.path.isdir(current_file)}")
        print('\n'.join(formatted_file_data_list))
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)