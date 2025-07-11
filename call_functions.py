import os
import sys
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content,
    ]
)


# def call_function(function_call_part, verbose=False):
    
#     # Compile a list of all possible functions a user can call...this doesn't seem ideal
#     available_functions = {
#         "get_files_info" : schema_get_files_info,
#         "get_file_content" : schema_get_file_content,
#         "run_python_file" : schema_run_python_file,
#         "write_file" : schema_write_file
#     }

#     if verbose:
#         print(f"Calling function: {function_call_part.name}({function_call_part.args})")
#     else:
#         print(f" - Calling function: {function_call_part.name}")

#     # Attempt to actually run the chosen function
#     # working_directory = "./calculator"
#     function_call_part.args["working_directory"] = "./calculator"
#     try:

#         if function_call_part.name in available_functions:
#             function_result = available_functions[function_call_part.name](**function_call_part.args)
#         # After each function call, use the types.Content function
#         # to convert the function_responses into a message
#         # with a role of `tool`
#         return types.Content(
#             role="tool",
#             parts=[
#                 types.Part.from_function_response(
#                     name=function_call_part.name,
#                     response={"result": function_result},
#                 )
#             ],
#         )
#     except Exception as e:
#         return types.Content(
#             role="tool",
#             parts=[
#                 types.Part.from_function_response(
#                     name=function_call_part.name,
#                     response={"error": f"Unknown function: {function_call_part.name}"},
#                 )
#             ],
#         )
    

def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )