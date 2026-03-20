roi = float(input("Enter the campaign's ROI %:"))
if roi >= 50:
    print("Excellent Campaign- Scale this campaign")
elif roi>=20:
    print("Good performance - maintain current spend")
elif roi >=0:
    print("weak performance - Review targeting")
else :
    print("Negative ROI - Stop the campaign immediately")