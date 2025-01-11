import requests
import json
import pandas as pd
from pathlib import Path
import time
import random
import os


class SECRateLimiter:
    def __init__(self):
        self.last_request_time = 0
        self.min_delay = 0.5  # 500ms minimum delay for 2 requests per second
        self.max_delay = 0.6  # Add small buffer for safety

    def wait(self):
        """Ensures appropriate waiting time between requests"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time

        if elapsed < self.min_delay:
            wait_time = self.min_delay - elapsed + random.uniform(0, 0.05)
            time.sleep(wait_time)

        self.last_request_time = time.time()


class SECSetup:
    def __init__(self):
        self.base_folder = Path(r'C:\Data Projects')
        self.sec_folder = self.base_folder / 'SEC Filing Scrape'
        self.default_ciks = [
            '789019',  # MICROSOFT CORP
            '320193',  # APPLE INC
            '1318605', # TESLA INC
            '1288776', # GOOGLE/ALPHABET
            '1018724', # AMAZON COM INC
            '1326801', # META/FACEBOOK
            '1045810'  # NVIDIA CORP
        ]
        self.headers = {
            'User-Agent': 'Sample Company Name AdminContact@domain.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
        self.rate_limiter = SECRateLimiter()

    def create_directories(self):
        """Creates necessary directories for SEC data storage"""
        try:
            # Create base folder if it doesn't exist
            if self.base_folder.exists():
                print(f"Found existing directory: {self.base_folder}")
            else:
                self.base_folder.mkdir(parents=True)
                print(f"Created directory: {self.base_folder}")

            # Create SEC folder if needed
            if self.sec_folder.exists():
                print(f"Warning: SEC Filing Scrape folder already exists at: {self.sec_folder}")
                user_input = input("Do you want to proceed with updating the files? (yes/no): ")
                if user_input.lower() != 'yes':
                    print("Operation cancelled.")
                    return False
            else:
                self.sec_folder.mkdir(parents=True)
                print(f"Created directory: {self.sec_folder}")
            
            return True

        except Exception as e:
            print(f"Error during directory setup: {str(e)}")
            return False

    def fetch_company_tickers(self):
        """Fetches the complete list of companies and their CIK numbers from SEC's EDGAR system"""
        url = "https://www.sec.gov/files/company_tickers.json"

        try:
            print("Fetching company data from SEC...")
            self.rate_limiter.wait()
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            # Convert to DataFrame and process
            df = pd.DataFrame.from_dict(data, orient='index')
            df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)
            
            # Rename columns for clarity
            df = df.rename(columns={
                'cik_str': 'CIK',
                'title': 'Company Name',
                'ticker': 'Ticker'
            })

            # Sort by company name
            df = df.sort_values('Company Name')

            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def save_data(self, df):
        """Saves the company data to CSV and CIK list files"""
        try:
            csv_path = self.sec_folder / "SEC_Companies.csv"
            cik_path = self.sec_folder / "CIK_List.txt"

            # Save full company data to CSV
            df.to_csv(csv_path, index=False)
            
            # Save CIK list
            df['CIK'].to_csv(cik_path, index=False, header=False)

            print(f"\nSuccessfully saved {len(df)} companies")
            print(f"CSV: {csv_path}")
            print(f"CIK List: {cik_path}")
            
            return True

        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False

    def create_default_cik_list(self):
        """Creates a CIK list with default companies if SEC fetch fails"""
        try:
            cik_path = self.sec_folder / "CIK_List.txt"
            with open(cik_path, 'w') as f:
                f.write('\n'.join(self.default_ciks))
            print(f"\nCreated default CIK list with {len(self.default_ciks)} companies")
            print(f"CIK List: {cik_path}")
            return True
        except Exception as e:
            print(f"Error creating default CIK list: {str(e)}")
            return False

    def run_setup(self):
        """Main setup process"""
        print("Starting SEC data setup...")
        print("Please ensure you've updated the User-Agent header with your contact information")

        # Create necessary directories
        if not self.create_directories():
            return

        # Fetch company data
        df = self.fetch_company_tickers()
        
        if df is not None:
            # Save fetched data
            if self.save_data(df):
                print("\nSetup completed successfully!")
            else:
                print("\nFalling back to default CIK list...")
                self.create_default_cik_list()
        else:
            print("\nFalling back to default CIK list...")
            self.create_default_cik_list()


if __name__ == "__main__":
    setup = SECSetup()
    setup.run_setup()
