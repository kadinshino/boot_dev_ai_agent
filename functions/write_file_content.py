import os

def write_file(working_directory, file_path, content):
    # Combine the working directory with the file path using os.path.join
    full_file_path = os.path.join(working_directory, file_path)
    
    # Convert both paths to absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(full_file_path)
    
    # Check if the file path is outside of the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        # Write content to the file, overwriting if it already exists
        with open(full_file_path, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'

