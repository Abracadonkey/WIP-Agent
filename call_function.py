from ast import arguments
from operator import imod
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from google.genai import types # type: ignore

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content 
from functions.run_python_file import schema_run_python_file 
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content
    ]
)

function_call_dict = {
    "get_files_info": get_files_info, 
    "write_file": write_file, 
    "run_python_file": run_python_file, 
    "get_file_content": get_file_content, 
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    arguments = function_call_part.args
    arguments["working_directory"] = "./calculator"
    
    chosen_function =  function_call_dict.get(function_name) 
    if not chosen_function:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
             )
        ],
    )

    
    
    
    if verbose == True:
        print(f"Calling function: {function_name}({arguments})") 
    if verbose == False:
        print(f" - Calling function: {function_name}")  
    try:
        function_result = chosen_function(**arguments) 
    except TypeError as e: 
        print(f"Error calling '{function_name}': {e}") 
        raise


      
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result}, 
        )
    ],
)