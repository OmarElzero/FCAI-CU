#!/usr/bin/env python3
"""
Quick API Test Script
Use this to quickly test if the API is working and the token is valid
"""

import requests
from config import API_CONFIG

def quick_api_test():
    """Test API connection and token validity"""
    print("🔍 Testing API Connection...")
    print(f"📡 Endpoint: {API_CONFIG['base_url']}")
    
    try:
        # Test with just 5 records
        url = f"{API_CONFIG['base_url']}?size=5&page=0&includeWithdraw.equals=true"
        headers = {
            'Authorization': API_CONFIG['token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Connection Successful!")
            print(f"📊 Got {len(data)} sample records")
            
            if data:
                sample = data[0]
                student = sample.get('student', {})
                
                print("\n📋 Sample Data Structure:")
                print(f"   Student Name: {student.get('name', 'N/A')}")
                print(f"   Student ID: {student.get('id', 'N/A')}")
                print(f"   Entry Year: {student.get('entryYear', 'N/A')}")
                print(f"   Course Year: {sample.get('year', 'N/A')}")
                print(f"   Course: {sample.get('course', {}).get('name', 'N/A')}")
                
                # Check for entry years in sample
                entry_years = set(record.get('student', {}).get('entryYear') for record in data)
                entry_years = {year for year in entry_years if year}
                print(f"\n📅 Entry Years in Sample: {sorted(entry_years)}")
                
            print("\n🎉 Ready to fetch full dataset!")
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication Failed!")
            print("🔑 Token has expired or is invalid")
            print("💡 Please update the token in config.py")
            return False
            
        else:
            print(f"❌ API Error: Status Code {response.status_code}")
            print(f"📝 Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request Timeout - API might be slow")
        return False
    except requests.exceptions.ConnectionError:
        print("🌐 Connection Error - Check internet or API endpoint")
        return False
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        return False

def estimate_total_records():
    """Estimate total number of records available"""
    print("\n📊 Estimating Total Records...")
    
    try:
        # Test with larger page size to estimate
        url = f"{API_CONFIG['base_url']}?size=2000&page=0&includeWithdraw.equals=true"
        headers = {
            'Authorization': API_CONFIG['token'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"📦 First page: {len(data)} records")
            
            if len(data) == 2000:
                print("📈 Looks like there are more pages (full page received)")
                print("🔢 Estimated total: 50,000+ records (will take several minutes to fetch)")
            else:
                print(f"📉 Total records: ~{len(data)} (partial page, might be all data)")
                
        else:
            print("❌ Could not estimate - API error")
            
    except Exception as e:
        print(f"💥 Error estimating: {e}")

def main():
    print("=" * 60)
    print("🚀 STUDENT DATA API - QUICK TEST")
    print("=" * 60)
    
    # Test basic connection
    success = quick_api_test()
    
    if success:
        # Estimate data size
        estimate_total_records()
        
        print("\n" + "=" * 60)
        print("📋 NEXT STEPS:")
        print("=" * 60)
        print("✅ API is working!")
        print("🔄 Run: python fetch_corrected_data.py")
        print("⏱️  This will take 10-30 minutes for full dataset")
        print("📁 Output: corrected_student_data_YYYYMMDD_HHMMSS.xlsx")
        
    else:
        print("\n" + "=" * 60)
        print("🔧 TROUBLESHOOTING:")
        print("=" * 60)
        print("1. Check your internet connection")
        print("2. Update token in config.py if expired")
        print("3. Verify API endpoint is accessible")
        
    print("=" * 60)

if __name__ == "__main__":
    main()
