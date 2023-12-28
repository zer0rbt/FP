students = [
    {"name": "Alice", "age": 20, "grades": [85, 90, 88, 92]},
    {"name": "Bob", "age": 22, "grades": [78, 89, 76, 85]},
    {"name": "Charlie", "age": 21, "grades": [92, 95, 88, 94]},
    {"name": "David", "age": 23, "grades": [86, 88, 84, 90]},
    {"name": "Eva", "age": 20, "grades": [89, 91, 87, 93]},
    {"name": "Frank", "age": 22, "grades": [79, 82, 81, 88]},
    {"name": "Grace", "age": 21, "grades": [93, 96, 89, 95]},
    {"name": "Hannah", "age": 20, "grades": [87, 90, 85, 91]},
    {"name": "Isaac", "age": 22, "grades": [94, 89, 86, 92]},
    {"name": "Jack", "age": 21, "grades": [89, 87, 88, 90]},
    {"name": "Karen", "age": 23, "grades": [85, 89, 82, 91]},
    {"name": "Liam", "age": 20, "grades": [88, 91, 87, 92]},
    {"name": "Mia", "age": 22, "grades": [83, 85, 80, 89]},
    {"name": "Noah", "age": 21, "grades": [91, 93, 90, 94]},
    {"name": "Olivia", "age": 23, "grades": [87, 89, 84, 91]},
    {"name": "Patrick", "age": 20, "grades": [85, 88, 86, 90]},
    {"name": "Quinn", "age": 22, "grades": [86, 87, 84, 89]},
    {"name": "Rachel", "age": 21, "grades": [90, 91, 88, 92]},
    {"name": "Sam", "age": 23, "grades": [92, 94, 91, 95]},
    {"name": "Tom", "age": 20, "grades": [88, 90, 87, 91]}
]

age = 21
grades = "92 95".split(" ")
print(list(filter(lambda x: (x["age"] == age and all(
    list(map(lambda y: int(y) in x["grades"], grades)))), students)))

print(list(map(lambda x: sum(x["grades"]) / len(x["grades"]), students)),
      sum(list(map(lambda x: sum(x["grades"]) / len(x["grades"]), students))) / len(
          list(map(lambda x: sum(x["grades"]) / len(x["grades"]), students))))

print(list(filter(lambda z: sum(z["grades"]) / len(
    z["grades"]) > 90, students)))
