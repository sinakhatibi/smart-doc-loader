from util.file_manager import *

# Example usage
if __name__ == "__main__":
    file_manager = FileManager()
    
    # file_manager.reset_all_directories()
    file_manager.reset_originals_directory()
    # raw_files = file_manager.list_raw_files()
    # print(raw_files)

    processed_files = file_manager.process_raw_dir()