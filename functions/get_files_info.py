import os

#Acepts a directory path, and return a str that represents the contents
#of that directory. This is a function for the LLM agent
def get_files_info(working_directory, directory="."):
    #directory es treated as a relative path within wd

    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    #If the absolute path of directory is outside the wd, return Error
    #This is a guardrail, so the LLM cannot perform anything outside wd gave
    path_to_wd = os.path.abspath(working_directory)
    path_to_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not path_to_dir.startswith(path_to_wd):
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    #In case the directory argument is not a directory
    if not os.path.isdir(path_to_dir):
        return  f'  Error: "{directory}" is not a directory'
    
    try:
        for file in os.listdir(path_to_dir):
            #Building a complete path for every file
            full_path = os.path.join(path_to_dir, file)
            size_of_file = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)

            print(f"    - {file}: file_size={size_of_file} bytes, is_dir={is_dir}")
        #Returns a str representing the contents of a directory

    except Exception as e:
        return f"Error: {e}"
    