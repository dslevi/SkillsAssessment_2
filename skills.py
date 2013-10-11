# Write a function that takes an iterable (something you can loop through, ie: string, list, or tuple) and produces a dictionary with all distinct elements as the keys, and the number of each element as the value
def count_unique(some_iterable):
    distinct = {}
    for x in some_iterable:
        value = distinct.get(x, 0) + 1
        distinct[x] = value
    return distinct

# Given two lists, (without using the keyword 'in' or the method 'index') return a list of all common items shared between both lists
def common_items(l1, l2):
    common = []
    for i in range(len(l1)):
        for h in range(len(l2)):
            if l1[i] == l2[h]:
                common.append(l1[i])
    return common

print common_items(["hello", "world", "pizza", "face"], ["hey", "there", "world", "hello", "hello"])
# Given two lists, (without using the keyword 'in' or the method 'index') return a list of all common items shared between both lists. This time, use a dictionary as part of your solution.
def common_items2(list1, list2):
    common = []
    distinct = {}
    for x in list1:
        value = distinct.get(x, 0) + 1
        distinct[x] = value
    for x in list2:
        value = distinct.get(x, 0) + 1
        distinct[x] = value
    for i in distinct:
        if distinct[i] > 1:
            common.append(i)
    return common

print common_items2(["hello", "world", "pizza", "face"], ["hey", "there", "world", "hello", "hello"])

