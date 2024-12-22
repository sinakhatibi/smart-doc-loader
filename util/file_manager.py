import os
import shutil

# Reset the processed directory
def reset_processed_directory():
    processed_dir = "./Data/processed"
    
    # Check if the directory exists
    if os.path.exists(processed_dir):
        # Delete the directory and all its contents
        shutil.rmtree(processed_dir)
    
    # Create a new directory
    os.makedirs(processed_dir)

# Reset the raw directory
def reset_raw_directory():
    raw_dir = "./Data/raw"
    
    # Check if the directory exists
    if os.path.exists(raw_dir):
        # Delete the directory and all its contents
        shutil.rmtree(raw_dir)
    
    # Create a new directory
    os.makedirs(raw_dir)

# Reset the originals directory
def reset_originals_directory():
    originals_dir = "./Data/originals"
    
    # Check if the directory exists
    if os.path.exists(originals_dir):
        # Delete the directory and all its contents
        shutil.rmtree(originals_dir)
    
    # Create a new directory
    os.makedirs(originals_dir)

    # Create a subdirectories for differnet file types and saved the address in a dictionary
    subdirs = ["pdf", "csv", "json", "xlsx", "docx", "png","jpg" ,"txt", "other"]
    subdir_dict = {}
    for subdir in subdirs:
        subdir_path = os.path.join(originals_dir, subdir)
        os.makedirs(subdir_path)
        subdir_dict[subdir] = subdir_path
    return subdir_dict

# Example usage
if __name__ == "__main__":
    reset_processed_directory()
    reset_raw_directory()
    subdir_dict = reset_originals_directory()