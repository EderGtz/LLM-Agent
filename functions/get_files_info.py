import os

#Acepts a directory path, and return a str that represents the contents
#of that directory. This is a function for the LLM agent
def get_files_info(working_directory, directory="."):
    #directory es treated as a relative path within wd

    contents_of_directory = ""
    if directory == ".":
        contents_of_directory += "Result for current directory:\n"
    else:
        contents_of_directory += f"Result for '{directory}' directory:\n"

    #If the absolute path of directory is outside the wd, return Error
    #This is a guardrail, so the LLM cannot perform anything outside wd gave
    path_to_wd = os.path.abspath(working_directory)
    path_to_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not path_to_dir.startswith(path_to_wd):
        contents_of_directory += f'   Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        return contents_of_directory
    
    #In case the directory argument is not a directory
    if not os.path.isdir(path_to_dir):
         contents_of_directory +=   f'  Error: "{directory}" is not a directory\n'
         return contents_of_directory
    
    try:
        for file in os.listdir(path_to_dir):
            #Building a complete path for every file
            full_path = os.path.join(path_to_dir, file)
            size_of_file = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            contents_of_directory += f"    - {file}: file_size={size_of_file} bytes, is_dir={is_dir}\n"
        return contents_of_directory
            #Returns a str representing the contents of a directory

    except Exception as e:
        return f"Error: {e}"
    