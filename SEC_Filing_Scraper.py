# Import necessary modules
import requests
import pandas as pd
import time
import sys
from datetime import datetime, timedelta
import pytz
import os


def ensure_directory_exists(file_path):
    """Create directory if it doesn't exist"""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def print_program_info():
    print(r"""
███████ ███████  ██████     ██████  ██████   ██████       ██ ███████  ██████ ████████     ███    ███  ██████  ███    ██ ██ ████████  ██████  ██████  ██ ███    ██  ██████  
██      ██      ██          ██   ██ ██   ██ ██    ██      ██ ██      ██         ██        ████  ████ ██    ██ ████   ██ ██    ██    ██    ██ ██   ██ ██ ████   ██ ██       
███████ █████   ██          ██████  ██████  ██    ██      ██ █████   ██         ██        ██ ████ ██ ██    ██ ██ ██  ██ ██    ██    ██    ██ ██████  ██ ██ ██  ██ ██   ███ 
     ██ ██      ██          ██      ██   ██ ██    ██ ██   ██ ██      ██         ██        ██  ██  ██ ██    ██ ██  ██ ██ ██    ██    ██    ██ ██   ██ ██ ██  ██ ██ ██    ██ 
███████ ███████  ██████     ██      ██   ██  ██████   █████  ███████  ██████    ██        ██      ██  ██████  ██   ████ ██    ██     ██████  ██   ██ ██ ██   ████  ██████  
""")
    print("=" * 80)
    print("SEC Filing Monitor".center(80))
    print("=" * 80)
    print("Copyright © 2025 Gabriel Cabrera & Nomad Data Services. All Rights Reserved.".center(80))
    print("=" * 80)
    print("""
This program pulls all SEC filings for a specified list of companies found at C:\\Data Projects\\SEC Filing Scrape\\CIK_List.txt.

It performs the following tasks:

1. Fetches recent SEC filing data for each company
2. Filters out certain form types (Forms 3, 4, 144, 13G and their amendments)
3. Creates a comprehensive dataset with filing details and clickable URLs
4. Identifies new filings since the previous Friday

The program respects SEC's rate limits and includes error handling for failed requests.

For assistance and other troubleshooting services, contact Gabriel Cabrera.
    """)
    print("=" * 80 + "\n")


def load_ciks_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read lines, strip whitespace, and filter out empty lines
            ciks = [line.strip() for line in file.readlines() if line.strip()]

            # Format each CIK as a 10-digit string
            formatted_ciks = [cik.zfill(10) for cik in ciks]

            print(f"Successfully loaded {len(formatted_ciks)} CIKs from {file_path}")
            return formatted_ciks
    except FileNotFoundError:
        print(f"Error: Could not find file at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CIK file: {str(e)}")
        sys.exit(1)


# Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/91.0.4472.124 Safari/537.36'
}

# Define absolute file paths
log_file_path = r'C:\Data Projects\SEC Monitoring\log.txt'
cik_file_path = r'C:\Data Projects\SEC Filing Scrape\CIK_List.txt'
output_file_path = r'C:\Data Projects\SEC Filing Scrape\SEC_filings_data_all_ciks_with_urls_filtered.xlsx'


# Calculate the previous Friday at 12:01 AM EST
def get_previous_friday():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    days_since_friday = (now.weekday() - 4) % 7
    last_friday = now - timedelta(days=days_since_friday)
    return last_friday.replace(hour=0, minute=1, second=0, microsecond=0)


# Redirect print output to the log file and console
class Logger:
    def __init__(self, log_file):
        ensure_directory_exists(log_file)
        self.log_file = open(log_file, "w", encoding='utf-8')
        self.console = sys.stdout
        self.is_closed = False

    def write(self, message):
        if not self.is_closed:
            self.console.write(message)
            self.log_file.write(message)

    def flush(self):
        if not self.is_closed:
            self.console.flush()
            self.log_file.flush()

    def close(self):
        if not self.is_closed:
            self.log_file.close()
            self.is_closed = True


# Fetch SEC data for a single CIK
def fetch_sec_data(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        company_name = data.get('name', 'Unknown Company')
        return data, company_name
    elif response.status_code == 404:
        print(f"Data not found for CIK {cik} (404).")
        return None, None
    else:
        print(f"Failed to fetch data for CIK {cik}. Status code: {response.status_code}")
        return None, None


def main():
    try:
        # Ensure all necessary directories exist
        ensure_directory_exists(log_file_path)
        ensure_directory_exists(output_file_path)

        sys.stdout = Logger(log_file_path)

        # Print program information
        print_program_info()

        # Load CIKs from file
        ciks = load_ciks_from_file(cik_file_path)

        # Create an empty dataframe to store all the data
        all_filings_df = pd.DataFrame()

        # Lists to keep track of CIKs that succeeded or failed
        successful_ciks = []
        failed_ciks = []

        # Forms to filter out
        excluded_forms = ['3', '4', '144', '13G', '3/A', '4/A', '144/A', '13G/A', 'SC 13G', 'SC 13G/A']

        # Get the date range for reporting
        previous_friday = get_previous_friday()
        current_time = datetime.now(pytz.timezone('US/Eastern'))

        print(
            f"\nGathering all filings and will report new submissions since {previous_friday.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")

        # Loop through each CIK
        for cik in ciks:
            sec_data, company_name = fetch_sec_data(cik)
            time.sleep(0.33)  # 330 ms delay to ensure no more than 3 requests per second

            if sec_data:
                # Extract the 'recent' filings section
                recent_filings = sec_data.get('filings', {}).get('recent', {})

                # Check if the recent_filings section exists
                if 'accessionNumber' in recent_filings:
                    num_filings = len(recent_filings['accessionNumber'])

                    # Create a dataframe from the JSON data
                    df = pd.DataFrame({
                        'Company Name': [company_name] * num_filings,
                        'CIK': [cik] * num_filings,
                        'Accession Number': recent_filings['accessionNumber'],
                        'Combined File Number': [f"{cik}-{acc_num}" for acc_num in recent_filings['accessionNumber']],
                        'Filing Date': recent_filings['filingDate'],
                        'Report Date': recent_filings.get('reportDate', ['N/A'] * num_filings),
                        'Form': recent_filings['form'],
                        'SEC File Number': recent_filings.get('fileNumber', ['N/A'] * num_filings),
                        'Primary Document': recent_filings['primaryDocument']
                    })

                    # Filter out excluded forms
                    df = df[~df['Form'].isin(excluded_forms)]

                    if not df.empty:
                        # Generate the clickable filing URL
                        df['Filing URL'] = df.apply(
                            lambda row: f"https://www.sec.gov/Archives/edgar/data/{row['CIK'].lstrip('0')}/"
                                        f"{row['Accession Number'].replace('-', '')}/{row['Accession Number']}-index.html",
                            axis=1
                        )

                        # Append this CIK's filings to the main dataframe
                        all_filings_df = pd.concat([all_filings_df, df], ignore_index=True)

                    # Add this CIK to the list of successful CIKs
                    successful_ciks.append(cik)
            else:
                # Keep track of CIKs that failed
                failed_ciks.append(cik)

        # Save files with all filings
        all_filings_df.to_excel(output_file_path, index=False)
        print(f"\nResults successfully saved to {output_file_path}")

        # Now analyze recent filings
        all_filings_df['Filing Date'] = pd.to_datetime(all_filings_df['Filing Date'])
        # Convert previous_friday to timezone-naive for comparison
        previous_friday_naive = previous_friday.replace(tzinfo=None)
        recent_filings = all_filings_df[all_filings_df['Filing Date'] >= previous_friday_naive]

        print(f"\nAnalyzing new filings since {previous_friday.strftime('%Y-%m-%d %H:%M:%S %Z')}:")
        print(f"Number of new filings: {len(recent_filings)}")

        if len(recent_filings) > 0:
            print("\nBreakdown of new filings by form type:")
            form_counts = recent_filings['Form'].value_counts()
            for form, count in form_counts.items():
                print(f"{form}: {count} filings")

        if successful_ciks:
            print(f"\nData was successfully retrieved for {len(successful_ciks)} CIKs")

        if failed_ciks:
            print(f"\nThe following CIKs returned no data (404 or other errors): {failed_ciks}")

    finally:
        # Properly close the logger
        if isinstance(sys.stdout, Logger):
            sys.stdout.close()


if __name__ == "__main__":
    main()