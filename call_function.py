from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file_content import write_file

# Configuration
WORKING_DIR = "./calculator"

# Function registry - defined once at module level
FUNCTION_REGISTRY = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

# Schema definition
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


def _create_function_response(function_name: str, response_data: dict) -> types.Content:
    """Helper to create standardized function response."""
    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=response_data,
            )
        ],
    )

def _execute_function(function_name: str, args: dict) -> dict:
    """Execute the actual function call and return result as dict."""
    if function_name not in FUNCTION_REGISTRY:
        return {"error": f"Unknown function: {function_name}"}
    
    try:
        # Add working directory to all function calls
        enhanced_args = {**args, "working_directory": WORKING_DIR}
        result = FUNCTION_REGISTRY[function_name](**enhanced_args)
        
        # Ensure result is always a dict
        return result if isinstance(result, dict) else {"result": str(result)}
        
    except Exception as e:
        return {"error": f"Function execution error: {type(e).__name__}: {e}"}

def call_function(function_call_part, verbose: bool = False) -> types.Content:
    """
    Execute a function call and return the result in the proper format for Gemini.
    
    Args:
        function_call_part: The function call part from Gemini
        verbose: Whether to print debug information
        
    Returns:
        types.Content: Formatted response for Gemini
    """
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    
    if verbose:
        print(f"Calling function: {function_name}")
        print(f"Arguments: {args}")
    
    # Execute function and get result
    result = _execute_function(function_name, args)
    
    if verbose:
        print(f"Function result: {result}")
    
    # Return formatted response
    return _create_function_response(function_name, result)