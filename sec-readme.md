# SEC Filing Monitor

## Overview
The SEC Filing Monitor is a Python-based system that automatically tracks and retrieves SEC filings for specified companies. It maintains a watchlist of companies by their Central Index Key (CIK) numbers and provides comprehensive filing data with direct links to SEC documents.

## Features
- Automated retrieval of SEC filings from EDGAR database
- Filtering capabilities to exclude specific form types (Forms 3, 4, 144, 13G and their amendments)
- Generation of clickable URLs for easy access to filing documents
- Detection of new filings since the previous Friday
- Rate limiting compliance with SEC's API requirements
- Comprehensive error handling and logging

## System Requirements
- Python 3.x
- Internet connection
- Required Python packages:
  - requests
  - pandas
  - pytz

## Directory Structure
The system operates in the following directory structure:
```
C:\Data Projects\
└── SEC Filing Scrape\
    ├── CIK_List.txt
    ├── SEC_Companies.csv
    └── SEC_filings_data_all_ciks_with_urls_filtered.csv
```

## Components

### 1. Directory_Creation.py
Sets up the initial directory structure and creates necessary files:
- Creates required folders
- Fetches and saves a comprehensive list of SEC-registered companies
- Generates a default CIK list for major tech companies if SEC fetch fails
- Implements SEC-compliant rate limiting

### 2. SEC_Filing_Scraper.py
The main monitoring system that:
- Reads CIKs from CIK_List.txt
- Retrieves filing data for each company
- Filters out specified form types
- Generates clickable URLs for each filing
- Creates a comprehensive CSV report
- Identifies new filings since the previous Friday

### 3. Directory_Removal.py
A utility script for cleaning up the SEC Filing Scrape directory when needed.

## Setup Instructions

1. Ensure Python 3.x is installed on your system
2. Install required packages:
   ```bash
   pip install requests pandas pytz
   ```
3. Run the initial setup:
   ```bash
   python Directory_Creation.py
   ```
4. Add or modify CIKs in the CIK_List.txt file as needed
5. Run the monitoring system:
   ```bash
   python SEC_Filing_Scraper.py
   ```

## Output Files

### SEC_Companies.csv
Contains comprehensive information about all SEC-registered companies:
- CIK (Central Index Key)
- Company Name
- Ticker Symbol

### SEC_filings_data_all_ciks_with_urls_filtered.csv
Contains detailed filing information:
- Company Name
- CIK
- Accession Number
- Filing Date
- Report Date
- Form Type
- SEC File Number
- Primary Document
- Filing URL

## Rate Limiting
The system implements SEC's rate limiting requirements:
- Maximum 2 requests per second
- Includes safety buffers and random delays
- User-Agent header identification

## Error Handling
- Comprehensive logging of all operations
- Fallback mechanisms for failed data retrieval
- User confirmation for potentially destructive operations

## Copyright
Copyright © 2025 Gabriel Cabrera & Nomad Data Services. All Rights Reserved.

## Support
For assistance and troubleshooting services, contact Gabriel Cabrera.

## Notes
- Ensure proper network connectivity to access SEC's EDGAR database
- Keep the CIK_List.txt file updated with desired companies
- Review log files for any issues or errors
- The system automatically excludes certain form types (3, 4, 144, 13G and amendments)
