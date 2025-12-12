import pandas as pd
import numpy as np
import os

np.random.seed(123)
os.makedirs('data', exist_ok=True)

specialties = ['Accident & Emergency', 'Dermatology', 'Clinical Genetics', 'Cardiology', 'Orthopedics', 'Neurology', 'General Surgery', 'Oncology']
case_types = ['Outpatient', 'Day Case', 'Inpatient']
age_groups = ['0-15', '16-64', '65+']

wait_list_data = []
for i in range(5000):
    wait_list_data.append({
        'PatientID': f'P{i+1:05d}',
        'Specialty': np.random.choice(specialties),
        'CaseType': np.random.choice(case_types, p=[0.74, 0.15, 0.11]),
        'AgeGroup': np.random.choice(age_groups, p=[0.2, 0.6, 0.2]),
        'WaitDays': np.random.gamma(2, 30),
        'Priority': np.random.choice(['Routine', 'Urgent', 'Emergency'], p=[0.7, 0.25, 0.05])
    })

pd.DataFrame(wait_list_data).to_csv('data/patient_waitlist.csv', index=False)

months = ['Jan 2018', 'Jul 2018', 'Jan 2019', 'Jul 2019', 'Jan 2020', 'Jul 2020', 'Jan 2021']
monthly_trends = []
for month in months:
    monthly_trends.append({
        'Month': month,
        'Outpatient': np.random.randint(500000, 630000),
        'Inpatient': np.random.randint(20000, 60000),
        'TotalWaitList': np.random.randint(520000, 690000)
    })

pd.DataFrame(monthly_trends).to_csv('data/monthly_trends.csv', index=False)

specialty_stats = []
for specialty in specialties:
    specialty_stats.append({
        'Specialty': specialty,
        'WaitListCount': np.random.randint(15000, 70000),
        'AvgWaitTime': round(np.random.uniform(20, 180), 1),
        'CompletedCases': np.random.randint(5000, 25000)
    })

pd.DataFrame(specialty_stats).to_csv('data/specialty_performance.csv', index=False)

regions = ['North', 'South', 'East', 'West', 'Central', 'Northeast', 'Southwest']
regional_data = []
for region in regions:
    regional_data.append({
        'Region': region,
        'Hospitals': np.random.randint(5, 25),
        'TotalPatients': np.random.randint(50000, 150000),
        'AvgWaitTime': round(np.random.uniform(30, 120), 1),
        'Capacity': round(np.random.uniform(0.6, 0.95), 2)
    })

pd.DataFrame(regional_data).to_csv('data/regional_healthcare.csv', index=False)

age_profile_data = []
time_bands = ['0-3 Months', '3-6 Months', '6-9 Months', '9-12 Months', '12-15 Months', '15-18 Months']
for band in time_bands:
    for age in age_groups:
        age_profile_data.append({
            'TimeBand': band,
            'AgeGroup': age,
            'PatientCount': np.random.randint(500, 8000)
        })

pd.DataFrame(age_profile_data).to_csv('data/age_profile_analysis.csv', index=False)
print("Medical data generated")
