# import our 2 functions
from practice_ctr_grader.py import calculate_ctr
from practice_grade_ctr.py import grade_ctr

# List of campaign data

ads =[
    {"name": "Billboard A", "clicks": 320,  "impressions": 12000},
    {"name": "Digital B",   "clicks": 850,  "impressions": 15000},
    {"name": "Social C",    "clicks": 90,   "impressions": 8000},
]

#loop through each of the ads and calculate the CTR and print report
print ("\nCampaign Performance Report\n ")
print (f"{'name':<15} {'CTR (%)':<10} {'Grade':<10} {'Performance':<15}")

for ad in ads:
    ctr = calculate_ctr(ad["clicks"], ad["impressions"])
    grade = grade_ctr(ctr)
    print (f"{ad['name']:<15} {ctr:.2f}%   {grade:<10} {'Excellent' if grade == 'Excellent' else 'Needs Improvement':<15}")