import shutil
import os

# Example 1: Copy file
shutil.copy("source.txt", "copy.txt")


# Example 2: Delete file
if os.path.exists("copy.txt"):
    os.remove("copy.txt")


# Example 3: Copy file to directory
shutil.copy("source.txt", "backup/source_copy.txt")