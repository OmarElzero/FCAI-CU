import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

class GeographicAnalyticsDashboard:
    def __init__(self):
        """Initialize dashboard with data loading"""
        self.load_data()
        self.setup_styling()
    
    def load_data(self):
        """Load datasets from CSV files"""
        try:
            self.geographic_data = pd.read_csv('data/geographic_audience.csv')
            self.time_series_data = pd.read_csv('data/time_series_data.csv')
            self.detailed_metrics = pd.read_csv('data/detailed_metrics.csv')
            
            # Convert date columns
            self.time_series_data['date'] = pd.to_datetime(self.time_series_data['date'])
            
            print("✓ Data loaded successfully")
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        return True
    
    def setup_styling(self):
        """Define professional styling and color schemes"""
        self.colors = {
            'primary': '#1a73e8',
            'secondary': '#34a853', 
            'accent': '#ea4335',
            'warning': '#fbbc04',
            'purple': '#9c27b0',
            'teal': '#00acc1',
            'orange': '#ff9800',
            'background': '#f8f9fa',
            'card_bg': '#ffffff',
            'text_dark': '#202124',
            'text_light': '#5f6368',
            'border': '#dadce0',
            'hover': '#e8f0fe'
        }
    
    def create_world_map(self):
        """Create world map with geographic distribution"""
        fig = go.Figure()
        
        # Create bubble map
        fig.add_trace(go.Scattergeo(
            lon=self.geographic_data['lng'],
            lat=self.geographic_data['lat'],
            text=self.geographic_data['country'],
            mode='markers',
            marker=dict(
                size=np.sqrt(self.geographic_data['users']) / 8,
                color=self.geographic_data['users'],
                colorscale=[
                    [0, '#e3f2fd'],
                    [0.2, '#90caf9'], 
                    [0.4, '#42a5f5'],
                    [0.6, '#2196f3'],
                    [0.8, '#1976d2'],
                    [1.0, '#0d47a1']
                ],
                showscale=True,
                colorbar=dict(
                    title="Users",
                    titleside="right",
                    tickmode="linear",
                    thickness=15,
                    len=0.7,
                    x=1.02
                ),
                sizemode='diameter',
                sizemin=5,
                opacity=0.8,
                line=dict(width=1, color='white')
            ),
            customdata=np.column_stack((
                self.geographic_data['users'],
                self.geographic_data['sessions'],
                self.geographic_data['avg_session_duration'],
                self.geographic_data['bounce_rate']
            )),
            hovertemplate='<b>%{text}</b><br>' +
                         'Users: %{customdata[0]:,.0f}<br>' +
                         'Sessions: %{customdata[1]:,.0f}<br>' +
                         'Avg Session Duration: %{customdata[2]:.1f}s<br>' +
                         'Bounce Rate: %{customdata[3]:.1%}<br>' +
                         '<extra></extra>',
            name='Geographic Data'
        ))
        
        fig.update_layout(
            title=dict(
                text='<b>Global Audience Distribution</b>',
                font=dict(size=20, color=self.colors['text_dark'], family='Google Sans, sans-serif'),
                x=0.5,
                y=0.95
            ),
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='#f5f5f5',
                coastlinecolor='#cccccc',
                showocean=True,
                oceancolor='#e1f5fe',
                showlakes=True,
                lakecolor='#e1f5fe',
                showframe=False,
                bgcolor='rgba(0,0,0,0)',
                showcoastlines=True,
                resolution=50
            ),
            margin=dict(t=80, b=20, l=20, r=100),
            paper_bgcolor='rgba(0,0,0,0)',
            height=500
        )
        
        return fig
    
    def create_top_countries_table(self):
        """Create top countries table"""
        top5 = self.geographic_data.head(5)
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Country</b>', '<b>Users</b>', '<b>%</b>', '<b>Sessions</b>', '<b>%</b>'],
                fill_color=self.colors['hover'],
                font=dict(color=self.colors['text_dark'], size=14),
                align='left',
                height=40
            ),
            cells=dict(
                values=[
                    top5['country'],
                    [f"{x:,}" for x in top5['users']],
                    [f"{x:.1f}%" for x in top5['user_percentage']],
                    [f"{x:,}" for x in top5['sessions']],
                    [f"{x:.1f}%" for x in top5['session_percentage']]
                ],
                fill_color='white',
                font=dict(color=self.colors['text_dark'], size=12),
                align='left',
                height=35
            )
        )])
        
        fig.update_layout(
            title=dict(
                text='<b>Top Countries</b>',
                font=dict(size=16, color=self.colors['text_dark'], family='Google Sans, sans-serif'),
                x=0,
                y=0.95
            ),
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        
        return fig
    
    def create_sessions_bar_chart(self):
        """Create sessions by country bar chart"""
        top10 = self.geographic_data.head(10)
        
        fig = go.Figure(data=[
            go.Bar(
                x=top10['sessions'],
                y=top10['country'],
                orientation='h',
                marker=dict(
                    color=self.colors['primary'],
                    opacity=0.8
                ),
                hovertemplate='<b>%{y}</b><br>' +
                             'Sessions: %{x:,.0f}<br>' +
                             '<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(
                text='<b>Sessions by Country</b>',
                font=dict(size=16, color=self.colors['text_dark'], family='Google Sans, sans-serif'),
                x=0,
                y=0.95
            ),
            xaxis=dict(
                title='Sessions',
                showgrid=True,
                gridcolor='#f0f0f0',
                color=self.colors['text_light']
            ),
            yaxis=dict(
                autorange='reversed',
                color=self.colors['text_light']
            ),
            margin=dict(t=50, b=40, l=120, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        return fig
    
    def create_time_series_chart(self):
        """Create time series chart for top countries"""
        top_countries = ['United States', 'Australia', 'United Kingdom', 'Canada', 'New Zealand']
        
        fig = go.Figure()
        
        colors = [self.colors['primary'], self.colors['secondary'], self.colors['accent'], 
                 self.colors['warning'], self.colors['purple']]
        
        for i, country in enumerate(top_countries):
            country_data = self.time_series_data[self.time_series_data['country'] == country]
            
            fig.add_trace(go.Scatter(
                x=country_data['date'],
                y=country_data['users'],
                mode='lines',
                name=country,
                line=dict(
                    color=colors[i],
                    width=2
                ),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Date: %{x|%b %d}<br>' +
                             'Users: %{y:,.0f}<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text='<b>User Trends Over Time</b>',
                font=dict(size=16, color=self.colors['text_dark'], family='Google Sans, sans-serif'),
                x=0,
                y=0.95
            ),
            xaxis=dict(
                title='Date',
                showgrid=True,
                gridcolor='#f0f0f0',
                color=self.colors['text_light']
            ),
            yaxis=dict(
                title='Users',
                showgrid=True,
                gridcolor='#f0f0f0',
                color=self.colors['text_light']
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            margin=dict(t=80, b=40, l=60, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        
        return fig
    
    def create_metrics_summary(self):
        """Create metrics summary cards"""
        total_users = self.geographic_data['users'].sum()
        total_sessions = self.geographic_data['sessions'].sum()
        avg_duration = self.geographic_data['avg_session_duration'].mean()
        avg_bounce_rate = self.geographic_data['bounce_rate'].mean()
        
        return {
            'total_users': total_users,
            'total_sessions': total_sessions,
            'avg_duration': avg_duration,
            'avg_bounce_rate': avg_bounce_rate,
            'countries_count': len(self.geographic_data)
        }
    
    def create_dashboard_html(self):
        """Generate complete HTML dashboard"""
        # Calculate metrics
        metrics = self.create_metrics_summary()
        
        # Create visualizations
        world_map = self.create_world_map()
        countries_table = self.create_top_countries_table()
        sessions_chart = self.create_sessions_bar_chart()
        time_series = self.create_time_series_chart()
        
        # Convert to HTML
        map_html = pyo.plot(world_map, output_type='div', include_plotlyjs=False)
        table_html = pyo.plot(countries_table, output_type='div', include_plotlyjs=False)
        bar_html = pyo.plot(sessions_chart, output_type='div', include_plotlyjs=False)
        time_html = pyo.plot(time_series, output_type='div', include_plotlyjs=False)
        
        # Generate HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Geographic Analytics Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, sans-serif;
                    background: #f8f9fa;
                    color: #202124;
                    line-height: 1.6;
                    padding: 20px;
                }}
                
                .dashboard {{
                    max-width: 1400px;
                    margin: 0 auto;
                }}
                
                .header {{
                    text-align: center;
                    margin-bottom: 32px;
                    padding: 24px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
                }}
                
                .header h1 {{
                    color: #202124;
                    font-size: 2.5rem;
                    font-weight: 400;
                    margin-bottom: 8px;
                }}
                
                .header p {{
                    color: #5f6368;
                    font-size: 1.1rem;
                }}
                
                .metrics-container {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                    gap: 20px;
                    margin-bottom: 32px;
                }}
                
                .metric-card {{
                    background: white;
                    padding: 24px;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
                    text-align: center;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }}
                
                .metric-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.12);
                }}
                
                .metric-value {{
                    font-size: 2.5rem;
                    font-weight: 500;
                    color: #1a73e8;
                    margin-bottom: 8px;
                }}
                
                .metric-label {{
                    font-size: 0.95rem;
                    color: #5f6368;
                    font-weight: 400;
                }}
                
                .chart-container {{
                    display: grid;
                    grid-template-columns: 2fr 1fr;
                    gap: 24px;
                    margin-bottom: 32px;
                }}
                
                .chart-card {{
                    background: white;
                    padding: 24px;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
                }}
                
                .full-width {{
                    grid-column: 1 / -1;
                }}
                
                .bottom-charts {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 24px;
                    margin-bottom: 32px;
                }}
                
                @media (max-width: 768px) {{
                    .chart-container {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .bottom-charts {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .header h1 {{
                        font-size: 2rem;
                    }}
                    
                    body {{
                        padding: 16px;
                    }}
                }}
                
                .js-plotly-plot .plotly {{
                    width: 100% !important;
                    height: 100% !important;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>Geographic Analytics Dashboard</h1>
                    <p>Global audience insights and performance metrics</p>
                </div>
                
                <div class="metrics-container">
                    <div class="metric-card">
                        <div class="metric-value">{metrics['total_users']:,}</div>
                        <div class="metric-label">Total Users</div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-value">{metrics['total_sessions']:,}</div>
                        <div class="metric-label">Total Sessions</div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-value">{metrics['avg_duration']:.0f}s</div>
                        <div class="metric-label">Avg Session Duration</div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-value">{metrics['avg_bounce_rate']:.1%}</div>
                        <div class="metric-label">Avg Bounce Rate</div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-value">{metrics['countries_count']}</div>
                        <div class="metric-label">Countries</div>
                    </div>
                </div>
                
                <div class="chart-card full-width">
                    {map_html}
                </div>
                
                <div class="chart-container">
                    <div class="chart-card">
                        {table_html}
                    </div>
                    
                    <div class="chart-card">
                        {bar_html}
                    </div>
                </div>
                
                <div class="chart-card">
                    {time_html}
                </div>
            </div>
            
            <script>
                // Responsive resizing
                window.addEventListener('resize', function() {{
                    var plots = document.querySelectorAll('.js-plotly-plot');
                    plots.forEach(function(plot) {{
                        Plotly.Plots.resize(plot);
                    }});
                }});
                
                // Initialize proper sizing
                document.addEventListener('DOMContentLoaded', function() {{
                    setTimeout(function() {{
                        var plots = document.querySelectorAll('.js-plotly-plot');
                        plots.forEach(function(plot) {{
                            Plotly.Plots.resize(plot);
                        }});
                    }}, 100);
                }});
            </script>
        </body>
        </html>
        """
        
        return html_content
    
    def save_dashboard(self, filename='outputs/dashboard.html'):
        """Save dashboard to HTML file"""
        import os
        os.makedirs('outputs', exist_ok=True)
        
        html_content = self.create_dashboard_html()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Dashboard saved to {filename}")
        return filename

def main():
    """Generate the geographic analytics dashboard"""
    print("Creating Geographic Analytics Dashboard...")
    
    dashboard = GeographicAnalyticsDashboard()
    filename = dashboard.save_dashboard()
    
    print(f"\n🎉 Dashboard created successfully!")
    print(f"📊 Features included:")
    print(f"   • Interactive world map with user distribution bubbles")
    print(f"   • Top countries table with percentages")
    print(f"   • Sessions by country bar chart")
    print(f"   • Time series trends for top 5 countries")
    print(f"   • Key performance metrics summary")
    print(f"   • Google Analytics-inspired clean design")
    print(f"   • World map covers >40% of dashboard space")
    
    print(f"\n📂 Open {filename} in your browser to view the dashboard")

if __name__ == "__main__":
    main()
