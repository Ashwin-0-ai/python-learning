""" 

Campaign_dashboard.py
Day 7 - OOH Campaign performance dashboard 

"""
import csv
import os

# Loading the campaign from the csv file

def load_campaigns(filepath):
    campaigns = []

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            campaigns.append({
                'campaign_name': row ['campaign_name'],
                'city' :         row['city'],
                'format':        row['format'],
                'spend':          float(row['spend']),
                'impressions':    int(row['impressions']),
                'clicks':         int(row['clicks']),
                'conversions':    int(row['conversions']),
                'revenue':        float(row['revenue'])
            }
            )
            return campaigns 
        
# Calculating metrics for campaigns 

def calculate_metrics(campaign):
    spend       = campaign['spend']
    impressions = campaign['impressions']
    clicks      = campaign['clicks']
    revenue     = campaign['revenue']

    campaign['roi'] = ((revenue - spend)/spend)*100 
    campaign['cpm'] = (spend / impressions) * 1000
    campaign['ctr'] = (clicks / impressions) * 100

    return campaign

# print the table for the campaign performance on the dashboard 

def print_report(campaigns):
    width = 100 


    print()
    print("OOH Campaign Performance Dashboard".center(width))
    print("-" * width)
    print(f"{'Day7 Portfolio Piece':^{width}}")
    print("-" * width)
    print()

#Print the values to be inserted in the table

    print(f"{'CAMPAIGN':<38} {'CITY':<12} {'FORMAT':<14} {'SPEND':>8} {'ROI':>8} {'CPM':>7} {'CTR':>7}")
    print("-" * width)

    for c in campaigns:
        roi_flag = "*" if c['roi'] >= 200 else " "

        print (
            f"{c['campaign_name']:<38} {c['city']:<12} {c['format']:<14} ${c['spend']:>7.2f} {c['roi']:>7.2f}% ${c['cpm']:>5.2f} {c['ctr']:>6.3f}%"

        )
def main():
    campaigns = load_campaigns("campaign_data.csv")
    campaigns = [calculate_metrics(c) for c in campaigns]
    print_report(campaigns)

if __name__ == "__main__":
    main()