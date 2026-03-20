def calculate_roi(spend, revenue):
    roi = (revenue - spend) / spend * 100
    return roi

# Testing the function
if __name__ == "__main__":
 result: float = calculate_roi(200, 40)
 print(f"roi: {result:,.2f}%")
