#defining a function called calculator_ctr

def calculate_ctr(clicks,impressions):
    ctr = (clicks / impressions) *100
    return ctr 

#test calculator_ctr
result = calculate_ctr(500, 1000)
print(f"the ctr is {result:.2f}%")
