import os
import shutil
import copy
from markitdown import MarkItDown
from data_utils import *
from docx import Document

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
        # loop over the file in files
        for file in files:
            md = MarkItDown()
            result = md.convert(file)
            # Save result to a markdown file
            file_name = os.path.splitext(file)[0] + ".md"
            with open(file_name, 'w') as f:
                f.write(result)

            # if the pdf file is available in the original_files_dict
            # move the file to the processed directory
            # else delete the pdf file
            # if file in self.original_files_dict["pdf"]:
            #     shutil.move(file, self.subdir_dict["pdf"])
            # else:
            #     os.remove(file)

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
        for file in files:
            # Read docx file and separate content
            doc = Document(file)
            elements = []
            para_start_index = 0
            objects_dict = {}

            # Iterate through document elements
            for element in doc.element.body:
                if element.tag.endswith('p'):
                    for index, para in enumerate(doc.paragraphs[para_start_index:]):
                        if para._element == element:
                            para_start_index += index + 1 # Update the start index for the next iteration
                            para_text = para.text
                            if para.style is None:
                                para_style = ""
                            else:
                                para_style = para.style.name.lower()
                            elements.append({"type": para_style, "content": para_text})
                            
                            # Check for images in the paragraph
                            for run in para.runs:
                            #     image_elements = has_image(run)
                            #     for img_index, img in enumerate(image_elements):
                            #         # print(f"Image found in paragraph {index + 1}, run {para.runs.index(run) + 1}, image {img_index + 1}")
                            #         # Add image to elements
                            #         elements.append({"type": "image", "content": img})
                                if hasattr(run, 'element') and run.element.xpath('.//a:blip'):
                                    for blip in run.element.xpath('.//a:blip'):
                                        rId = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                                        image_data = doc.part.related_parts[rId].blob
                                        elements.append({"type": "image", "content": image_data})
                            break

                elif element.tag.endswith('tbl'):
                    # Find the table in doc.tables
                    for table in doc.tables:
                        if table._element == element:
                            table_data = []
                            for row in table.rows:
                                row_data = [cell.text for cell in row.cells]
                                table_data.append(row_data)
                            elements.append({"type": "table", "content": table_data})
                            break
                elif element.tag.endswith('sectPr'):
                    # Handle section properties if needed
                    pass

            #save the content of elements to a markdown file
            # Determine the relative path of the file within the raw directory
            relative_path = os.path.relpath(file, self.raw_dir)
            
            # Construct the new file path in the processed directory
            new_file_path = os.path.join(self.processed_dir, os.path.splitext(relative_path)[0] + ".md")
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            image_index = 1
            # Save the result to the new file path
            with open(new_file_path, 'w') as f:
                for element in elements:
                    element_type = element["type"].lower()
                    if ("list" in element_type)  or ("bullet" in element_type):
                        bullet = '-' if 'bullet' in element_type else '1.'
                        f.write(f"{bullet} {element['content']}\n")
                    elif element_type== "title":
                        f.write("# " + element["content"] + "\n")
                    elif element_type.startswith("heading"):
                        heading_level = element_type.replace("heading", "")
                        f.write("#" * int(heading_level) + " " + element["content"] + "\n")
                    elif element_type == "table":
                        table_content = element["content"]
                        # Write table header
                        header = table_content[0]
                        f.write("| " + " | ".join(header) + " |\n")
                        f.write("|" + " --- |" * len(header) + "\n")
                        # Write table rows
                        for row in table_content[1:]:
                            f.write("| " + " | ".join(row) + " |\n")
                    elif element_type == "image":
                        #check if the images folder exists and create it if it does not
                        images_folder = os.path.join(os.path.dirname(new_file_path), "images")
                        os.makedirs(images_folder, exist_ok=True)
                        #save the image to the images folder
                        image_path = os.path.join(images_folder, f"image_{image_index}.png")
                        with open(image_path, 'wb') as img_file:
                            img_file.write(element["content"])
                        f.write(f"![image](images/image_{image_index}.png)\n")
                        image_index += 1

                    else:
                        f.write(element["content"] + "\n")
    
                    
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
        
def has_image(run):
    return run.element.xpath('.//pic:pic')

# Example usage
if __name__ == "__main__":
    file_manager = FileManager()
    
    # file_manager.reset_all_directories()
    file_manager.reset_originals_directory()
    # raw_files = file_manager.list_raw_files()
    # print(raw_files)

    processed_files = file_manager.process_raw_dir()