# Пользователь вводит в консоль строку.
# Если выведенная строка является палиндромом - выведите True. Если не является - выведите False.
# Палиндром — это слово или фраза, которые одинаково читаются слева направо и справа налево.

s = input()
print(s == s[::-1])
