import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

print("=== PHASE 2: Department Admission Threshold Estimation ===")
print("DEBUG: Starting analysis with debug statements...")

# Load survey data
survey = pd.read_excel('Sample.xlsx')
main = pd.read_excel('corrected_student_data_20250807_171527.xlsx', sheet_name='All Data')

print(f"DEBUG: Survey raw data loaded: {len(survey)} entries")
print(f"DEBUG: Main dataset loaded: {len(main)} total records")
print(f"DEBUG: Unique students in main dataset: {main['student_id'].nunique()}")

# Check entry year distribution in main data
entry_year_dist = main['entry_year'].value_counts().sort_index()
print(f"DEBUG: Entry year distribution in main data:")
for year, count in entry_year_dist.head(10).items():
    print(f"  {year}: {count} records")

# Clean survey IDs and filter for 2023
survey['id'] = survey['id'].astype(str).str.strip()
print(f"DEBUG: Survey after ID cleaning: {len(survey)} entries")

survey = survey[survey['id'].str.startswith('2023')]
print(f"DEBUG: Survey entries with valid 2023 IDs: {len(survey)}")

# Show sample of survey IDs
print(f"DEBUG: Sample survey IDs: {survey['id'].head(10).tolist()}")

# Get only 2023 entry year students from main data
main['student_id'] = main['student_id'].astype(str).str.strip()
main_2023 = main[main['entry_year'].astype(str) == '2023']
print(f"DEBUG: 2023 students in main dataset: {main_2023['student_id'].nunique()} unique students")
print(f"DEBUG: 2023 records in main dataset: {len(main_2023)} total records")

# Show sample of main dataset student IDs
sample_main_ids = main_2023['student_id'].unique()[:10]
print(f"DEBUG: Sample main dataset IDs: {sample_main_ids.tolist()}")

# Calculate total credit hours per student (assuming 3 credits per course)
course_counts = main_2023.groupby('student_id').size().reset_index(name='course_count')
course_counts['total_hours'] = course_counts['course_count'] * 3

print(f"DEBUG: Students with course data: {len(course_counts)}")
print(f"DEBUG: Course count distribution:")
print(f"  Min courses: {course_counts['course_count'].min()}")
print(f"  Max courses: {course_counts['course_count'].max()}")
print(f"  Mean courses: {course_counts['course_count'].mean():.1f}")

# Get max GPA per student
gpa_per_student = main_2023.groupby('student_id')['gpa'].max().reset_index()

# Create student summary
student_summary = course_counts.merge(gpa_per_student, on='student_id')
print(f"DEBUG: Student summary created: {len(student_summary)} students")
print(f"Total hours distribution: min={student_summary['total_hours'].min()}, max={student_summary['total_hours'].max()}, mean={student_summary['total_hours'].mean():.1f}")

# Show how many students have different hour thresholds
for threshold in [30, 45, 60, 75, 90]:
    count = len(student_summary[student_summary['total_hours'] >= threshold])
    print(f"DEBUG: Students with >={threshold} hours: {count}")

    # Step 6: Analyze survey to get department preference distributions
    print("DEBUG: Analyzing survey preferences to get distribution patterns...")
    survey_prefs = survey['Select your first preferred department. '].str.strip().str.upper()
    
    # Get preference distribution from survey sample
    pref_counts = survey_prefs.value_counts()
    total_survey = len(survey_prefs.dropna())
    pref_distribution = (pref_counts / total_survey).to_dict()
    
    print(f"DEBUG: Survey preference distribution:")
    for dept, ratio in pref_distribution.items():
        print(f"  {dept}: {ratio:.3f} ({pref_counts[dept]} out of {total_survey})")
    
    # Step 7: Apply preference distribution to ALL 2023 students
    print(f"DEBUG: Applying preference patterns to all {len(student_summary)} students...")
    
    # Filter students with sufficient credit hours first
    eligible = student_summary[student_summary['total_hours'] >= 60].copy()
    print(f"DEBUG: Students with >=60 hours: {len(eligible)}")
    
    # Assign departments based on GPA ranking and preference distribution
    # Sort by GPA (highest first) for fair distribution
    eligible = eligible.sort_values('gpa', ascending=False).reset_index(drop=True)
    
    # Calculate how many students should prefer each department
    total_eligible = len(eligible)
    dept_targets = {}
    for dept, ratio in pref_distribution.items():
        dept_targets[dept] = int(total_eligible * ratio)
    
    print(f"DEBUG: Target students per department (based on survey patterns):")
    for dept, count in dept_targets.items():
        print(f"  {dept}: {count} students")
    
    # Assign preferences to students based on distribution
    eligible['pref1'] = None
    start_idx = 0
    
    # Distribute students to departments based on preference ratios
    for dept in ['IS', 'AI', 'CS', 'IT', 'DS']:  # Order by survey popularity
        if dept in dept_targets:
            end_idx = start_idx + dept_targets[dept]
            if end_idx > len(eligible):
                end_idx = len(eligible)
            eligible.loc[start_idx:end_idx-1, 'pref1'] = dept
            start_idx = end_idx
    
    # Handle any remaining students (assign to least popular department)
    if start_idx < len(eligible):
        eligible.loc[start_idx:, 'pref1'] = 'DS'  # Least popular in survey

    # Departments
    departments = ['AI', 'CS', 'IT', 'DS', 'IS']

    # Show final preference distribution
    print(f"DEBUG: Final preference distribution for {len(eligible)} eligible students:")
    pref_values = eligible['pref1'].value_counts()
    for pref, count in pref_values.items():
        print(f"  '{pref}': {count}")

    print(f"Eligible students with assigned preferences: {len(eligible)}")

# Show preference distribution
print("\nFirst preference distribution:")
pref_dist = eligible['pref1'].value_counts()
for dept in departments:
    count = pref_dist.get(dept, 0)
    print(f"  {dept}: {count} students")

# Calculate department capacities
n_eligible = len(eligible)
base_capacity = n_eligible // len(departments)
print(f"\nBase capacity per department: {base_capacity}")

# Capacity allocation: IT +30%, DS +20%, CS/AI/IS ±10
capacities = {
    'IT': int(base_capacity * 1.3),  # +30%
    'DS': int(base_capacity * 1.2),  # +20%
    'CS': base_capacity + 10,        # +10
    'AI': base_capacity - 10,        # -10
    'IS': base_capacity + 5          # +5 to balance
}

print("\nDepartment capacities:")
for dept, cap in capacities.items():
    print(f"  {dept}: {cap} students")

# Estimate admission thresholds
print("\n=== ADMISSION THRESHOLD ESTIMATES ===")
results = {}

for dept in departments:
    # Get students who want this department as first preference
    dept_candidates = eligible[eligible['pref1'] == dept].copy()
    dept_candidates = dept_candidates.sort_values('gpa', ascending=False)
    
    # Take top candidates based on capacity
    capacity = capacities[dept]
    admitted = dept_candidates.head(capacity) if len(dept_candidates) >= capacity else dept_candidates
    
    # Calculate threshold
    if len(admitted) > 0:
        threshold_gpa = admitted['gpa'].min()
        avg_gpa = admitted['gpa'].mean()
    else:
        threshold_gpa = avg_gpa = None
    
    results[dept] = {
        'capacity': capacity,
        'applicants': len(dept_candidates),
        'admitted': len(admitted),
        'threshold_gpa': round(threshold_gpa, 2) if threshold_gpa else None,
        'avg_admitted_gpa': round(avg_gpa, 2) if avg_gpa else None,
        'competition_ratio': round(len(dept_candidates) / capacity, 2) if capacity > 0 else 0
    }
    
    print(f"\n{dept} Department:")
    print(f"  Capacity: {capacity}")
    print(f"  Applicants: {len(dept_candidates)}")
    print(f"  Admitted: {len(admitted)}")
    print(f"  Competition ratio: {results[dept]['competition_ratio']}:1")
    print(f"  GPA threshold: {threshold_gpa}")
    print(f"  Average admitted GPA: {avg_gpa}")

print("\n=== SUMMARY ===")
print("Expected admission thresholds based on preferences and capacity:")
for dept in departments:
    info = results[dept]
    print(f"{dept}: GPA ≥ {info['threshold_gpa']}, {info['competition_ratio']}:1 competition")

print("\n=== ACTUAL STUDENT DISTRIBUTION ANALYSIS ===")
print("Based on GPA thresholds, how many students would qualify for each department:")

# Count students who meet each department's GPA threshold
thresholds = {
    'IS': 3.10,
    'AI': 2.60, 
    'CS': 1.88,
    'IT': 1.37,
    'DS': 0.59
}

print("\n=== STUDENTS QUALIFYING FOR EACH DEPARTMENT ===")
for dept, threshold in thresholds.items():
    qualified = eligible[eligible['gpa'] >= threshold]
    print(f"{dept}: {len(qualified)} students qualify (GPA ≥ {threshold})")

print(f"\n=== GPA DISTRIBUTION ANALYSIS ===")
gpa_ranges = [
    (3.5, 4.0, "Excellent (3.5-4.0)"),
    (3.0, 3.5, "Very Good (3.0-3.5)"), 
    (2.5, 3.0, "Good (2.5-3.0)"),
    (2.0, 2.5, "Satisfactory (2.0-2.5)"),
    (1.5, 2.0, "Acceptable (1.5-2.0)"),
    (1.0, 1.5, "Pass (1.0-1.5)"),
    (0.0, 1.0, "Fail (0.0-1.0)")
]

for min_gpa, max_gpa, label in gpa_ranges:
    count = len(eligible[(eligible['gpa'] >= min_gpa) & (eligible['gpa'] < max_gpa)])
    percentage = (count / len(eligible)) * 100
    print(f"{label}: {count} students ({percentage:.1f}%)")

print(f"\n=== REALISTIC DEPARTMENT ENROLLMENT ===")
print("If students choose departments based on what they can qualify for:")

# Simulate realistic department assignment based on GPA qualification
# Students will choose the best department they qualify for
eligible_sorted = eligible.sort_values('gpa', ascending=False).copy()
eligible_sorted['assigned_dept'] = None

dept_capacities = {'IT': 261, 'DS': 241, 'CS': 211, 'AI': 191, 'IS': 206}
dept_enrolled = {dept: 0 for dept in dept_capacities.keys()}

# Department preference order (best to worst perceived)
dept_priority = ['IS', 'AI', 'CS', 'IT', 'DS']

for idx, student in eligible_sorted.iterrows():
    student_gpa = student['gpa']
    
    # Find the best department this student qualifies for that still has capacity
    for dept in dept_priority:
        if student_gpa >= thresholds[dept] and dept_enrolled[dept] < dept_capacities[dept]:
            eligible_sorted.loc[idx, 'assigned_dept'] = dept
            dept_enrolled[dept] += 1
            break

# Show final enrollment
print("\nFinal realistic enrollment:")
for dept in dept_priority:
    capacity = dept_capacities[dept]
    enrolled = dept_enrolled[dept]
    threshold_used = thresholds[dept]
    
    # Find actual GPA threshold used (minimum GPA of admitted students)
    admitted = eligible_sorted[eligible_sorted['assigned_dept'] == dept]
    if len(admitted) > 0:
        actual_min_gpa = admitted['gpa'].min()
        actual_avg_gpa = admitted['gpa'].mean()
        print(f"{dept}: {enrolled}/{capacity} students enrolled")
        print(f"    Planned threshold: {threshold_used}, Actual min GPA: {actual_min_gpa:.2f}")
        print(f"    Average admitted GPA: {actual_avg_gpa:.2f}")
    else:
        print(f"{dept}: {enrolled}/{capacity} students enrolled (no students)")

unassigned = len(eligible_sorted[eligible_sorted['assigned_dept'].isna()])
print("\n" + "="*60)
print("CALIBRATION: USING 2022 DATA TO PREDICT 2023 THRESHOLDS")
print("="*60)

# Actual 2022 data provided by user (for calibration)
actual_2022_data = {
    'IS': {'threshold': 3.04, 'enrolled': 185},  # 180-190 average
    'CS': {'threshold': 2.95, 'enrolled': 178},
    'AI': {'threshold': 2.24, 'enrolled': 400},
    'IT': {'threshold': 1.74, 'enrolled': 115},  # 110-120 average
    'DS': {'threshold': 1.69, 'enrolled': 140}
}

print("USING 2022 ACTUAL ENROLLMENT AS BASELINE:")
print("(To predict 2023 admission thresholds)")
print(f"{'Dept':<4} {'2022 Enrolled':<12} {'2022 Threshold':<12} {'Program Notes'}")
print("-" * 65)

for dept in ['AI', 'IS', 'CS', 'DS', 'IT']:  # Order by 2022 enrollment size
    enrolled_2022 = actual_2022_data[dept]['enrolled']
    thresh_2022 = actual_2022_data[dept]['threshold']
    
    if dept == 'AI':
        note = "Largest program (400 students)"
    elif dept == 'IS':
        note = "High-tier, selective program"
    elif dept == 'CS':
        note = "Traditional, competitive program"
    elif dept == 'DS':
        note = "Emerging field, moderate size"
    else:  # IT
        note = "Practical program, smaller intake"
    
    print(f"{dept:<4} {enrolled_2022:<12} {thresh_2022:<12} {note}")

total_2022 = sum(actual_2022_data[dept]['enrolled'] for dept in actual_2022_data)
print(f"\nTotal 2022 enrollment: {total_2022} students")

print("\n" + "="*60)
print("2023 THRESHOLD PREDICTIONS")
print("="*60)

print("Using 2022 enrollment patterns + 2023 student preferences + 2023 student GPA data...")

# Use 2022 enrollment as baseline capacity for 2023
capacity_2023 = {dept: actual_2022_data[dept]['enrolled'] for dept in actual_2022_data}

# Assume slight growth for 2023 (2-3% typical annual growth)
growth_factor = 1.025
total_2022_capacity = sum(capacity_2023.values())
target_2023_capacity = int(total_2022_capacity * growth_factor)
additional_spots = target_2023_capacity - total_2022_capacity

print(f"2022 baseline capacity: {total_2022_capacity}")
print(f"2023 estimated capacity: {target_2023_capacity} (+{additional_spots} spots)")

# Distribute additional spots based on typical growth patterns
if additional_spots > 0:
    # AI typically grows most, followed by emerging fields
    growth_distribution = {
        'AI': 0.4,   # AI field expanding rapidly
        'DS': 0.25,  # Data Science growing
        'IS': 0.15,  # Information Systems steady growth
        'CS': 0.15,  # Computer Science steady
        'IT': 0.05   # IT more stable
    }
    
    for dept, portion in growth_distribution.items():
        extra_spots = int(additional_spots * portion)
        capacity_2023[dept] += extra_spots

print(f"\n2023 ESTIMATED DEPARTMENT CAPACITIES:")
for dept in ['AI', 'IS', 'CS', 'DS', 'IT']:  # Order by size
    capacity = capacity_2023[dept]
    growth = capacity - actual_2022_data[dept]['enrolled']
    percentage = (capacity / sum(capacity_2023.values())) * 100
    print(f"  {dept}: {capacity} students (+{growth}) - {percentage:.1f}% of total")

print(f"\nTotal 2023 estimated capacity: {sum(capacity_2023.values())} students")

# Calculate 2023 thresholds using current student data and 2023 survey preferences
print(f"\n2023 ADMISSION THRESHOLD PREDICTIONS:")
print("Based on 2023 student GPA distribution and preference patterns...")

predicted_2023 = {}

for dept in ['IS', 'CS', 'AI', 'IT', 'DS']:
    # Get students who would prefer this department
    dept_candidates = eligible[eligible['pref1'] == dept].copy()
    dept_candidates = dept_candidates.sort_values('gpa', ascending=False)
    
    capacity = capacity_2023[dept]
    
    # Take top students up to capacity
    if len(dept_candidates) >= capacity:
        admitted = dept_candidates.head(capacity)
        threshold_gpa = admitted['gpa'].min()
    else:
        # Not enough direct applicants - program will likely fill with lower preference students
        # This suggests lower competition and threshold
        all_students = eligible.sort_values('gpa', ascending=False)
        admitted = all_students.head(capacity)
        threshold_gpa = admitted['gpa'].min() if len(admitted) > 0 else 0
    
    avg_gpa = admitted['gpa'].mean() if len(admitted) > 0 else 0
    competition = len(dept_candidates) / capacity if capacity > 0 else 0
    
    predicted_2023[dept] = {
        'threshold_gpa': threshold_gpa,
        'avg_gpa': avg_gpa,
        'competition_ratio': competition,
        'capacity': capacity,
        'direct_applicants': len(dept_candidates),
        'total_qualified': len(eligible[eligible['gpa'] >= threshold_gpa])
    }
    
    # Compare with 2022
    thresh_2022 = actual_2022_data[dept]['threshold']
    threshold_change = threshold_gpa - thresh_2022
    change_direction = "↗️" if threshold_change > 0.1 else "↘️" if threshold_change < -0.1 else "➡️"
    
    print(f"\n{dept} Department - 2023 Prediction:")
    print(f"  2022 threshold: {thresh_2022} GPA")
    print(f"  2023 predicted: {threshold_gpa:.2f} GPA {change_direction}")
    print(f"  Change: {threshold_change:+.2f}")
    print(f"  Capacity: {capacity} ({actual_2022_data[dept]['enrolled']} in 2022)")
    print(f"  Survey applicants: {len(dept_candidates)}")
    print(f"  Competition: {competition:.2f}:1")
    print(f"  Students qualifying: {len(eligible[eligible['gpa'] >= threshold_gpa])}")

print(f"\n" + "="*60)
print("2023 ADMISSION REQUIREMENTS SUMMARY")
print("="*60)

# Sort by threshold (hardest to easiest)
sorted_depts = sorted(predicted_2023.items(), key=lambda x: x[1]['threshold_gpa'], reverse=True)

print("📋 2023 Department Rankings (by admission difficulty):")
print()

for i, (dept, data) in enumerate(sorted_depts, 1):
    threshold = data['threshold_gpa']
    capacity = data['capacity']
    competition = data['competition_ratio']
    qualified = data['total_qualified']
    
    # Determine competitiveness
    if competition > 1.5:
        comp_level = "🔴 HIGHLY COMPETITIVE"
    elif competition > 1.0:
        comp_level = "🟡 COMPETITIVE"
    elif competition > 0.7:
        comp_level = "🟢 MODERATE"
    else:
        comp_level = "🟢 ACCESSIBLE"
    
    # Compare with 2022
    thresh_2022 = actual_2022_data[dept]['threshold']
    change = threshold - thresh_2022
    
    print(f"{i}. {dept} Department:")
    print(f"   GPA Required: {threshold:.2f} (was {thresh_2022} in 2022)")
    print(f"   Status: {comp_level}")
    print(f"   Capacity: {capacity} students")
    print(f"   Students qualifying: {qualified}/{len(eligible)} ({qualified/len(eligible)*100:.1f}%)")
    print()

print(f"🎯 KEY INSIGHTS FOR 2023 ADMISSIONS:")

# Analyze trends
print("\n📈 COMPETITIVENESS CHANGES FROM 2022:")
increases = []
decreases = []
stable = []

for dept in predicted_2023:
    change = predicted_2023[dept]['threshold_gpa'] - actual_2022_data[dept]['threshold']
    if change > 0.15:
        increases.append((dept, change))
    elif change < -0.15:
        decreases.append((dept, change))
    else:
        stable.append((dept, change))

if increases:
    print("   Getting HARDER:")
    for dept, change in sorted(increases, key=lambda x: x[1], reverse=True):
        print(f"     {dept}: +{change:.2f} GPA points")

if decreases:
    print("   Getting EASIER:")
    for dept, change in sorted(decreases, key=lambda x: x[1]):
        print(f"     {dept}: {change:.2f} GPA points")

if stable:
    print("   SIMILAR to 2022:")
    for dept, change in stable:
        print(f"     {dept}: {change:+.2f} GPA points")

print(f"\n💡 STUDENT GUIDANCE FOR 2023:")
print("   • High achievers (3.0+): Focus on IS, AI, or CS")
print("   • Good students (2.5+): AI and CS are accessible")  
print("   • Average students (2.0+): Consider IT and DS")
print("   • All students: AI has largest capacity with reasonable requirements")

print(f"\n📊 CAPACITY UTILIZATION:")
total_capacity = sum(capacity_2023.values())
total_eligible = len(eligible)
utilization = (total_capacity / total_eligible) * 100
print(f"   Total capacity: {total_capacity} students")
print(f"   Eligible students: {total_eligible}")
print(f"   Capacity utilization: {utilization:.1f}%")

if utilization > 100:
    print("   ✅ Sufficient capacity for all eligible students")
else:
    print("   ⚠️  More eligible students than available spots")

# Run multiple simulations with different capacity distributions
print("\n=== SIMULATION RESULTS ===")
print("Testing different capacity scenarios:")

scenarios = [
    {"name": "Current", "IT": 1.3, "DS": 1.2, "CS": 10, "AI": -10, "IS": 5},
    {"name": "Higher IT demand", "IT": 1.4, "DS": 1.1, "CS": 5, "AI": -5, "IS": 0},
    {"name": "Higher DS demand", "IT": 1.2, "DS": 1.4, "CS": 0, "AI": -5, "IS": -5}
]

for scenario in scenarios:
    print(f"\n--- {scenario['name']} Scenario ---")
    
    # Calculate capacities for this scenario
    sim_capacities = {
        'IT': int(base_capacity * scenario['IT']) if scenario['IT'] > 1 else base_capacity + scenario['IT'],
        'DS': int(base_capacity * scenario['DS']) if scenario['DS'] > 1 else base_capacity + scenario['DS'],
        'CS': base_capacity + scenario['CS'],
        'AI': base_capacity + scenario['AI'],
        'IS': base_capacity + scenario['IS']
    }
    
    print("Capacities:", sim_capacities)
    
    for dept in departments:
        dept_candidates = eligible[eligible['pref1'] == dept].copy()
        dept_candidates = dept_candidates.sort_values('gpa', ascending=False)
        
        capacity = sim_capacities[dept]
        admitted = dept_candidates.head(capacity) if len(dept_candidates) >= capacity else dept_candidates
        
        if len(admitted) > 0:
            threshold_gpa = admitted['gpa'].min()
            competition = len(dept_candidates) / capacity if capacity > 0 else 0
            print(f"  {dept}: GPA ≥ {threshold_gpa:.2f}, {competition:.2f}:1 competition")
        else:
            print(f"  {dept}: No applicants")
