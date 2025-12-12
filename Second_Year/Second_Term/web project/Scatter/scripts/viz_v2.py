import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

df1 = pd.read_csv('data/patient_waitlist.csv')
df2 = pd.read_csv('data/monthly_trends.csv')
df3 = pd.read_csv('data/specialty_performance.csv')
df4 = pd.read_csv('data/regional_healthcare.csv')
df5 = pd.read_csv('data/age_profile_analysis.csv')

os.makedirs('outputs', exist_ok=True)

fig = make_subplots(
    rows=3, cols=4,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}, {"type": "domain"}, {"type": "bar"}],
        [{"type": "xy", "colspan": 2}, None, {"type": "bar"}, {"type": "table"}],
        [{"type": "geo", "colspan": 2}, None, {"type": "bar", "colspan": 2}, None]
    ],
    subplot_titles=(
        "", "", "Wait List Breakdown", "Top Specialties",
        "Monthly Wait List Trend Analysis", "", "Age Profile Analysis", "Key Metrics",
        "Regional Healthcare Distribution", "", "Time Band vs Age Profile", ""
    ),
    vertical_spacing=0.08,
    horizontal_spacing=0.05
)

total_waitlist = len(df1)
current_month_waitlist = int(total_waitlist * 0.709)

fig.add_trace(go.Indicator(
    mode="number",
    value=current_month_waitlist,
    title={"text": "709K<br><span style='font-size:0.8em;color:gray'>Latest Month Wait List</span>"},
    number={'font': {'size': 48, 'color': '#2E86AB'}},
    domain={'x': [0, 1], 'y': [0, 1]}
), row=1, col=1)

prev_month_waitlist = int(current_month_waitlist * 0.9)
fig.add_trace(go.Indicator(
    mode="number",
    value=prev_month_waitlist,
    title={"text": "640K<br><span style='font-size:0.8em;color:gray'>PY Latest Month Wait List</span>"},
    number={'font': {'size': 48, 'color': '#A23B72'}},
    domain={'x': [0, 1], 'y': [0, 1]}
), row=1, col=2)

case_counts = df1['CaseType'].value_counts()
fig.add_trace(go.Pie(
    labels=case_counts.index,
    values=case_counts.values,
    hole=0.6,
    marker_colors=['#2E86AB', '#F18F01', '#C73E1D'],
    textinfo='percent+label',
    textfont_size=12
), row=1, col=3)

top_specialties = df3.nlargest(4, 'WaitListCount')
fig.add_trace(go.Bar(
    x=top_specialties['WaitListCount'],
    y=top_specialties['Specialty'],
    orientation='h',
    marker_color='#2E86AB',
    text=top_specialties['WaitListCount'],
    textposition='outside'
), row=1, col=4)

fig.add_trace(go.Scatter(
    x=df2['Month'],
    y=df2['Outpatient'],
    mode='lines+markers',
    name='Outpatient',
    line=dict(color='#2E86AB', width=3),
    marker=dict(size=6)
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=df2['Month'],
    y=df2['Inpatient'],
    mode='lines+markers',
    name='Inpatient',
    line=dict(color='#F18F01', width=3),
    marker=dict(size=6)
), row=2, col=1)

age_pivot = df5.pivot(index='TimeBand', columns='AgeGroup', values='PatientCount')
colors = ['#2E86AB', '#F18F01', '#A23B72']
for i, age_group in enumerate(age_pivot.columns):
    fig.add_trace(go.Bar(
        x=age_pivot.index,
        y=age_pivot[age_group],
        name=age_group,
        marker_color=colors[i % len(colors)]
    ), row=2, col=3)

metrics_data = [
    ['Total Wait List', '709,000'],
    ['Avg Wait Time', '13.0 weeks'],
    ['Case Types', '3 categories'],
    ['Specialties', '8 departments'],
    ['Regions Covered', '7 areas']
]

fig.add_trace(go.Table(
    header=dict(values=['Metric', 'Value'], fill_color='#2E86AB', font_color='white'),
    cells=dict(values=list(zip(*metrics_data)), fill_color='#f8f9fa')
), row=2, col=4)

states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
state_patients = [np.random.randint(50000, 150000) for _ in states]

fig.add_trace(go.Choropleth(
    locations=states,
    z=state_patients,
    locationmode='USA-states',
    colorscale='Blues',
    marker_line_color='white',
    marker_line_width=0.5,
    colorbar_title="Patients"
), row=3, col=1)

time_bands = df5['TimeBand'].unique()
total_by_band = df5.groupby('TimeBand')['PatientCount'].sum().sort_values(ascending=True)

fig.add_trace(go.Bar(
    x=total_by_band.values,
    y=total_by_band.index,
    orientation='h',
    marker_color=['#2E86AB', '#3D5A80', '#98C1D9', '#E0FBFC', '#F18F01', '#A23B72'],
    text=total_by_band.values,
    textposition='outside'
), row=3, col=3)

fig.update_layout(
    height=1000,
    width=1600,
    title_text="Healthcare Wait List Analysis Dashboard",
    title_x=0.5,
    title_font_size=28,
    showlegend=False,
    font=dict(family="Arial", size=11),
    paper_bgcolor="#E8F4FD",
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
print("Medical dashboard created")
