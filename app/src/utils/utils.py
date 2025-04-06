import  os

# ========== utils.py ========== 

"""
Create a directory if it doesn't exist.

Args:
    directory (str): The path of the directory to create.
"""
def create_directory(directory):
    try:
        # Check if the directory exists, and create it if it doesn't
        if os.path.isdir(directory):
            print(f"The directory '{directory}' exists.")
            return 0
        else:
            print(f"The directory '{directory}' does not exist.")
            try:
                os.makedirs(directory, exist_ok=True)  # Create the full directory path
                print(f"Created directory: {directory}")
                return 1
            except Exception as e:
                return -1
    except Exception as e:
        print(f"Error creating directory '{directory}': {e}")
        return -1
