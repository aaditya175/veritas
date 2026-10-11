"""
Generates rich preloaded sample dataset matching the project concept paper:
employee_data.csv (Education, Age, Experience, Occupation, HoursPerWeek, Department, Income, PerformanceScore)
with known causal structure:
Age -> Experience -> Income
Education -> Occupation -> Income
HoursPerWeek -> Income
Occupation -> Department
"""
import os
import numpy as np
import pandas as pd

np.random.seed(42)
n = 300

# 1. Root: Age ~ N(32, 6) clipped between 22 and 60
age = np.random.normal(32, 7, n).clip(22, 60).astype(int)

# 2. Education: depends somewhat on Age
edu_choices = ["Bachelor's", "Master's", "PhD"]
edu = []
for a in age:
    if a < 25:
        p = [0.85, 0.15, 0.0]
    elif a < 30:
        p = [0.55, 0.40, 0.05]
    else:
        p = [0.40, 0.45, 0.15]
    edu.append(np.random.choice(edu_choices, p=p))
edu = np.array(edu)

# 3. Experience: caused by Age and Education
min_edu_age = {"Bachelor's": 22, "Master's": 24, "PhD": 27}
exp = []
for a, e in zip(age, edu):
    max_possible = max(0, a - min_edu_age[e])
    actual = np.random.uniform(0.6, 1.0) * max_possible
    exp.append(round(actual, 1))
exp = np.array(exp)

# 4. Occupation: caused by Education
occupations = []
for e in edu:
    if e == "PhD":
        p = [0.15, 0.10, 0.10, 0.65] # Dev, Manager, Analyst, Researcher
    elif e == "Master's":
        p = [0.35, 0.35, 0.20, 0.10]
    else:
        p = [0.55, 0.15, 0.25, 0.05]
    occupations.append(np.random.choice(["Developer", "Manager", "Analyst", "Researcher"], p=p))
occupations = np.array(occupations)

# 5. HoursPerWeek: ~ N(42, 5)
hours = np.random.normal(42, 5, n).clip(30, 65).round().astype(int)

# 6. Department: related to occupation
dept_map = {
    "Developer": ["Engineering", "Product"],
    "Manager": ["Operations", "Management"],
    "Analyst": ["Analytics", "Finance"],
    "Researcher": ["R&D", "AI Lab"]
}
depts = [np.random.choice(dept_map[occ]) for occ in occupations]

# 7. Income: Caused by Education, Experience, Occupation, and HoursPerWeek
base_occ_sal = {"Developer": 65000, "Manager": 85000, "Analyst": 55000, "Researcher": 90000}
edu_bonus = {"Bachelor's": 0, "Master's": 12000, "PhD": 25000}
income = []
for e, ex, occ, h in zip(edu, exp, occupations, hours):
    base = base_occ_sal[occ] + edu_bonus[e]
    exp_factor = ex * 4200
    hours_factor = (h - 40) * 800
    noise = np.random.normal(0, 4000)
    total = max(35000, base + exp_factor + hours_factor + noise)
    income.append(int(round(total, -2)))
income = np.array(income)

# 8. PerformanceScore: 1.0 to 5.0
perf = np.random.normal(4.1, 0.5, n).clip(2.5, 5.0).round(1)

df = pd.DataFrame({
    "Age": age,
    "Education": edu,
    "Experience": exp,
    "Occupation": occupations,
    "HoursPerWeek": hours,
    "Department": depts,
    "Income": income,
    "PerformanceScore": perf
})

out_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(out_dir, "employee_data.csv")
df.to_csv(csv_path, index=False)
print(f"Generated {len(df)} rows sample dataset at {csv_path}")
