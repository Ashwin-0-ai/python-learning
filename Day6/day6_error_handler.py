# Create the messy campiagn data 

campaign = [
      {"channel": "OOH" ,     "spend":"5000",     "revenue": "18000"},
      {"channel": "Digital",  "spend":"3000",     "revenue": "9500"},
      {"channel": "Social" ,  "spend":"",         "revenue": "4200"},
      {"channel": "Email" ,   "spend":"abc" ,     "revenue": "3100"},
      {"channel": "Print" ,   "spend":"2000",     "revenue": "5800"},
]

print (f"{'channel' :<12} {'spend' :<10} {'revenue':<10} {'status'}")
print ("--" *45)

for c in campaign :
    try :
        spend  = int (c["spend"])
        revenue = int (c["revenue"])
        roi = (revenue - spend) / spend * 100

        print(f" {c['channel'] :<12} {c['spend'] :<10} {c['revenue']:<10} ROI {roi:.1f}%")
    except ValueError:
        print (f" {c['channel'] :<12} {'---':<10} {'---':<10}  ! Skipped : Bad Data")
    except ZeroDivisionError:
        print (f" {c['channel'] :<12} {'---':<10} {'---':<10}  ! Skipped : Spend is zero ")
        