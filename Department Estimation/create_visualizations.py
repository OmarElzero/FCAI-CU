import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("=== CREATING DEPARTMENT ANALYSIS VISUALIZATIONS ===")

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Load and process data (same as main script)
print("Loading data...")
survey = pd.read_excel('Sample.xlsx')
main = pd.read_excel('corrected_student_data_20250807_171527.xlsx', sheet_name='All Data')

# Clean and filter data
survey['id'] = survey['id'].astype(str).str.strip()
survey = survey[survey['id'].str.startswith('2023')]

main['student_id'] = main['student_id'].astype(str).str.strip()
main_2023 = main[main['entry_year'].astype(str) == '2023']

# Process student data
course_counts = main_2023.groupby('student_id').size().reset_index(name='course_count')
course_counts['total_hours'] = course_counts['course_count'] * 3

# Get max GPA per student
gpa_per_student = main_2023.groupby('student_id')['gpa'].max().reset_index()

# Create student summary
student_summary = course_counts.merge(gpa_per_student, on='student_id')
eligible = student_summary[student_summary['total_hours'] >= 60].copy()

print(f"Working with {len(eligible)} eligible students")

# Get preference distribution from survey
survey_prefs = survey['Select your first preferred department. '].str.strip().str.upper()
pref_counts = survey_prefs.value_counts()
total_survey = len(survey_prefs.dropna())
pref_distribution = (pref_counts / total_survey).to_dict()

# Apply preference distribution to all students
eligible = eligible.sort_values('gpa', ascending=False).reset_index(drop=True)
total_eligible = len(eligible)
dept_targets = {}
for dept, ratio in pref_distribution.items():
    dept_targets[dept] = int(total_eligible * ratio)

# Assign preferences
eligible['pref1'] = None
start_idx = 0
for dept in ['IS', 'AI', 'CS', 'IT', 'DS']:
    if dept in dept_targets:
        end_idx = start_idx + dept_targets[dept]
        if end_idx > len(eligible):
            end_idx = len(eligible)
        eligible.loc[start_idx:end_idx-1, 'pref1'] = dept
        start_idx = end_idx

if start_idx < len(eligible):
    eligible.loc[start_idx:, 'pref1'] = 'DS'

# Calculate thresholds and realistic enrollment
thresholds = {'IS': 3.10, 'AI': 2.60, 'CS': 1.88, 'IT': 1.37, 'DS': 0.59}
dept_capacities = {'IT': 261, 'DS': 241, 'CS': 211, 'AI': 191, 'IS': 206}

# Simulate realistic enrollment
eligible_sorted = eligible.sort_values('gpa', ascending=False).copy()
eligible_sorted['assigned_dept'] = None
dept_enrolled = {dept: 0 for dept in dept_capacities.keys()}
dept_priority = ['IS', 'AI', 'CS', 'IT', 'DS']

for idx, student in eligible_sorted.iterrows():
    student_gpa = student['gpa']
    for dept in dept_priority:
        if student_gpa >= thresholds[dept] and dept_enrolled[dept] < dept_capacities[dept]:
            eligible_sorted.loc[idx, 'assigned_dept'] = dept
            dept_enrolled[dept] += 1
            break

print("Creating visualizations...")

# Create timestamp for file naming
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 1. GPA Distribution Chart
plt.figure(figsize=(14, 8))
plt.subplot(2, 2, 1)
plt.hist(eligible['gpa'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
plt.axvline(eligible['gpa'].mean(), color='red', linestyle='--', label=f'Mean: {eligible["gpa"].mean():.2f}')
plt.xlabel('GPA')
plt.ylabel('Number of Students')
plt.title('GPA Distribution of Eligible Students (≥60 hours)')
plt.legend()
plt.grid(True, alpha=0.3)

# 2. Department Preferences vs Reality
plt.subplot(2, 2, 2)
preference_counts = eligible['pref1'].value_counts()
reality_counts = eligible_sorted['assigned_dept'].value_counts()

x = np.arange(len(dept_priority))
width = 0.35

plt.bar(x - width/2, [preference_counts.get(dept, 0) for dept in dept_priority], 
        width, label='Survey Preferences', alpha=0.8)
plt.bar(x + width/2, [reality_counts.get(dept, 0) for dept in dept_priority], 
        width, label='Actual Enrollment', alpha=0.8)

plt.xlabel('Departments')
plt.ylabel('Number of Students')
plt.title('Preferences vs Reality')
plt.xticks(x, dept_priority)
plt.legend()
plt.grid(True, alpha=0.3)

# 3. GPA Thresholds Visualization
plt.subplot(2, 2, 3)
depts = list(thresholds.keys())
threshold_values = [thresholds[dept] for dept in depts]
colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']

bars = plt.bar(depts, threshold_values, color=colors, alpha=0.7, edgecolor='black')
plt.ylabel('Minimum GPA Required')
plt.title('Department Admission Thresholds')
plt.ylim(0, 4.0)

# Add value labels on bars
for bar, value in zip(bars, threshold_values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
             f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

plt.grid(True, alpha=0.3)

# 4. Capacity vs Demand
plt.subplot(2, 2, 4)
capacities = [dept_capacities[dept] for dept in dept_priority]
demands = [preference_counts.get(dept, 0) for dept in dept_priority]
enrolled = [reality_counts.get(dept, 0) for dept in dept_priority]

x = np.arange(len(dept_priority))
width = 0.25

plt.bar(x - width, capacities, width, label='Capacity', alpha=0.8)
plt.bar(x, demands, width, label='Demand (Survey)', alpha=0.8)
plt.bar(x + width, enrolled, width, label='Actual Enrolled', alpha=0.8)

plt.xlabel('Departments')
plt.ylabel('Number of Students')
plt.title('Capacity vs Demand vs Reality')
plt.xticks(x, dept_priority)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'department_analysis_overview_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: department_analysis_overview_{timestamp}.png")
plt.close()

# Create detailed GPA analysis chart
plt.figure(figsize=(16, 10))

# GPA ranges analysis
gpa_ranges = [
    (3.5, 4.0, "Excellent (3.5-4.0)"),
    (3.0, 3.5, "Very Good (3.0-3.5)"), 
    (2.5, 3.0, "Good (2.5-3.0)"),
    (2.0, 2.5, "Satisfactory (2.0-2.5)"),
    (1.5, 2.0, "Acceptable (1.5-2.0)"),
    (1.0, 1.5, "Pass (1.0-1.5)"),
    (0.0, 1.0, "Fail (0.0-1.0)")
]

# 1. GPA Ranges Pie Chart
plt.subplot(2, 3, 1)
range_counts = []
range_labels = []
for min_gpa, max_gpa, label in gpa_ranges:
    count = len(eligible[(eligible['gpa'] >= min_gpa) & (eligible['gpa'] < max_gpa)])
    if count > 0:
        range_counts.append(count)
        range_labels.append(f"{label}\n{count} students")

plt.pie(range_counts, labels=range_labels, autopct='%1.1f%%', startangle=90)
plt.title('GPA Distribution by Grade Categories')

# 2. Department GPA Boxplots
plt.subplot(2, 3, 2)
dept_gpas = []
dept_names = []
for dept in dept_priority:
    dept_students = eligible_sorted[eligible_sorted['assigned_dept'] == dept]
    if len(dept_students) > 0:
        dept_gpas.append(dept_students['gpa'].tolist())
        dept_names.append(f"{dept}\n({len(dept_students)})")

plt.boxplot(dept_gpas, labels=dept_names)
plt.ylabel('GPA')
plt.title('GPA Distribution by Department')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# 3. Qualification Analysis
plt.subplot(2, 3, 3)
qualified_counts = []
for dept, threshold in thresholds.items():
    qualified = len(eligible[eligible['gpa'] >= threshold])
    qualified_counts.append(qualified)

plt.bar(thresholds.keys(), qualified_counts, alpha=0.7, color='lightcoral')
plt.ylabel('Students Qualified')
plt.title('Students Qualifying for Each Department')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add value labels
for i, v in enumerate(qualified_counts):
    plt.text(i, v + 10, str(v), ha='center', va='bottom', fontweight='bold')

# 4. Competition Ratios
plt.subplot(2, 3, 4)
competition_ratios = []
dept_names_comp = []
for dept in dept_priority:
    demand = preference_counts.get(dept, 0)
    capacity = dept_capacities[dept]
    ratio = demand / capacity if capacity > 0 else 0
    competition_ratios.append(ratio)
    dept_names_comp.append(dept)

colors_comp = ['red' if r > 1.5 else 'orange' if r > 1 else 'green' for r in competition_ratios]
bars = plt.bar(dept_names_comp, competition_ratios, color=colors_comp, alpha=0.7)
plt.ylabel('Competition Ratio (Demand/Capacity)')
plt.title('Department Competition Levels')
plt.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Break-even')
plt.legend()
plt.grid(True, alpha=0.3)

# Add value labels
for bar, ratio in zip(bars, competition_ratios):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
             f'{ratio:.2f}:1', ha='center', va='bottom', fontweight='bold')

# 5. Actual vs Planned Thresholds
plt.subplot(2, 3, 5)
actual_mins = []
for dept in dept_priority:
    admitted = eligible_sorted[eligible_sorted['assigned_dept'] == dept]
    if len(admitted) > 0:
        actual_mins.append(admitted['gpa'].min())
    else:
        actual_mins.append(0)

planned_thresholds = [thresholds[dept] for dept in dept_priority]

x = np.arange(len(dept_priority))
width = 0.35

plt.bar(x - width/2, planned_thresholds, width, label='Planned Threshold', alpha=0.8)
plt.bar(x + width/2, actual_mins, width, label='Actual Min GPA', alpha=0.8)

plt.xlabel('Departments')
plt.ylabel('GPA')
plt.title('Planned vs Actual GPA Thresholds')
plt.xticks(x, dept_priority)
plt.legend()
plt.grid(True, alpha=0.3)

# 6. Summary Statistics Table
plt.subplot(2, 3, 6)
plt.axis('off')

# Create summary table data
table_data = []
for dept in dept_priority:
    admitted = eligible_sorted[eligible_sorted['assigned_dept'] == dept]
    capacity = dept_capacities[dept]
    enrolled = len(admitted)
    
    if len(admitted) > 0:
        min_gpa = admitted['gpa'].min()
        avg_gpa = admitted['gpa'].mean()
    else:
        min_gpa = 0
        avg_gpa = 0
    
    table_data.append([dept, f"{enrolled}/{capacity}", f"{min_gpa:.2f}", f"{avg_gpa:.2f}"])

table = plt.table(cellText=table_data,
                 colLabels=['Dept', 'Enrolled/Cap', 'Min GPA', 'Avg GPA'],
                 cellLoc='center',
                 loc='center',
                 bbox=[0, 0, 1, 1])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.5)
plt.title('Department Summary Statistics', pad=20)

plt.tight_layout()
plt.savefig(f'department_detailed_analysis_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: department_detailed_analysis_{timestamp}.png")
plt.close()

# Create a simple infographic-style summary
plt.figure(figsize=(14, 10))
plt.suptitle('FCAI-CU Department Admission Analysis 2023', fontsize=20, fontweight='bold', y=0.95)

# Key metrics in large text
plt.subplot(3, 4, 1)
plt.text(0.5, 0.5, f"{len(eligible)}", ha='center', va='center', fontsize=36, fontweight='bold', color='blue')
plt.text(0.5, 0.2, "Eligible Students", ha='center', va='center', fontsize=12)
plt.axis('off')

plt.subplot(3, 4, 2)
plt.text(0.5, 0.5, f"{eligible['gpa'].mean():.2f}", ha='center', va='center', fontsize=36, fontweight='bold', color='green')
plt.text(0.5, 0.2, "Average GPA", ha='center', va='center', fontsize=12)
plt.axis('off')

plt.subplot(3, 4, 3)
plt.text(0.5, 0.5, "5", ha='center', va='center', fontsize=36, fontweight='bold', color='purple')
plt.text(0.5, 0.2, "Departments", ha='center', va='center', fontsize=12)
plt.axis('off')

plt.subplot(3, 4, 4)
plt.text(0.5, 0.5, f"{sum(dept_capacities.values())}", ha='center', va='center', fontsize=36, fontweight='bold', color='orange')
plt.text(0.5, 0.2, "Total Capacity", ha='center', va='center', fontsize=12)
plt.axis('off')

# Department ranking by difficulty
plt.subplot(3, 2, 3)
dept_difficulty = sorted(thresholds.items(), key=lambda x: x[1], reverse=True)
y_pos = np.arange(len(dept_difficulty))
difficulty_values = [item[1] for item in dept_difficulty]
dept_labels = [item[0] for item in dept_difficulty]

colors_diff = ['darkred', 'red', 'orange', 'yellow', 'lightgreen']
plt.barh(y_pos, difficulty_values, color=colors_diff, alpha=0.8)
plt.yticks(y_pos, dept_labels)
plt.xlabel('Minimum GPA Required')
plt.title('Department Difficulty Ranking', fontweight='bold')
plt.grid(True, alpha=0.3)

# Add value labels
for i, v in enumerate(difficulty_values):
    plt.text(v + 0.05, i, f'{v:.2f}', va='center', fontweight='bold')

# Final enrollment pie chart
plt.subplot(3, 2, 4)
final_enrollment = [dept_enrolled[dept] for dept in dept_priority]
colors_pie = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
plt.pie(final_enrollment, labels=[f"{dept}\n{count}" for dept, count in zip(dept_priority, final_enrollment)], 
        autopct='%1.1f%%', colors=colors_pie, startangle=90)
plt.title('Final Student Distribution', fontweight='bold')

# Key insights text
plt.subplot(3, 1, 3)
plt.axis('off')
insights_text = f"""
KEY INSIGHTS:
• Most Competitive: IS (GPA ≥ 3.10) and AI (GPA ≥ 2.60) - High demand, limited capacity
• Most Accessible: DS (GPA ≥ 0.59) and IT (GPA ≥ 1.37) - Lower competition, more spots
• Biggest Surprise: DS has {241 - dept_enrolled['DS']} unfilled spots despite lowest requirements
• Reality Check: Many students end up in different departments than they prefer due to GPA limits
• Waterfall Effect: Better students "fall down" to lower-ranked departments when they can't qualify for top choices
"""

plt.text(0.05, 0.8, insights_text, transform=plt.gca().transAxes, fontsize=11, 
         verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5))

plt.tight_layout()
plt.savefig(f'department_summary_infographic_{timestamp}.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: department_summary_infographic_{timestamp}.png")
plt.close()

print("\n🎉 All visualizations created successfully!")
print("\nFiles generated:")
print(f"1. department_analysis_overview_{timestamp}.png - Comprehensive 4-chart overview")
print(f"2. department_detailed_analysis_{timestamp}.png - Detailed statistical analysis")
print(f"3. department_summary_infographic_{timestamp}.png - Easy-to-share summary")
print("\nYou can now share these PNG files with stakeholders!")
