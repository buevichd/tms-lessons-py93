def is_palindrome(s):
    return s == s[::-1]


print(is_palindrome('aaa'))  # True
print(is_palindrome('aba'))  # True
print(is_palindrome('abca'))  # False
print(is_palindrome('abba'))  # True
print(is_palindrome(''))  # True
print(is_palindrome('abcCBA'))  # False

input_s = input()
print(is_palindrome(input_s))
