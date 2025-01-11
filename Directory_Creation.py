import os


def create_sec_structure():
    # Define paths
    base_folder = r'C:\Data Projects'
    sec_folder = os.path.join(base_folder, 'SEC Filing Scrape')
    cik_file = os.path.join(sec_folder, 'CIK_List.txt')

    # Default CIK numbers
    default_ciks = [
        '789019',
        '320193',
        '1318605',
        '1288776',
        '1018724',
        '1326801',
        '1045810'
    ]

    try:
        # Check if base folder exists
        if os.path.exists(base_folder):
            print(f"Found existing directory: {base_folder}")
        else:
            os.makedirs(base_folder)
            print(f"Created directory: {base_folder}")

        # Create SEC folder
        if os.path.exists(sec_folder):
            print(f"Warning: SEC Filing Scrape folder already exists at: {sec_folder}")
            user_input = input("Do you want to create a new CIK_List.txt file anyway? (yes/no): ")
            if user_input.lower() != 'yes':
                print("Operation cancelled.")
                return
        else:
            os.makedirs(sec_folder)
            print(f"Created directory: {sec_folder}")

        # Create CIK_List.txt with default CIKs
        with open(cik_file, 'w') as f:
            f.write('\n'.join(default_ciks))
        print(f"Created file: {cik_file} with {len(default_ciks)} default CIK numbers")

        print("\nSetup completed successfully!")

    except Exception as e:
        print(f"Error during setup: {str(e)}")


if __name__ == "__main__":
    create_sec_structure()