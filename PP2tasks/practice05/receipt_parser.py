import re


#1 Match a string that has 'a' followed by 0 or more 'b'
pattern1 = r"ab*"
print(bool(re.fullmatch(pattern1, "abbb")))


#2 Match a string that has 'a' followed by 2 to 3 'b'
pattern2 = r"ab{2,3}"
print(bool(re.fullmatch(pattern2, "abb")))


#3 Find sequences of lowercase letters joined with underscore
pattern3 = r"^[a-z]+_[a-z]+$"
print(bool(re.fullmatch(pattern3, "hello_world")))


#4 Find sequences of one uppercase letter followed by lowercase letters
pattern4 = r"[A-Z][a-z]+"
print(re.findall(pattern4, "Hello World TEST Python"))


#5 Match a string that has 'a' followed by anything, ending in 'b'
pattern5 = r"a.*b"
print(bool(re.fullmatch(pattern5, "axxxb")))


#6 Replace space, comma, or dot with colon
text6 = "Hello, world. Python is cool"
result6 = re.sub(r"[ ,.]", ":", text6)
print(result6)


#7 Convert snake_case to camelCase
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

print(snake_to_camel("hello_world_test"))


#8 Split a string at uppercase letters
text8 = "HelloWorldPython"
result8 = re.split(r"(?=[A-Z])", text8)
print(result8)


#9 Insert spaces between words starting with capital letters
text9 = "HelloWorldPython"
result9 = re.sub(r"(?<!^)(?=[A-Z])", " ", text9)
print(result9)


#10 Convert camelCase to snake_case
def camel_to_snake(text):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()

print(camel_to_snake("helloWorldTest"))