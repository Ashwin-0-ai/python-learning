from day4_ROI_Calculator import calculate_roi 
from day4_currency_formatter import format_currency
from day4_performance_classifier import classify_performance

#campaign data 
campaigns = [
    {"channel": "OOH",     "spend": 5000,  "revenue": 18000},
    {"channel": "Digital", "spend": 3000,  "revenue": 9500},
    {"channel": "Social",  "spend": 1500,  "revenue": 4200},
    {"channel": "Email",   "spend": 500,   "revenue": 3100},
    ]

#run the analysis
print ("\n ___Campaign Performance Report___")
print (f"{'Channel' :<12} {'Spend' :<15} {'ROI' :<12} {'Performance'}")
print ("_" * 50)

for campaign in campaigns:
    roi    = calculate_roi(campaign["spend"], campaign["revenue"])
    spend_fmt = format_currency(campaign["spend"])
    performance = classify_performance (roi)

    print(f"{campaign['channel']:<12} {spend_fmt:<15} {roi:<10.1f}% {performance}")
    