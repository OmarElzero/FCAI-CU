import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs('data', exist_ok=True)

delivery_data = []
for i in range(2000):
    dtype = np.random.choice(['Same-Day', 'Two-Day'], p=[0.6, 0.4])
    if dtype == 'Same-Day':
        time_val = np.random.gamma(2, 3)
    else:
        time_val = np.random.gamma(8, 5)
    
    delivery_data.append({
        'OrderID': f'ORD{i+1:04d}',
        'DeliveryType': dtype,
        'DeliveryTime': round(time_val, 1)
    })

pd.DataFrame(delivery_data).to_csv('data/delivery_times.csv', index=False)

delay_data = pd.DataFrame({
    'Reason': ['Weather', 'Traffic', 'Sorting Error', 'Customer Not Home', 'System Glitch'],
    'Count': [400, 290, 180, 120, 60]
})
delay_data.to_csv('data/delay_reasons.csv', index=False)

dates = pd.date_range('2024-12-01', '2024-12-31', freq='D')
backlog_data = []
for date in dates:
    if date.day < 20:
        base = 300 + (date.day * 20)
    else:
        base = 700 - ((date.day - 20) * 50)
    backlog_data.append({
        'Date': date.strftime('%Y-%m-%d'),
        'BacklogOrders': max(50, base + np.random.randint(-50, 50))
    })

pd.DataFrame(backlog_data).to_csv('data/backlog.csv', index=False)

cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
lats = [40.7128, 34.0522, 41.8781, 29.7604, 33.4484, 39.9526, 29.4241, 32.7157, 32.7767, 37.3382]
lons = [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740, -75.1652, -98.4936, -117.1611, -96.7970, -121.8863]

regional_data = []
for i, city in enumerate(cities):
    regional_data.append({
        'City': city,
        'State': ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA'][i],
        'Lat': lats[i],
        'Lon': lons[i],
        'OrderVolume': np.random.randint(800, 2500),
        'DeliveryScore': round(np.random.uniform(75, 95), 1),
        'Performance': np.random.choice(['High', 'Medium', 'Low'], p=[0.4, 0.4, 0.2])
    })

pd.DataFrame(regional_data).to_csv('data/regional_performance.csv', index=False)

salary_data = []
departments = ['Operations', 'Logistics', 'Customer Service', 'IT', 'Management']
for dept in departments:
    for i in range(np.random.randint(50, 200)):
        salary_data.append({
            'Department': dept,
            'Salary': np.random.normal(75000, 15000),
            'Rating': np.random.randint(1, 6),
            'Group': np.random.choice(['Entry', 'Mid', 'Senior'], p=[0.3, 0.5, 0.2])
        })

pd.DataFrame(salary_data).to_csv('data/employee_data.csv', index=False)
print("Data files created")
