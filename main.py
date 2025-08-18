import sys
import shutil
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import call_function, available_functions

# Constants
MODEL_NAME = "gemini-2.0-flash-001"
ENV_API_KEY = "GEMINI_API_KEY"
VERBOSE_FLAG = "--verbose"

# Messages
USAGE_MESSAGE = """AI Code Assistant

Usage: python main.py "your prompt here" [--verbose]
Example: python main.py "How do I fix the calculator?"
"""

ERROR_MESSAGES = {
    "no_prompt": "No prompt provided. Use --help for usage information.",
    "no_api_key": f"API key not found. Please set {ENV_API_KEY} environment variable.",
    "empty_function_result": "Empty function call result received.",
    "final_response_error": "Function executed successfully but couldn't generate final response.",
    "max_iterations": "Maximum iterations reached without final response."
}


class AIAssistant:
    """Main AI Assistant class handling Gemini API interactions."""
    
    def __init__(self, api_key: str, verbose: bool = False):
        self.client = genai.Client(api_key=api_key)
        self.verbose = verbose
        self.messages = []
    
    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def _create_config(self) -> types.GenerateContentConfig:
        """Create generation configuration."""
        return types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        )
    
    def _handle_function_calls(self, response) -> None:
        """Process function calls and add responses to message history."""
        for function_call_part in response.function_calls:
            # CHANGE 1: Add dash prefix to match required output format
            print(f"- Calling function: {function_call_part.name}")
            
            # Execute the function call
            function_result = call_function(function_call_part, self.verbose)
            
            if not function_result.parts or not function_result.parts[0].function_response:
                raise Exception(ERROR_MESSAGES["empty_function_result"])
            
            # Extract the actual result for logging
            response_data = function_result.parts[0].function_response.response
            self._log(f"-> {response_data}")
            
            # CRITICAL FIX: Append function result as user message with correct format
            # This was the bug - I was appending function_result directly instead of wrapping it properly
            self.messages.append(types.Content(role="user", parts=[function_result.parts[0]]))
    
    def _log_usage(self, response) -> None:
        """Log token usage information."""
        if self.verbose and hasattr(response, 'usage_metadata'):
            self._log(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            self._log(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    def generate_response(self, user_prompt: str) -> str:
        """Generate response for user prompt, handling function calls if needed."""
        self._log(f"User prompt: {user_prompt}\n")
        
        # Initialize conversation with user prompt
        self.messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
        ]
        
        max_iterations = 20
        iteration_count = 0
        
        while iteration_count < max_iterations:
            self._log(f"Iteration {iteration_count + 1}")
            
            try:
                response = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=self.messages,
                    config=self._create_config()
                )
                
                self._log_usage(response)
                
                # Check if we have a valid response
                if not response.candidates or len(response.candidates) == 0:
                    raise Exception("No candidates returned from API")
                
                # CRITICAL: Add ALL candidates to messages list after EVERY generate_content call
                for candidate in response.candidates:
                    self.messages.append(candidate.content)
                
                # Check if there are function calls to handle
                if response.function_calls:
                    self._log("Function calls detected, processing...")
                    self._handle_function_calls(response)
                else:
                    # No function calls - check if this might be a final response
                    candidate = response.candidates[0]
                    if candidate.content and candidate.content.parts:
                        final_text = ""
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                final_text += part.text
                        
                        self._log(f"LLM response (no function calls): {final_text[:100]}...")
                        
                        # CHANGE 3: Return immediately when we have any text response
                        if final_text.strip():
                            return final_text.strip()
                
            except Exception as e:
                self._log(f"Error in iteration {iteration_count + 1}: {e}")
                if iteration_count == 0:
                    # If first iteration fails, re-raise the error
                    raise
                else:
                    # For later iterations, try to continue or break
                    break
            
            iteration_count += 1
        
        # If we hit max iterations, return the last response we got
        if self.messages and len(self.messages) > 1:
            last_message = self.messages[-1]
            if last_message.parts:
                final_text = ""
                for part in last_message.parts:
                    if hasattr(part, 'text') and part.text:
                        final_text += part.text
                if final_text.strip():
                    self._log("Returning final response after max iterations")
                    return final_text.strip()
        
        # Fallback
        raise Exception(ERROR_MESSAGES["max_iterations"])

def parse_arguments() -> tuple[list[str], bool]:
    """Parse command line arguments and return prompt args and verbose flag."""
    verbose = VERBOSE_FLAG in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    return args, verbose

def validate_environment() -> str:
    """Validate environment and return API key."""
    api_key = os.environ.get(ENV_API_KEY)
    if not api_key:
        raise ValueError(ERROR_MESSAGES["no_api_key"])
    return api_key

def clean_pycache():
    """Clean up Python cache directories."""
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)

def main():
    """Main entry point."""
    load_dotenv()
    
    # Parse arguments
    args, verbose = parse_arguments()
    
    if not args:
        print(USAGE_MESSAGE)
        sys.exit(1)
    
    try:
        # Validate environment
        api_key = validate_environment()
        
        # Create assistant and generate response
        assistant = AIAssistant(api_key, verbose)
        user_prompt = " ".join(args)
        response = assistant.generate_response(user_prompt)
        
        # CHANGE 2: Add "Final response:" header before printing the result
        print("Final response:")
        print(response)
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    clean_pycache()