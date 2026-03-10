name = input("Enter your name: ")
birth_year = int(input("Enter your birth year: "))

current_year = 2026

age = current_year - birth_year

print("Hello", name)
print("Your age is:", age)
print("You have lived approximately", age * 365, "days")