import requests
import pandas as pd
import json
from datetime import datetime
import time

# API Configuration - Update token here when it expires
API_CONFIG = {
    "base_url": "http://193.227.14.58/api/student-courses",
    "token": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIyMDIzMDI2MyIsImF1dGgiOiJST0xFX1NUVURFTlQiLCJleHAiOjE3NTQ2OTMwOTh9.BzjnOzZ4LlMAxJIcbD7GRt-3EK1giwrGmpmmM_xPBq0RoSJ1FL6QbNJeivw45a3aqH2NTijNF6-FhWOsgY8mUg",
    "page_size": 2000,
    "timeout": 60,
    "max_retries": 3,
    "delay_between_requests": 0.3
}

def fetch_all_student_data_corrected():
    """Fetch all student data using correct entry year"""
    headers = {
        'Authorization': API_CONFIG['token'],
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    all_data = []
    page = 0
    page_size = API_CONFIG['page_size']
    consecutive_failures = 0
    max_failures = API_CONFIG['max_retries']
    
    print("Starting to fetch ALL student data with correct entry years...")
    
    while page < 300 and consecutive_failures < max_failures:  # Increased limit
        try:
            url = f"{API_CONFIG['base_url']}?size={page_size}&page={page}&includeWithdraw.equals=true"
            print(f"Fetching page {page + 1}...")
            
            response = requests.get(url, headers=headers, timeout=API_CONFIG['timeout'])
            response.raise_for_status()
            
            data = response.json()
            
            if not data or len(data) == 0:
                print(f"No more data at page {page + 1}")
                break
                
            all_data.extend(data)
            print(f"  Got {len(data)} records, total: {len(all_data)}")
            
            # Show entry year range for this page
            entry_years = set(record.get('student', {}).get('entryYear') for record in data)
            entry_years = {year for year in entry_years if year}  # Remove None/empty values
            print(f"  Entry years in this page: {sorted(entry_years)}")
            
            # Reset failure counter on success
            consecutive_failures = 0
            
            if len(data) < page_size:
                print("Reached end of data (partial page)")
                break
                
            page += 1
            time.sleep(API_CONFIG['delay_between_requests'])  # Be nice to the server
            
        except Exception as e:
            consecutive_failures += 1
            print(f"Error on page {page}: {e}")
            print(f"Consecutive failures: {consecutive_failures}/{max_failures}")
            
            if consecutive_failures < max_failures:
                print("Retrying after delay...")
                time.sleep(2)
            else:
                print("Too many consecutive failures, stopping.")
                break
    
    print(f"Total records fetched: {len(all_data)}")
    
    # Show all entry years found
    all_entry_years = set(record.get('student', {}).get('entryYear') for record in all_data)
    all_entry_years = {year for year in all_entry_years if year}  # Remove None/empty values
    print(f"All entry years found: {sorted(all_entry_years)}")
    
    return all_data

def process_and_save_corrected_data(raw_data):
    """Process raw data and save to Excel with correct entry years"""
    student_data = []
    
    print("Processing student data with correct entry years...")
    for record in raw_data:
        try:
            student = record.get('student', {})
            
            student_info = {
                'name': student.get('name', ''),
                'student_id': student.get('id', ''),
                'phone': student.get('phone', ''),
                'mobile': student.get('mobile', ''),
                'email': student.get('email', ''),
                'address': student.get('address', ''),
                'gpa': student.get('gpa', ''),
                'entry_year': student.get('entryYear', ''),  # Correct entry year
                'course_year': record.get('year', ''),  # Course year for reference
                'course_name': record.get('course', {}).get('name', ''),
                'withdraw': record.get('withdraw', False)
            }
            
            student_data.append(student_info)
            
        except Exception as e:
            print(f"Error processing record: {e}")
            continue
    
    # Save to Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"corrected_student_data_{timestamp}.xlsx"
    
    df_all = pd.DataFrame(student_data)
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Save ALL data
        df_all.to_excel(writer, sheet_name='All Data', index=False)
        print(f"Saved all data: {len(df_all)} records")
        
        # Get unique entry years
        entry_years = df_all['entry_year'].unique()
        entry_years = [year for year in entry_years if str(year).strip() and str(year) != 'nan' and str(year) != '']
        
        print(f"Creating sheets for entry years: {sorted(entry_years)}")
        
        # Create entry year sheets with unique students only
        for entry_year in sorted(entry_years):
            year_data = df_all[df_all['entry_year'] == entry_year]
            
            # Remove duplicates - keep unique students only
            unique_students = year_data.drop_duplicates(subset=['student_id'], keep='first')
            
            # Select and reorder columns: name, student_id, phone, mobile, email, address, gpa
            columns = ['name', 'student_id', 'phone', 'mobile', 'email', 'address', 'gpa']
            final_data = unique_students[columns]
            
            sheet_name = f"Entry_Year_{entry_year}"
            final_data.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Entry Year {entry_year}: {len(final_data)} unique students (from {len(year_data)} total course records)")
    
    print(f"Data saved to: {filename}")
    return filename

def main():
    print("=" * 70)
    print("CORRECTED STUDENT DATA FETCHER")
    print("Using correct student entry years (not course years)")
    print("=" * 70)
    
    # Fetch all data
    raw_data = fetch_all_student_data_corrected()
    
    if not raw_data:
        print("No data fetched!")
        return
    
    # Process and save
    filename = process_and_save_corrected_data(raw_data)
    
    print("=" * 70)
    print("COMPLETED SUCCESSFULLY!")
    print(f"File saved: {filename}")
    print("Now each sheet contains students by their ENTRY YEAR, not course year")
    print("=" * 70)

if __name__ == "__main__":
    main()
