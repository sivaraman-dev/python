print("Mobile Recharge Recommendation for Jio")

data = float(input("Enter your monthly data usage (in GB): "))
budget = int(input("Enter your budget (₹): "))

if data >= 50 and budget >= 350:
    print("Recommended Plan: ₹349 Plan")
elif data >= 40 and budget >= 300:
    print("Recommended Plan: ₹299 Plan")
elif data >= 30 and budget >= 200:
    print("Recommended Plan: ₹239 Plan")
else:
    print("Recommended Plan: Basic ₹199 Plan")