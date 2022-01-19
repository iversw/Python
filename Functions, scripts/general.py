#Task 1: Write a function to calculate the sum of the first 100 even-valued
#fibonacci numbers.
def fib_even():
    #Store values in dict to avoid computing same value multiple times
    nums = {}
    for i in range(100):
        if i <= 1:
            nums[i] = 1
        else:
            n1 = nums[i-1]
            n2 = nums[i-2]
            nums[i] = nums[i-1] + nums[i-2]
    return sum(num for num in nums.values() if num % 2 == 0)

#Task 2: Write a function which, when passed two sorted arrays of integers
#returns an array of any numbers which appear in both. No value should appear
#in the returned array more than once.
def find_same(a1, a2):
    #Create iterators
    a1, a2 = iter(a1), iter(a2)

    #When an iterator is empty it returns None
    val1, val2 = next(a1, None), next(a2, None)
    equals = []

    #Loops while both iterators have values
    while val1 and val2:
        if val1 <= val2:
            if val1 == val2:
                #Match found
                equals.append(val1)
            val1 = next(a1, None)
        else:
            val2 = next(a2, None)
    return equals

#Task 3: Write a function which, when passed a positive integer returns true if
#the decimal representation of that integer contains no odd digits and otherwise
#returns false.
def contains_even(n):
    #Convert to string to check each character
    return all(int(n_char) % 2 == 0 for n_char in str(n))

#Task 4: Write a function which, when passed a decimal digit X, returns the
#value of X + XX + XXX + XXXX. E.g when supplied the digit 3 it should return
#3702 (3 + 33 + 333 + 3333).
def plus_x(X):
    return sum(X * i for i in [1,11,111,1111])

if __name__ == '__main__':
    print("Task 1:")
    print(fib_even())

    print("\nTask 2:")
    print(find_same([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [5, 9]))

    print("\nTask 3:")
    print(contains_even(22122))
    print(contains_even(22222))

    print("\nTask 4:")
    print(plus_x(3))
