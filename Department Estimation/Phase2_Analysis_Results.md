# Phase 2: Department Admission Threshold Analysis

## Summary of Results

Based on the survey data from 395 students (362 valid 2023 IDs, 359 matched with academic records, 358 eligible with >=60 credit hours), here are the estimated admission thresholds for each department:

## Current Student Preferences (First Choice)
- **IS (Information Systems)**: 141 students (39.4%) - Most popular
- **AI (Artificial Intelligence)**: 87 students (24.3%) - High demand
- **CS (Computer Science)**: 79 students (22.1%) - Moderate demand  
- **IT (Information Technology)**: 33 students (9.2%) - Low demand
- **DS (Data Science)**: 18 students (5.0%) - Lowest demand

## Recommended Department Capacities
Based on the allocation strategy (IT +30%, DS +20%, CS/AI/IS ±10):

| Department | Capacity | Strategy |
|------------|----------|----------|
| IT | 92 students | +30% (base × 1.3) |
| DS | 85 students | +20% (base × 1.2) |
| CS | 81 students | +10 students |
| AI | 61 students | -10 students |
| IS | 76 students | +5 students |

**Base capacity**: 71 students per department

## Expected Admission Thresholds

### Current Moderate Scenario
| Department | GPA Threshold | Competition Ratio | Status |
|------------|---------------|-------------------|---------|
| **IS** | ≥ 2.90 | 1.86:1 | High competition |
| **AI** | ≥ 2.62 | 1.43:1 | Moderate competition |
| **CS** | ≥ 1.41 | 0.98:1 | Balanced |
| **IT** | ≥ 1.58 | 0.36:1 | Under-subscribed |
| **DS** | ≥ 1.75 | 0.21:1 | Under-subscribed |

## Scenario Analysis

### Conservative Scenario (Lower capacity increases)
- **AI**: GPA ≥ 2.54 (capacity: 66)
- **CS**: GPA ≥ 1.83 (capacity: 76)  
- **IT**: GPA ≥ 1.58 (capacity: 85)
- **DS**: GPA ≥ 1.75 (capacity: 78)
- **IS**: GPA ≥ 2.90 (capacity: 76)

### Aggressive Scenario (Higher capacity increases)
- **AI**: GPA ≥ 2.69 (capacity: 56)
- **CS**: GPA ≥ 1.41 (capacity: 86)
- **IT**: GPA ≥ 1.58 (capacity: 99)
- **DS**: GPA ≥ 1.75 (capacity: 92)
- **IS**: GPA ≥ 2.92 (capacity: 71)

## Key Insights

1. **High Demand Departments**: IS and AI show significant over-subscription
2. **Under-subscribed Departments**: IT and DS have very low competition ratios
3. **Balanced Department**: CS shows near-perfect balance between supply and demand
4. **GPA Range**: Thresholds range from 1.41 (CS) to 2.90+ (IS)

## Recommendations

### For University Administration:
1. **Consider increasing IS capacity** - highest demand with 1.86:1 competition
2. **Promote IT and DS programs** - currently under-subscribed despite capacity increases
3. **AI capacity seems appropriate** - good balance of selectivity vs. access
4. **CS shows ideal balance** - maintain current strategy

### For Students:
1. **IS applicants**: Need GPA ≥ 2.90 for reasonable admission chances
2. **AI applicants**: Need GPA ≥ 2.62 for admission
3. **CS applicants**: GPA ≥ 1.41 should be sufficient
4. **IT/DS applicants**: Lower thresholds, good opportunities for students with moderate GPAs

## Data Quality Notes

- **Survey Coverage**: 359/1088 (33%) of 2023 students responded
- **Eligibility Filter**: ≥60 credit hours (estimated as 3 credits per course)
- **GPA Distribution**: Students range from 1.41 to 4.0 GPA
- **Credit Hours**: Range from 9 to 114 hours (mean: 74.3 hours)

## Methodology

1. **Student Selection**: 2023 entry year students with ≥60 credit hours
2. **Credit Calculation**: Course count × 3 (standard credit assumption)
3. **GPA**: Maximum GPA across all courses for each student
4. **Preference Matching**: First choice department preference
5. **Capacity Allocation**: Based on strategic departmental priorities
6. **Threshold Calculation**: Minimum GPA of admitted students in each department

---

*Analysis completed: August 2025*  
*Based on survey data from 358 eligible students*
