import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    parent_working_dir = os.path.abspath(working_directory)
    file_to_run = os.path.normpath(os.path.join(parent_working_dir,file_path))
    if not file_to_run.startswith(parent_working_dir):
        print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    elif not os.path.isfile(file_to_run):
        print(f'Error: File "{file_path}" not found.')
    elif os.name.endswith(".py"):
        print(f'Error: "{file_path}" is not a Python file.')
    else:
        stdout = None
        stderr = None
        try:
            result = subprocess.run(['python',file_to_run],timeout=30,cwd=parent_working_dir,capture_output=True)
            print(f"STDOUT:{result.stdout}")
            print(f"STDERR:{result.stderr}")
            if result.returncode != 0:
                print(f"Process exited with code {result.returncode}")
            else:
                print(f"No output produced")
        except Exception as e:
            f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run.",
            ),
        },
    ),
)