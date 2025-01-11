import os
import shutil
import sys


def delete_folder():
    folder_path = r'C:\Data Projects\SEC Filing Scrape'

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    # Get user confirmation
    print(f"WARNING: This will permanently delete the folder and all contents:")
    print(folder_path)
    confirmation = input("\nAre you sure you want to proceed? (yes/no): ")

    if confirmation.lower() != 'yes':
        print("Operation cancelled.")
        return

    try:
        # Delete the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"\nSuccessfully deleted: {folder_path}")
    except Exception as e:
        print(f"\nError deleting folder: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    delete_folder()