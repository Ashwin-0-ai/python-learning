# Defining the inputs 
num1 = float (input ("Enter your first number"))
num2 = float (input ("Enter your second number"))
num3 = float (input ("Enteryour third number" ))

# Formula for total and average
total = num1 + num2 + num3
average = total / 3

# print functions 
print (f" The total of the numbers are {total}")
print (f" The average of the numbers are {average}")
print (f" The difference between the highest and the lowest inputs are {max(num1,num2,num3) - min(num1,num2,num3  )}")
