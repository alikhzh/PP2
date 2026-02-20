#1
def squares(n):
    for i in range(1, n + 1):
        yield i * i

for num in squares(5):
    print(num)

#2
def evens(n):
    for i in range(0, n + 1, 2):
        yield i

print(list(evens(10)))
#3
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for i in countdown(5):
    print(i)
