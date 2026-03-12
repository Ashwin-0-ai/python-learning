def classify_performance(roi):
    if roi >= 50:
        return "Strong"
    elif  roi >= 20:
        return "Moderate"
    elif roi >= 0:
        return "Weak"
    else:
        return "Negative - Pause Campaign"
    
#Testing the function

print(classify_performance(75))
print(classify_performance(35))
print(classify_performance(10))
print(classify_performance(-5))