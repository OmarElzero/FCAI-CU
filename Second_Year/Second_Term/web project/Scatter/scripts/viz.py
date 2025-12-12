import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

df1 = pd.read_csv('data/delivery_times.csv')
df2 = pd.read_csv('data/delay_reasons.csv')
df3 = pd.read_csv('data/backlog.csv')
df4 = pd.read_csv('data/regional_performance.csv')
df5 = pd.read_csv('data/employee_data.csv')

os.makedirs('outputs', exist_ok=True)

fig = make_subplots(
    rows=3, cols=3,
    specs=[
        [{"type": "domain"}, {"type": "bar"}, {"type": "scatter"}],
        [{"type": "table"}, {"type": "xy"}, {"type": "bar"}],
        [{"type": "geo", "colspan": 3}, None, None]
    ],
    subplot_titles=(
        "Delivery Type Distribution", "Delay Reasons Analysis", "Performance by Department",
        "Key Metrics Summary", "Backlog Trend Over Time", "Regional Performance Stats",
        "Geographic Distribution by State"
    ),
    vertical_spacing=0.08,
    horizontal_spacing=0.05
)

delivery_counts = df1['DeliveryType'].value_counts()
fig.add_trace(go.Pie(
    labels=delivery_counts.index,
    values=delivery_counts.values,
    hole=0.5,
    marker_colors=['#3498db', '#e74c3c'],
    textinfo='percent+label',
    textfont_size=12
), row=1, col=1)

fig.add_trace(go.Bar(
    x=df2['Reason'],
    y=df2['Count'],
    marker_color=['#e74c3c', '#f39c12', '#3498db', '#9b59b6', '#2ecc71'],
    text=df2['Count'],
    textposition='outside'
), row=1, col=2)

dept_perf = df5.groupby('Department')['Rating'].mean().sort_values(ascending=False)
fig.add_trace(go.Scatter(
    x=dept_perf.values,
    y=list(range(len(dept_perf))),
    mode='markers',
    marker=dict(size=12, color='#3498db'),
    text=dept_perf.index,
    textposition='middle right'
), row=1, col=3)

metrics_data = [
    ['Total Orders', '2,000'],
    ['Same-Day %', '60%'],
    ['Avg Delivery Time', '8.5 hrs'],
    ['Peak Backlog', '955 orders'],
    ['Regional Score', '88.2%']
]

fig.add_trace(go.Table(
    header=dict(values=['Metric', 'Value'], fill_color='#34495e', font_color='white'),
    cells=dict(values=list(zip(*metrics_data)), fill_color='#ecf0f1')
), row=2, col=1)

df3['Date'] = pd.to_datetime(df3['Date'])
fig.add_trace(go.Scatter(
    x=df3['Date'],
    y=df3['BacklogOrders'],
    mode='lines+markers',
    line=dict(color='#e74c3c', width=2),
    marker=dict(size=4),
    name='Backlog'
), row=2, col=2)

region_stats = df4.groupby('Performance').size()
fig.add_trace(go.Bar(
    x=region_stats.index,
    y=region_stats.values,
    marker_color=['#2ecc71', '#f39c12', '#e74c3c']
), row=2, col=3)

state_data = df4.groupby('State').agg({
    'OrderVolume': 'sum',
    'DeliveryScore': 'mean'
}).reset_index()

fig.add_trace(go.Choropleth(
    locations=state_data['State'],
    z=state_data['OrderVolume'],
    locationmode='USA-states',
    colorscale='Blues',
    marker_line_color='white',
    marker_line_width=0.5,
    colorbar_title="Order Volume"
), row=3, col=1)

fig.update_layout(
    height=900,
    width=1400,
    title_text="Business Performance Dashboard",
    title_x=0.5,
    title_font_size=24,
    showlegend=False,
    font=dict(family="Arial", size=11),
    paper_bgcolor="white",
    plot_bgcolor="white"
)

fig.update_geos(
    scope='usa',
    projection_type='albers usa',
    showland=True,
    landcolor='rgb(243, 243, 243)',
    coastlinecolor='rgb(204, 204, 204)'
)

fig.write_html('outputs/golden_image.html')
print("Dashboard created")
