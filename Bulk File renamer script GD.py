import os
import shutil
import logging
import argparse
from datetime import datetime

# Logging Setup
log_filename = f"organizer_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to organize files by extension
def organize_files_by_extension(folder_path):
    try:
        if not os.path.isdir(folder_path):
            logging.error(f"Provided path is not a directory: {folder_path}")
            print(" The path you provided is not a valid directory.")
            return

        files = os.listdir(folder_path)
        if not files:
            print(" The folder is empty.")
            return

        moved_files_count = 0  # NEW: Count of moved files


        for file_name in files:
            # Skip hidden files
            if file_name.startswith('.'):
                continue

            full_file_path = os.path.join(folder_path, file_name)

            if os.path.isfile(full_file_path):
                extension = file_name.split('.')[-1].lower()
                if extension == file_name:
                    extension = "no_extension"

                target_folder = os.path.join(folder_path, f"{extension.upper()}_Files")

                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                    logging.info(f" Created folder: {target_folder}")

                # Handle filename conflict
                base, ext = os.path.splitext(file_name)
                new_name = file_name
                counter = 1
                while os.path.exists(os.path.join(target_folder, new_name)):
                    new_name = f"{base}_{counter}{ext}"
                    counter += 1

                # Move the file
                shutil.move(full_file_path, os.path.join(target_folder, new_name))
                logging.info(f" Moved: {file_name} → {target_folder}/{new_name}")
                moved_files_count += 1  # NEW: Count updated

        print(f"\n {moved_files_count} file(s) have been organized by extension.")
        print(f" Log file saved as: {log_filename}\n") # NEW: Log file info


    except Exception as e:
        logging.exception("An error occurred while organizing files.")
        print(f"Error: {e}")  # UPDATED: Error print is cleaner


# CLI Setup
def main():
    parser = argparse.ArgumentParser(description=" Bulk File Organizer Script")
    parser.add_argument("path", help=" Path to the folder you want to organize")
    args = parser.parse_args()

    organize_files_by_extension(args.path)

# Run the script
if __name__ == "__main__":
    main()