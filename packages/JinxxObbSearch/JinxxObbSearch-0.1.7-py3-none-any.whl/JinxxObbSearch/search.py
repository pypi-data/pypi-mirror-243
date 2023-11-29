import os
import shutil
from tqdm import tqdm


GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
text = "\r\n░░█ █ █▄░█ ▀▄▀ ▀▄▀ █▄▄ █▄▄"
text1 = "Multiple File Search"
print(GREEN + text + RESET)
print(RED + text1 + RESET)
print("Press Ctrl+C to exit.")

search_text = input("Search: ")

while True:
    search_directory = input("Input Path: ")
    if os.path.exists(search_directory) and os.path.isdir(search_directory):
        break
    else:
        print("Folder does not exist. Please enter a valid directory path.")

destination_directory = input("Output path: ")
move = input("Enter 'y' for move or 'n' for copy: ")
saved_files = 0  # Initialize saved_files to 0

try:
    if not os.path.exists(destination_directory):
        print("Folder does not exist. Creating...")
        os.makedirs(destination_directory)

    files_to_process = [filename for filename in os.listdir(search_directory) if os.path.isfile(os.path.join(search_directory, filename))]
    
    if move == "y":
        for filename in tqdm(files_to_process, desc="Processing files"):
            filepath = os.path.join(search_directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    file_content = file.read().lower()  # Read content and convert to lowercase
                    if search_text.lower().encode('utf-8') in file_content:
                        shutil.move(filepath, os.path.join(destination_directory, filename.lower()))
                        saved_files += 1
            except Exception as e:
                print(f"Error processing file {filepath}: {str(e)}")

        print(f"Saved {saved_files} files.")
    else:
        for filename in tqdm(files_to_process, desc="Processing files"):
            filepath = os.path.join(search_directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    file_content = file.read().lower()  # Read content and convert to lowercase
                    if search_text.lower().encode('utf-8') in file_content:
                        shutil.copy(filepath, os.path.join(destination_directory, filename.lower()))
                        saved_files += 1
            except Exception as e:
                print(f"Error processing file {filepath}: {str(e)}")

        print(f"Saved {saved_files} files.")

except KeyboardInterrupt:
    print("\nOperation aborted by user (Ctrl+C). Exiting...")
    exit(0)
except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)