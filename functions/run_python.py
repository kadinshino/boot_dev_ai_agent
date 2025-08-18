import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    # Get the absolute path of the working directory
    abs_working_dir = os.path.abspath(working_directory)

    # Combine the working directory and the relative file path to get the full file path
    full_file_path = os.path.join(abs_working_dir, file_path)

    # Get the absolute path of the full file path
    abs_full_file_path = os.path.abspath(full_file_path)

    # Check if the file path is outside the working directory
    if not abs_full_file_path.startswith(abs_working_dir + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check if the file exists
    if not os.path.exists(abs_full_file_path):
        return f'Error: File "{file_path}" not found.'

    # Check if the file ends with .py
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Set up environment with PYTHONPATH pointing to project root
        env = os.environ.copy()
        project_root = os.path.dirname(abs_working_dir)  # Parent of calculator directory
        env['PYTHONPATH'] = project_root
        
        # Execute the Python file using subprocess.run
        completed_process = subprocess.run(
            ['python3', abs_full_file_path] + args,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=project_root,  # Run from project root, not calculator directory
            env=env
        )

        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        output_str = ""
        if stdout:
            output_str += f"STDOUT: {stdout}\n"
        if stderr:
            output_str += f"STDERR: {stderr}\n"

        if completed_process.returncode != 0:
            output_str += f"Process exited with code {completed_process.returncode}"

        if not output_str.strip():
            return "No output produced."

        return output_str

    except subprocess.TimeoutExpired:
        return "Error: Process execution timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
