# Student Data Fetcher - API Documentation

## Overview
This project fetches student course data from the FCAI-CU API and organizes it into Excel sheets by student entry year.

## 📁 Project Files
- `fetch_corrected_data.py` - Main script to fetch and process all student data
- `corrected_student_data_YYYYMMDD_HHMMSS.xlsx` - Output Excel file with all data
- `Sample.xlsx` - Sample/reference file

## 🔧 API Information

### Endpoint
```
http://193.227.14.58/api/student-courses
```

### Authentication
Bearer Token (needs to be updated when expired):
```
Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIyMDIzMDI2MyIsImF1dGgiOiJST0xFX1NUVURFTlQiLCJleHAiOjE3NTQ2OTMwOTh9.BzjnOzZ4LlMAxJIcbD7GRt-3EK1giwrGmpmmM_xPBq0RoSJ1FL6QbNJeivw45a3aqH2NTijNF6-FhWOsgY8mUg
```

### Parameters
- `size`: Number of records per page (recommended: 2000)
- `page`: Page number (0-based)
- `includeWithdraw.equals`: Include withdrawn students (true/false)

### Example Request
```
GET http://193.227.14.58/api/student-courses?size=2000&page=0&includeWithdraw.equals=true
```

## 📊 Data Structure

### API Response Format
The API returns an array of course enrollment records:

```json
[
  {
    "id": 12345,
    "year": 2023,           // Course completion year
    "student": {
      "id": "20230123",
      "name": "Student Name",
      "phone": "123456789",
      "mobile": "987654321",
      "email": "student@example.com",
      "address": "Student Address",
      "gpa": 3.5,
      "entryYear": "2020"   // ⭐ IMPORTANT: Student's actual entry year
    },
    "course": {
      "name": "Course Name"
    },
    "withdraw": false
  }
]
```

### Key Fields Explanation
- **`student.entryYear`**: The year the student was admitted/entered the university
- **`year`**: The academic year when the specific course was taken
- **`withdraw`**: Whether the student withdrew from this course

## 🎯 Output Excel Structure

### Sheet: "All Data"
Contains all raw course enrollment records with these columns:
- `name` - Student name
- `student_id` - Student ID
- `phone` - Phone number
- `mobile` - Mobile number
- `email` - Email address
- `address` - Address
- `gpa` - GPA
- `entry_year` - Student's entry/admission year
- `course_year` - Year when course was taken
- `course_name` - Course name
- `withdraw` - Withdrawal status

### Sheets: "Entry_Year_YYYY"
One sheet per entry year containing unique students only:
- `name` - Student name
- `student_id` - Student ID
- `phone` - Phone number
- `mobile` - Mobile number
- `email` - Email address
- `address` - Address
- `gpa` - GPA

**Note**: Duplicate students (same student_id) are removed, keeping only the first occurrence.

## 🚀 How to Use

### Prerequisites
```bash
pip install requests pandas openpyxl
```

### Running the Script
```bash
python fetch_corrected_data.py
```

### Expected Output
```
==============================================================
CORRECTED STUDENT DATA FETCHER
Using correct student entry years (not course years)
==============================================================
Starting to fetch ALL student data with correct entry years...
Fetching page 1...
  Got 2000 records, total: 2000
  Entry years in this page: ['2016', '2017', '2018']
...
Total records fetched: XXXXX
All entry years found: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
Processing student data with correct entry years...
Saved all data: XXXXX records
Creating sheets for entry years: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
Entry Year 2016: XX unique students (from XXX total course records)
...
Data saved to: corrected_student_data_YYYYMMDD_HHMMSS.xlsx
==============================================================
COMPLETED SUCCESSFULLY!
==============================================================
```

## 🔄 Updating Data

### When to Update
- When new students are enrolled
- At the end of each semester
- When student information changes
- When the API token expires

### Steps to Update
1. **Check if token is still valid** by running a small test
2. **Update the token** in the script if expired
3. **Run the script** to fetch latest data
4. **Compare** with previous data to see changes
5. **Archive** old files if needed

### Token Renewal
If you get authentication errors, you need to:
1. Log into the system with valid credentials
2. Extract the new Bearer token from browser developer tools
3. Update the token in `fetch_corrected_data.py`

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Increase timeout in the script
   - Check internet connection
   - Try smaller page sizes

2. **Authentication Failed**
   - Token has expired - get a new one
   - Check token format (should start with "Bearer ")

3. **Empty Response**
   - API might be down
   - Check if endpoint URL is correct
   - Verify parameters

4. **Memory Issues**
   - Process data in smaller chunks
   - Reduce page size
   - Clear variables between pages

### Error Handling
The script includes:
- Automatic retry on failures
- Timeout handling
- Progress tracking
- Error logging

## 📋 Data Quality Checks

### Before Using Data
1. **Check entry years**: Should have reasonable range (e.g., 2015-2024)
2. **Verify student counts**: Compare with expected enrollment numbers
3. **Check for duplicates**: Script removes them, but verify manually
4. **Validate required fields**: Ensure names, IDs are not empty

### Data Validation
```python
# Quick validation in Python
import pandas as pd

df = pd.read_excel('corrected_student_data_YYYYMMDD_HHMMSS.xlsx', sheet_name='All Data')

print(f"Total records: {len(df)}")
print(f"Unique students: {df['student_id'].nunique()}")
print(f"Entry years: {sorted(df['entry_year'].unique())}")
print(f"Missing names: {df['name'].isna().sum()}")
print(f"Missing student IDs: {df['student_id'].isna().sum()}")
```

## 📞 Support

### For LLMs/AI Assistants
When helping users with this system:

1. **Always check the token expiration** first
2. **Use the corrected script** (`fetch_corrected_data.py`)
3. **Explain the difference** between entry year and course year
4. **Monitor progress** during long fetches
5. **Help with data validation** after fetch
6. **Assist with Excel sheet interpretation**

### Key Points to Remember
- **Entry Year ≠ Course Year**: Use `student.entryYear` for grouping students
- **Handle Duplicates**: Same student appears multiple times (different courses)
- **Large Dataset**: Expect 50,000+ records, be patient
- **Token Management**: Tokens expire, need renewal
- **Error Recovery**: Script can resume from failures

## 🔒 Security Notes
- Never commit tokens to version control
- Rotate tokens regularly
- Use environment variables for sensitive data
- Limit access to student data files
- Follow data privacy regulations

---

**Last Updated**: August 2025  
**Version**: 1.0  
**Tested With**: Python 3.11, pandas 2.x, requests 2.x
