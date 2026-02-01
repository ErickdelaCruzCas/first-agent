import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
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
                f'Error: Cannot read "{file_path}" '
                f'as it is outside the permitted working directory'
            )

        # Must be a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read the file content
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read(MAX_CHARS)

            # Check if the file was larger than the limit
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"