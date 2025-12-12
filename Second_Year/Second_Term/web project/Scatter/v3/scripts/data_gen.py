import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

def generate_geographic_audience_data():
    """Generate geographic audience data for top countries"""
    
    # Top countries data based on the reference image
    countries_data = [
        {'country': 'United States', 'country_code': 'US', 'lat': 39.8283, 'lng': -98.5795},
        {'country': 'United Kingdom', 'country_code': 'GB', 'lat': 55.3781, 'lng': -3.4360},
        {'country': 'Canada', 'country_code': 'CA', 'lat': 56.1304, 'lng': -106.3468},
        {'country': 'Australia', 'country_code': 'AU', 'lat': -25.2744, 'lng': 133.7751},
        {'country': 'New Zealand', 'country_code': 'NZ', 'lat': -40.9006, 'lng': 174.8860},
        {'country': 'Germany', 'country_code': 'DE', 'lat': 51.1657, 'lng': 10.4515},
        {'country': 'France', 'country_code': 'FR', 'lat': 46.2276, 'lng': 2.2137},
        {'country': 'Netherlands', 'country_code': 'NL', 'lat': 52.1326, 'lng': 5.2913},
        {'country': 'Sweden', 'country_code': 'SE', 'lat': 60.1282, 'lng': 18.6435},
        {'country': 'Norway', 'country_code': 'NO', 'lat': 60.4720, 'lng': 8.4689},
        {'country': 'Denmark', 'country_code': 'DK', 'lat': 56.2639, 'lng': 9.5018},
        {'country': 'Belgium', 'country_code': 'BE', 'lat': 50.5039, 'lng': 4.4699},
        {'country': 'Switzerland', 'country_code': 'CH', 'lat': 46.8182, 'lng': 8.2275},
        {'country': 'Austria', 'country_code': 'AT', 'lat': 47.5162, 'lng': 14.5501},
        {'country': 'Japan', 'country_code': 'JP', 'lat': 36.2048, 'lng': 138.2529},
        {'country': 'South Korea', 'country_code': 'KR', 'lat': 35.9078, 'lng': 127.7669},
        {'country': 'Singapore', 'country_code': 'SG', 'lat': 1.3521, 'lng': 103.8198},
        {'country': 'Brazil', 'country_code': 'BR', 'lat': -14.2350, 'lng': -51.9253},
        {'country': 'Mexico', 'country_code': 'MX', 'lat': 23.6345, 'lng': -102.5528},
        {'country': 'India', 'country_code': 'IN', 'lat': 20.5937, 'lng': 78.9629}
    ]
    
    geographic_data = []
    
    # Generate realistic data distribution similar to reference
    base_users = [15500, 869, 1146, 19950, 900, 8200, 6500, 4200, 3100, 2800,
                  2100, 1800, 1600, 1200, 5200, 3800, 2200, 4100, 3600, 7200]
    
    base_sessions = [18600, 1050, 1380, 24000, 1080, 9800, 7800, 5100, 3700, 3400,
                     2500, 2200, 1900, 1450, 6200, 4600, 2650, 4900, 4300, 8600]
    
    for i, country in enumerate(countries_data):
        # Add some variation
        users_variation = np.random.uniform(0.9, 1.1)
        sessions_variation = np.random.uniform(0.9, 1.1)
        
        users = int(base_users[i] * users_variation)
        sessions = int(base_sessions[i] * sessions_variation)
        
        # Calculate average session duration (similar to reference values)
        avg_duration_base = [158.55, 97.96, 73.33, 64.85, 67.52, 145.2, 132.8,
                             125.4, 118.7, 112.3, 105.8, 98.6, 91.4, 87.2,
                             156.8, 149.3, 142.7, 138.9, 135.2, 162.1]
        
        avg_duration = avg_duration_base[i] + np.random.uniform(-10, 10)
        
        # Calculate metrics
        bounce_rate = np.random.uniform(0.35, 0.65)
        pages_per_session = np.random.uniform(1.8, 4.2)
        
        # Calculate percentages for top 5
        total_users_top5 = sum(base_users[:5])
        total_sessions_top5 = sum(base_sessions[:5])
        
        user_percentage = (users / total_users_top5 * 100) if i < 5 else 0
        session_percentage = (sessions / total_sessions_top5 * 100) if i < 5 else 0
        
        geographic_data.append({
            'country': country['country'],
            'country_code': country['country_code'],
            'lat': country['lat'],
            'lng': country['lng'],
            'users': users,
            'sessions': sessions,
            'avg_session_duration': round(avg_duration, 2),
            'bounce_rate': round(bounce_rate, 3),
            'pages_per_session': round(pages_per_session, 2),
            'user_percentage': round(user_percentage, 2) if i < 5 else 0,
            'session_percentage': round(session_percentage, 2) if i < 5 else 0,
            'is_top5_users': i < 5,
            'is_top5_sessions': i < 5
        })
    
    return pd.DataFrame(geographic_data)

def generate_time_series_data():
    """Generate time series data for geographic trends"""
    
    # Generate daily data for the last 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Top 5 countries for time series
    top_countries = ['United States', 'Australia', 'New Zealand', 'United Kingdom', 'Canada']
    
    time_series_data = []
    
    for date in dates:
        day_of_week = date.weekday()
        # Weekly pattern - higher traffic on weekdays
        weekly_factor = 1.2 if day_of_week < 5 else 0.8
        
        # Seasonal trend
        day_of_year = date.timetuple().tm_yday
        seasonal_factor = 1 + 0.2 * np.sin(day_of_year / 365 * 2 * np.pi)
        
        for i, country in enumerate(top_countries):
            base_traffic = [1200, 950, 85, 65, 110][i]  # Different base for each country
            
            # Apply patterns
            daily_users = int(base_traffic * weekly_factor * seasonal_factor * np.random.uniform(0.8, 1.2))
            daily_sessions = int(daily_users * np.random.uniform(1.1, 1.4))
            
            time_series_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'country': country,
                'users': daily_users,
                'sessions': daily_sessions,
                'bounce_rate': round(np.random.uniform(0.35, 0.65), 3),
                'avg_session_duration': round(np.random.uniform(60, 180), 2)
            })
    
    return pd.DataFrame(time_series_data)

def generate_detailed_metrics():
    """Generate detailed metrics for dashboard KPIs"""
    
    countries = ['United States', 'Australia', 'New Zealand', 'United Kingdom', 'Canada',
                'Germany', 'France', 'Netherlands', 'Sweden', 'Norway', 'Denmark',
                'Belgium', 'Switzerland', 'Austria', 'Japan', 'South Korea',
                'Singapore', 'Brazil', 'Mexico', 'India']
    
    detailed_data = []
    
    for country in countries:
        # Generate comprehensive metrics
        users = np.random.randint(500, 20000)
        sessions = int(users * np.random.uniform(1.1, 1.5))
        pageviews = int(sessions * np.random.uniform(2.1, 4.8))
        
        # E-commerce metrics
        transactions = int(sessions * np.random.uniform(0.02, 0.08))
        revenue = transactions * np.random.uniform(45, 250)
        
        # Engagement metrics
        avg_session_duration = np.random.uniform(45, 200)
        bounce_rate = np.random.uniform(0.25, 0.75)
        pages_per_session = pageviews / sessions
        
        detailed_data.append({
            'country': country,
            'users': users,
            'new_users': int(users * np.random.uniform(0.6, 0.9)),
            'sessions': sessions,
            'pageviews': pageviews,
            'pages_per_session': round(pages_per_session, 2),
            'avg_session_duration': round(avg_session_duration, 2),
            'bounce_rate': round(bounce_rate, 3),
            'transactions': transactions,
            'revenue': round(revenue, 2),
            'conversion_rate': round((transactions / sessions) * 100, 2),
            'revenue_per_user': round(revenue / users, 2)
        })
    
    return pd.DataFrame(detailed_data)

def main():
    """Generate all datasets"""
    
    print("Generating Geographic Audience Analytics datasets...")
    
    # Create data directory
    import os
    os.makedirs('data', exist_ok=True)
    
    # Generate and save datasets
    print("1. Generating geographic audience data...")
    geo_df = generate_geographic_audience_data()
    geo_df.to_csv('data/geographic_audience.csv', index=False)
    print(f"   ✓ Saved {len(geo_df)} country records")
    
    print("2. Generating time series data...")
    time_df = generate_time_series_data()
    time_df.to_csv('data/time_series_data.csv', index=False)
    print(f"   ✓ Saved {len(time_df)} daily records")
    
    print("3. Generating detailed metrics...")
    metrics_df = generate_detailed_metrics()
    metrics_df.to_csv('data/detailed_metrics.csv', index=False)
    print(f"   ✓ Saved {len(metrics_df)} detailed country metrics")
    
    # Print summary
    top5_users = geo_df.head(5)
    total_users = geo_df['users'].sum()
    total_sessions = geo_df['sessions'].sum()
    
    print(f"\nDataset Summary:")
    print(f"📊 Total Countries: {len(geo_df)}")
    print(f"👥 Total Users: {total_users:,}")
    print(f"📈 Total Sessions: {total_sessions:,}")
    print(f"🌍 Time Series Days: {len(time_df['date'].unique())}")
    
    print(f"\nTop 5 Countries by Users:")
    for _, country in top5_users.iterrows():
        print(f"   {country['country']}: {country['users']:,} users ({country['user_percentage']:.1f}%)")

if __name__ == "__main__":
    main()
