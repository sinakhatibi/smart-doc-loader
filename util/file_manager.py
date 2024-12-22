import os
import shutil
import copy

from data_utils import *

class FileManager:
    def __init__(self):
        self.processed_dir = "./Data/processed"
        self.raw_dir = "./Data/raw"
        self.originals_dir = "./Data/originals"
        self.subdir_dict = {}
        self.raw_files_dict = {}
        self.original_files_dict = {}

    # Reset the processed directory
    def reset_processed_directory(self):
        # Check if the directory exists
        if os.path.exists(self.processed_dir):
            # Delete the directory and all its contents
            shutil.rmtree(self.processed_dir)
        
        # Create a new directory
        os.makedirs(self.processed_dir)

    # Reset the raw directory
    def reset_raw_directory(self):
        # Check if the directory exists
        if os.path.exists(self.raw_dir):
            # Delete the directory and all its contents
            shutil.rmtree(self.raw_dir)
        
        # Create a new directory
        os.makedirs(self.raw_dir)

    # Reset the originals directory
    def reset_originals_directory(self):
        # Check if the directory exists
        if os.path.exists(self.originals_dir):
            # Delete the directory and all its contents
            shutil.rmtree(self.originals_dir)
        
        # Create a new directory
        os.makedirs(self.originals_dir)

        # Create subdirectories for different file types and save the addresses in a dictionary
        subdirs = ["zip", "pdf", "csv", "json", "xlsx", "docx", "png", "jpg", "txt", "other"]
        self.subdir_dict = {}
        for subdir in subdirs:
            subdir_path = os.path.join(self.originals_dir, subdir)
            os.makedirs(subdir_path)
            self.subdir_dict[subdir] = subdir_path

    # Reset all directories
    def reset_all_directories(self):
        self.reset_processed_directory()
        self.reset_raw_directory()
        self.reset_originals_directory()

    # List the files in the raw directory to be processed in a dictionary based on their extensions
    def list_raw_files(self):
        return self.append_raw_files(self.raw_dir)
    
    # Append the files in a folder to the list raw files
    def append_raw_files(self, raw_dir, raw_files_dict=None):
        if raw_files_dict is None:
            raw_files_dict = self.raw_files_dict
        for subdir, dirs, files in os.walk(raw_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                extension = file.split(".")[-1]
                if extension in raw_files_dict:
                    raw_files_dict[extension].append(file_path)
                else:
                    raw_files_dict[extension] = [file_path]
        return raw_files_dict
    
    # Process the files in the raw directory
    def process_raw_dir(self):
        raw_files_dict = self.list_raw_files()
        # Append hard copy of raw_files_dict to original_files_dict
        self.original_files_dict = copy.deepcopy(raw_files_dict)

        processed_files = []
        
        # Search in raw_files for the extensions of compressed files
        compressed_extensions = ["zip"]
        for extension in compressed_extensions:
            if extension in raw_files_dict:
                compressed_files = raw_files_dict.pop(extension)
                processed_file = self.process_raw_files(compressed_files, extension)
                processed_files.append(processed_file)

        for extension, files in raw_files_dict.items():
            processed_file = self.process_raw_files(files, extension)
            processed_files.append(processed_file)
        return processed_files
    
    # Process a raw file list based on its extension
    def process_raw_files(self, files, extension):
        switch = {
            "zip": self.process_zip_files,
            "pdf": self.process_pdf_files,
            "csv": self.process_csv_files,
            "json": self.process_json_files,
            "xlsx": self.process_xlsx_files,
            "docx": self.process_docx_files,
            "png": self.process_png_files,
            "jpg": self.process_jpg_files,
            "txt": self.process_txt_files,
            "other": self.process_other_files
        }
        process_function = switch.get(extension, self.process_other_files)
        return process_function(files)

    # Placeholder methods for processing different file types
    def process_zip_files(self, files):
        # loop over the file in files     
        for file in files:
            new_raw_files_dict = {}
            #get the path of the file and file name
            file_path = os.path.dirname(file)
            file_name_extension = os.path.basename(file)
            file_name = os.path.splitext(file_name_extension)[0]
            # create a folder with the name of the file with extension
            new_dir = os.path.join(file_path, file_name)
            os.makedirs(new_dir, exist_ok=True)

            try:
                # extract the file
                shutil.unpack_archive(file, new_dir)
                self.append_raw_files(new_dir, raw_files_dict=new_raw_files_dict)
                if "zip" in new_raw_files_dict:
                    files.extend(new_raw_files_dict["zip"])
                    new_raw_files_dict.pop("zip")
                append_dictionaries(self.raw_files_dict, new_raw_files_dict)
            except:
                print(f"Error extracting file: {file}")
                continue

            #if the zip file is available in the original_files_dict
            # move the file to the processed directory
            # else delete the zip file
            if file in self.original_files_dict["zip"]:
                shutil.move(file, self.subdir_dict["zip"])
            else:
                os.remove(file)



    def process_pdf_files(self, files):
        # Implement processing logic for pdf files
        pass

    def process_csv_files(self, files):
        # Implement processing logic for csv files
        pass

    def process_json_files(self, files):
        # Implement processing logic for json files
        pass

    def process_xlsx_files(self, files):
        # Implement processing logic for xlsx files
        pass

    def process_docx_files(self, files):
        # Implement processing logic for docx files
        pass

    def process_png_files(self, files):
        # Implement processing logic for png files
        pass

    def process_jpg_files(self, files):
        # Implement processing logic for jpg files
        pass

    def process_txt_files(self, files):
        # Implement processing logic for txt files
        pass

    def process_other_files(self, files):
        # Implement processing logic for other files
        pass

# Example usage
if __name__ == "__main__":
    file_manager = FileManager()
    
    # file_manager.reset_all_directories()
    file_manager.reset_originals_directory()
    # raw_files = file_manager.list_raw_files()
    # print(raw_files)

    processed_files = file_manager.process_raw_dir()