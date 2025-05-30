lst = [6, 2, 3, 24, 100, 45, 5, 60, 7, 74, 34]

for i in range(len(lst)):
    for j in range(0, len(lst) - i - 1):
        if lst[j] > lst[j + 1]:
            lst[j], lst[j + 1] = lst[j + 1], lst[j]

print(lst)
