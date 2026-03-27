def addition(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    if b == 0:
        return "Cannot divide by zero"
    return a/b

add = addition(10,20)
sub = subtract(100,50)
mul = multiply(10,4)
div = divide(25,5)

print(f"Addition :{add}\nSubtraction :{sub}\nMultiplication :{mul}\nDivision :{div}")