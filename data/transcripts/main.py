import json

grade_mapping = {
    "A+": 4,
    "A": 4,
    "B": 3,
    "C": 2
}


total_sum = 0

with open("./bachelor.json", "r") as f:
    data = json.load(f)

for course in data["courses"]:
    total_sum += grade_mapping[course["mark"]]

print(total_sum / len(data["courses"]))
