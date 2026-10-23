def compute_bmi(weight, height):
    if height <= 0:
        raise ValueError("Height must be greater than 0.")
    return weight / (height ** 2)


def classify_bmi(bmi):
    if bmi >= 30:
        return "Obese"
    elif bmi >= 25:
        return "Overweight"
    elif bmi >= 18.5:
        return "Normal"
    else:
        return "Underweight"


def main():
    weight = float(input("Enter your weight in kilograms: "))
    height = float(input("Enter your height in meters: "))
    bmi = compute_bmi(weight, height)
    print(f"Your BMI is: {bmi:.2f}")
    category = classify_bmi(bmi)
    print(f"Your category is: {category}")


if __name__ == "__main__":
    main()



