# Example 1: Write text to file
with open("output.txt", "w") as file:
    file.write("Hello, World!")


# Example 2: Write multiple lines
lines = ["Python\n", "File\n", "Writing\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)


# Example 3: Append text
with open("output.txt", "a") as file:
    file.write("\nNew line added")