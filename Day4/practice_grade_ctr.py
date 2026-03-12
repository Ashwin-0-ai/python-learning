# conditional loops to check grade_ctr

def grade_ctr(calculate_ctr):
    if calculate_ctr >= 5 and calculate_ctr < 10:
        return "Excellent"
    elif calculate_ctr <= 2 and calculate_ctr < 5:
        return "Good"
    else:
        return "poor"    
    
    #test the function
print (grade_ctr(1)) 
print (grade_ctr(0))
print (grade_ctr(89))
    
