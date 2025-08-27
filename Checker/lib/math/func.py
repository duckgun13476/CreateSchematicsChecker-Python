from collections import Counter
import random
import string

def has_duplicates(string_array):
    # 是否有相同的元素
    return len(string_array) != len(set(string_array))


def remove_element(string_array, element):
    return [item for item in string_array if item != element]

def count_elements(string_array):
    return Counter(string_array)


def generate_random_string(length):
    # 定义字符集，包括字母和数字
    characters = string.ascii_letters + string.digits
    # 随机选择字符并生成字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

