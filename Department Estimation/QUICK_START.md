# 🎯 QUICK START GUIDE FOR LLMs

## 📁 Project Status: READY TO USE ✅

### 🗂️ File Structure (Clean)
```
/root/FCAI-CU/Department Estimation/
├── 📋 README.md                              # Full documentation
├── ⚙️ config.py                             # API configuration (UPDATE TOKEN HERE)
├── 🚀 quick_test.py                         # Test API connection (RUN FIRST)
├── 📊 fetch_corrected_data.py               # Main data fetcher (MAIN SCRIPT)
├── 📄 corrected_student_data_YYYYMMDD.xlsx  # Latest data output
├── 📄 Sample.xlsx                           # Reference file
└── 🔧 .venv/                               # Python environment
```

## 🚨 CRITICAL: Token Management
**The API token WILL expire!** When it does:
1. ❌ You'll get 401 authentication errors
2. 🔄 Get new token from browser dev tools when logged in
3. ✏️ Update `token` in `config.py`
4. ✅ Test with `python quick_test.py`

## 🏃‍♂️ Quick Commands

### 1. Test API (Always run first!)
```bash
python quick_test.py
```
**Expected output**: ✅ API working, sample data shown

### 2. Fetch All Data (Main process)
```bash
python fetch_corrected_data.py
```
**Time**: 10-30 minutes  
**Output**: `corrected_student_data_YYYYMMDD_HHMMSS.xlsx`

## 📊 Data Output Structure

### Excel File Contains:
1. **"All Data" Sheet**: Every course enrollment record (~50,000+ rows)
2. **"Entry_Year_YYYY" Sheets**: Unique students by their admission year
   - Entry_Year_2016, Entry_Year_2017, ..., Entry_Year_2024
   - Only unique students (no duplicates)
   - Columns: name, student_id, phone, mobile, email, address, gpa

## 🔍 Key Concepts for LLMs

### ⚠️ IMPORTANT DISTINCTION:
- **Entry Year** (`student.entryYear`) = When student was admitted ✅ USE THIS
- **Course Year** (`record.year`) = When course was taken ❌ DON'T USE FOR GROUPING

**Example**: A student admitted in 2020 may have courses in 2020, 2021, 2022, 2023

### 🔄 Data Updates
- **When**: New semester, student info changes, token expires
- **How**: Run `fetch_corrected_data.py` again
- **Result**: New timestamped Excel file

## 🛟 Troubleshooting for LLMs

| Problem | Cause | Solution |
|---------|--------|----------|
| 401 Auth Error | Token expired | Update token in `config.py` |
| Connection timeout | Network/server slow | Increase timeout in config |
| Empty response | Wrong parameters | Check API endpoint |
| Memory error | Too much data | Process in smaller chunks |

## 📞 LLM Helper Functions

When assisting users, you can:

```python
# Test if API is working
def check_api_status():
    return run_command("python quick_test.py")

# Fetch latest data
def update_student_data():
    return run_command("python fetch_corrected_data.py")

# Quick validation
def validate_data(filename):
    df = pd.read_excel(filename, sheet_name='All Data')
    return {
        'total_records': len(df),
        'unique_students': df['student_id'].nunique(),
        'entry_years': sorted(df['entry_year'].unique()),
        'latest_file': filename
    }
```

## 🎯 Success Indicators

✅ **API Working**: `quick_test.py` shows sample data  
✅ **Data Fetched**: New Excel file created with timestamp  
✅ **Data Valid**: Multiple entry years (2016-2024), thousands of students  
✅ **Sheets Created**: One sheet per entry year + "All Data" sheet  

## 🚀 Ready to Help Users!

The system is now:
- ✅ Clean and organized
- ✅ Well documented
- ✅ Easy to test
- ✅ Easy to update
- ✅ Error-resistant
- ✅ LLM-friendly

**Last verified**: August 2025 ✨
