from collections import Counter


def has_duplicates(string_array):
    # 是否有相同的元素
    return len(string_array) != len(set(string_array))


def remove_element(string_array, element):
    return [item for item in string_array if item != element]

def count_elements(string_array):
    return Counter(string_array)


if __name__ == '__main__':
    # 示例
    strings = ["apple", "banana", "orange", "apple"]
    result = count_elements(strings)
    print(result)  # 输
    for element in result:
        print(element, result[element])
