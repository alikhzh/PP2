import os

# Example 1: Create directory
os.mkdir("new_folder")


# Example 2: Create nested directories
os.makedirs("parent/child")


# Example 3: List files in directory
files = os.listdir(".")
print(files)