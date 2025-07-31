import os


def get_files_info(working_directory, directory="."):
    base_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_path, directory)) 
    if not full_path.startswith(base_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    items = os.listdir(full_path) 
    if not items:
        return f"this directory '{directory} is empty"
    output_string = [f"Result for current directory:"]  
    for item in items: 
        item_path = os.path.join(full_path, item)
        file_size = os.path.getsize(item_path) 
        is_dir = os.path.isdir(item_path) 
        output_string.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}") 

    return "\n".join(output_string)



