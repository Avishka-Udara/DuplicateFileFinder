import os
import hashlib
from tqdm import tqdm
from termcolor import colored

def compute_file_hash(file_path, chunk_size=1024):
    """Compute SHA-256 hash of the given file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
    except IOError:
        print(colored(f"Cannot read file: {file_path}", 'red'))
        return None
    return sha256.hexdigest()

def find_duplicate_files(start_directory):
    """Find and list duplicate files in the given directory."""
    hashes = {}
    duplicates = []

    # Get a list of all files to process for progress bar
    file_list = []
    for root, _, files in os.walk(start_directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    
    for file_path in tqdm(file_list, desc="Scanning files"):
        file_hash = compute_file_hash(file_path)
        
        if file_hash:
            if file_hash in hashes:
                duplicates.append((file_path, hashes[file_hash]))
            else:
                hashes[file_hash] = file_path

    return duplicates

def delete_files(duplicates):
    """Delete the duplicate files after user confirmation."""
    for duplicate, original in duplicates:
        print(colored(f"Duplicate: {duplicate} (original: {original})", 'yellow'))
    
    confirm = input(colored("Do you want to delete all duplicate files? (yes/no): ", 'cyan')).strip().lower()
    
    if confirm == 'yes':
        for duplicate, _ in duplicates:
            try:
                os.remove(duplicate)
                print(colored(f"Deleted: {duplicate}", 'green'))
            except Exception as e:
                print(colored(f"Error deleting {duplicate}: {e}", 'red'))

def main_menu():
    print(colored("Duplicate File Finder", 'cyan'))
    print("1. Scan for duplicate files")
    print("2. Exit")
    choice = input(colored("Enter your choice: ", 'cyan')).strip()

    if choice == '1':
        directory = input(colored("Enter the directory to scan: ", 'cyan')).strip()
        if not os.path.isdir(directory):
            print(colored("Invalid directory. Please try again.", 'red'))
            return
        
        duplicates = find_duplicate_files(directory)

        if duplicates:
            print(colored("Duplicate files found:", 'blue'))
            for duplicate, original in duplicates:
                print(colored(f"{duplicate} is a duplicate of {original}", 'yellow'))
            
            delete_choice = input(colored("Do you want to delete duplicate files? (yes/no): ", 'cyan')).strip().lower()
            if delete_choice == 'yes':
                delete_files(duplicates)
        else:
            print(colored("No duplicate files found.", 'green'))
    elif choice == '2':
        print(colored("Exiting...", 'cyan'))
        exit()
    else:
        print(colored("Invalid choice. Please try again.", 'red'))

if __name__ == "__main__":
    try:
        while True:
            main_menu()
    except KeyboardInterrupt:
        print(colored("\nProcess interrupted by user. Exiting...", 'red'))
