# Example 1: Read entire file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)


# Example 2: Read line by line
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())


# Example 3: Read first 10 characters
with open("example.txt", "r") as file:
    content = file.read(10)
    print(content)