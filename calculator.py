import streamlit as st

# Title
st.title("Simple Calculator")

# Input Numbers
num1 = st.number_input("Enter First Number", value=0.0)
num2 = st.number_input("Enter Second Number", value=0.0)

# Operation Selection
operation = st.selectbox(
    "Select Operation",
    ["Addition", "Subtraction", "Multiplication", "Division", "Modulus", "Power"]
)

# Backend Function
def calculate(a, b, op):
    if op == "Addition":
        return a + b
    elif op == "Subtraction":
        return a - b
    elif op == "Multiplication":
        return a * b
    elif op == "Division":
        if b != 0:
            return a / b
        return "Cannot divide by zero"
    elif op == "Modulus":
        if b != 0:
            return a % b
        return "Cannot divide by zero"
    elif op == "Power":
        return a ** b

# Calculate Button
if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.success(f"Result: {result}")
