from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file_content import write_file

# Define working directory directly
WORKING_DIR = "./calculator"

# Define the schemas directly here
available_functions = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_files_info",
            description="List files and directories under a given relative path.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "directory": types.Schema(
                        type=types.Type.STRING,
                        description="Relative path to list (e.g., '.', 'pkg', 'src/utils')"
                    )
                },
                required=["directory"]
            )
        ),
        types.FunctionDeclaration(
            name="get_file_content",
            description="Read the contents of a specified file.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to the file"
                    )
                },
                required=["file_path"]
            )
        ),
        types.FunctionDeclaration(
            name="run_python_file",
            description="Execute a specified Python file with optional arguments.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to the Python file"
                    ),
                    "arguments": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                        description="Optional arguments for the Python script"
                    )
                },
                required=["file_path"]
            )
        ),
        types.FunctionDeclaration(
            name="write_file",
            description="Write or overwrite a specified file with given content.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to the file"
                    ),
                    "content": types.Schema(
                        type=types.Type.STRING,
                        description="Content to write into the file"
                    )
                },
                required=["file_path", "content"]
            )
        )
    ]
)

def call_function(function_call_part, verbose=False):
    """
    Execute a function call and return the result in the proper format for Gemini.
    """
    from google.genai import types

    from functions.get_files_info import get_files_info
    from functions.get_file_content import get_file_content
    from functions.run_python import run_python_file
    from functions.write_file_content import write_file

    # Assume WORKING_DIR is defined at top of your file

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call_part.name

    # FIX 1: Always return a dict on "function not found"
    if function_name not in function_map:
        error_result = {"error": f"Unknown function: {function_name}"}
        if verbose:
            print(f"Error: {error_result['error']}")
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response=error_result,  # Now ALWAYS a dict
                )
            ],
        )

    try:
        args = dict(function_call_part.args)
        args["working_directory"] = WORKING_DIR

        if verbose:
            print(f"Final args passed to function: {args}")

        function_result = function_map[function_name](**args)

        if verbose:
            print(f"Function returned: {function_result}")

        # FIX 2: Always return a dict
        if isinstance(function_result, dict):
            result_response = function_result
        else:
            result_response = {"result": str(function_result)}

        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response=result_response,  # Always a dict
                )
            ],
        )

    except Exception as e:
        # FIX 3: Always return a dict on errors
        error_result = {"error": f"Function execution error: {type(e).__name__}: {e}"}
        if verbose:
            print(f"Error executing function: {error_result['error']}")
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response=error_result,  # Always a dict
                )
            ],
        )

# """
# Clean and modular function handler for Google GenAI tool integration.
# """

# from google.genai import types
# from typing import Dict, Any, Optional, List

# # Import your function modules
# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content
# from functions.run_python import run_python_file
# from functions.write_file_content import write_file


# class FunctionHandler:
#     """Handles function calls and schema definitions for Google GenAI tools."""
    
#     def __init__(self, working_dir: str = "./calculator"):
#         self.working_dir = working_dir
#         self.function_map = {
#             "get_files_info": get_files_info,
#             "get_file_content": get_file_content,
#             "run_python_file": run_python_file,
#             "write_file": write_file,
#         }
    
#     @property
#     def available_functions(self) -> types.Tool:
#         """Define the function schemas for Google GenAI."""
#         return types.Tool(
#             function_declarations=[
#                 self._create_get_files_info_schema(),
#                 self._create_get_file_content_schema(),
#                 self._create_run_python_file_schema(),
#                 self._create_write_file_schema(),
#             ]
#         )
    
#     def _create_get_files_info_schema(self) -> types.FunctionDeclaration:
#         """Schema for listing files and directories."""
#         return types.FunctionDeclaration(
#             name="get_files_info",
#             description="List files and directories under a given relative path.",
#             parameters=types.Schema(
#                 type=types.Type.OBJECT,
#                 properties={
#                     "directory": types.Schema(
#                         type=types.Type.STRING,
#                         description="Relative path to list (e.g., '.', 'pkg', 'src/utils')"
#                     )
#                 },
#                 required=["directory"]
#             )
#         )
    
#     def _create_get_file_content_schema(self) -> types.FunctionDeclaration:
#         """Schema for reading file contents."""
#         return types.FunctionDeclaration(
#             name="get_file_content",
#             description="Read the contents of a specified file.",
#             parameters=types.Schema(
#                 type=types.Type.OBJECT,
#                 properties={
#                     "file_path": types.Schema(
#                         type=types.Type.STRING,
#                         description="Path to the file"
#                     )
#                 },
#                 required=["file_path"]
#             )
#         )
    
#     def _create_run_python_file_schema(self) -> types.FunctionDeclaration:
#         """Schema for executing Python files."""
#         return types.FunctionDeclaration(
#             name="run_python_file",
#             description="Execute a specified Python file with optional arguments.",
#             parameters=types.Schema(
#                 type=types.Type.OBJECT,
#                 properties={
#                     "file_path": types.Schema(
#                         type=types.Type.STRING,
#                         description="Path to the Python file"
#                     ),
#                     "arguments": types.Schema(
#                         type=types.Type.ARRAY,
#                         items=types.Schema(type=types.Type.STRING),
#                         description="Optional arguments for the Python script"
#                     )
#                 },
#                 required=["file_path"]
#             )
#         )
    
#     def _create_write_file_schema(self) -> types.FunctionDeclaration:
#         """Schema for writing files."""
#         return types.FunctionDeclaration(
#             name="write_file",
#             description="Write or overwrite a specified file with given content.",
#             parameters=types.Schema(
#                 type=types.Type.OBJECT,
#                 properties={
#                     "file_path": types.Schema(
#                         type=types.Type.STRING,
#                         description="Path to the file"
#                     ),
#                     "content": types.Schema(
#                         type=types.Type.STRING,
#                         description="Content to write into the file"
#                     )
#                 },
#                 required=["file_path", "content"]
#             )
#         )
    
#     def call_function(self, function_call_part, verbose: bool = False) -> types.Content:
#         """
#         Execute a function call and return the result in the proper format for Gemini.
        
#         Args:
#             function_call_part: The function call part from Gemini
#             verbose: Whether to print debug information
            
#         Returns:
#             types.Content: Formatted response for Gemini
#         """
#         function_name = function_call_part.name
        
#         # Check if function exists
#         if function_name not in self.function_map:
#             return self._create_error_response(
#                 function_name, 
#                 f"Unknown function: {function_name}",
#                 verbose
#             )
        
#         try:
#             # Prepare function arguments
#             args = dict(function_call_part.args)
#             args["working_directory"] = self.working_dir
            
#             if verbose:
#                 print(f"Calling {function_name} with args: {args}")
            
#             # Execute the function
#             function_result = self.function_map[function_name](**args)
            
#             if verbose:
#                 print(f"Function {function_name} returned: {function_result}")
            
#             # Ensure result is a dictionary
#             result_response = self._normalize_result(function_result)
            
#             return self._create_success_response(function_name, result_response)
            
#         except Exception as e:
#             error_msg = f"Function execution error: {type(e).__name__}: {e}"
#             return self._create_error_response(function_name, error_msg, verbose)
    
#     def _normalize_result(self, result: Any) -> Dict[str, Any]:
#         """Ensure the result is always a dictionary."""
#         if isinstance(result, dict):
#             return result
#         return {"result": str(result)}
    
#     def _create_success_response(self, function_name: str, response: Dict[str, Any]) -> types.Content:
#         """Create a successful function response."""
#         return types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_function_response(
#                     name=function_name,
#                     response=response,
#                 )
#             ],
#         )
    
#     def _create_error_response(self, function_name: str, error_msg: str, verbose: bool = False) -> types.Content:
#         """Create an error function response."""
#         error_result = {"error": error_msg}
        
#         if verbose:
#             print(f"Error: {error_msg}")
        
#         return types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_function_response(
#                     name=function_name,
#                     response=error_result,
#                 )
#             ],
#         )
    
#     def add_function(self, name: str, function_callable, schema: types.FunctionDeclaration):
#         """
#         Add a new function to the handler.
        
#         Args:
#             name: Function name
#             function_callable: The actual function to call
#             schema: The function schema for Gemini
#         """
#         self.function_map[name] = function_callable
#         # Note: You'll need to recreate the available_functions property 
#         # or modify it to be dynamic if you want runtime function addition

# # Usage example:
# def main():
#     """Example usage of the FunctionHandler."""
#     handler = FunctionHandler(working_dir="./calculator")
    
#     # Get the available functions for Gemini
#     available_functions = handler.available_functions
    
#     # Example of calling a function (this would normally come from Gemini)
#     # function_call_result = handler.call_function(function_call_part, verbose=True)
    
#     return handler, available_functions


# if __name__ == "__main__":
#     handler, functions = main()
#     print("Function handler initialized successfully!")