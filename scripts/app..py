import bmi

#result = bmi.compute_bmi(70, 1.75)
#print(f"Computed BMI: {result:.2f}")

people = [
	{"name": "Mira Solen", "height": 1.62, "weight": 58},
	{"name": "Theo Vance", "height": 1.78, "weight": 74},
	{"name": "Lena Marlow", "height": 1.69, "weight": 63},
	{"name": "Oren Vale", "height": 1.84, "weight": 81},
	{"name": "Nia Calder", "height": 1.57, "weight": 52},
	{"name": "Jasper Wren", "height": 1.73, "weight": 69},
	{"name": "Talia Fen", "height": 1.66, "weight": 61},
	{"name": "Remy Alder", "height": 1.80, "weight": 77},
]
for person in people:
    weight = person["weight"]
    height = person["height"]   
    bmivalue = bmi.compute_bmi(weight, height)
    category = bmi.classify_bmi(bmivalue)
    print(f"{person['name']} has a BMI of {bmivalue:.2f} and is classified as {category}.")
    
