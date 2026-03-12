def format_currency(amount):
    return f"Euro{amount:,.2f}"

#testing the function
print(format_currency(5000))
print(format_currency(1234567.89))
print(format_currency(800))