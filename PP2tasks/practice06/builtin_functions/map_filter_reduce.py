from functools import reduce

# Example 1: map
numbers = [1, 2, 3, 4]
squared = list(map(lambda x: x**2, numbers))
print(squared)


# Example 2: filter
numbers = [1, 2, 3, 4, 5, 6]
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)


# Example 3: reduce
numbers = [1, 2, 3, 4]
sum_all = reduce(lambda a, b: a + b, numbers)
print(sum_all)