# Example 1: enumerate
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(index, fruit)


# Example 2: zip
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

for name, score in zip(names, scores):
    print(name, score)


# Example 3: zip to dictionary
keys = ["name", "age", "city"]
values = ["John", 25, "London"]

person = dict(zip(keys, values))
print(person)