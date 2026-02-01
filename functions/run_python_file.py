import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        # Absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize target file path
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Guardrail: ensure target_file is inside working_directory
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot execute "{file_path}" '
                f'as it is outside the permitted working directory'
            )

        # Check if file exists and is a regular file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check if file is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        # Build the command
        command = ["python", target_file]
        if args:
            command.extend(args)

        # Run the subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Build output string
        output_parts = []

        # Check for non-zero exit code
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        # Check if there's any output
        has_stdout = result.stdout and result.stdout.strip()
        has_stderr = result.stderr and result.stderr.strip()

        if not has_stdout and not has_stderr:
            output_parts.append("No output produced")
        else:
            if has_stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if has_stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments. Returns the output (stdout/stderr) and exit code.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
