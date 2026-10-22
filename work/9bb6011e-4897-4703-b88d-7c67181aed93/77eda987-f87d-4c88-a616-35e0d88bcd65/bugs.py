"""两类常见坑：坏例子仅用于教学，请使用对应的修正版。"""


def append_bad(item, items=[]):
    # 坏例子：默认列表只在定义函数时创建一次，后续调用共用它。
    items.append(item)
    return items


def append_fixed(item, items=None):
    # 修正版：省略参数时，每次调用都创建新列表；显式传列表则修改它。
    if items is None:
        items = []
    items.append(item)
    return items


def same_content_bad(left, right):
    # 坏例子：is 判断是否同一对象，不能用来判断两个列表内容是否相等。
    return left is right


def same_content_fixed(left, right):
    # 修正版：== 比较内容；is 适合检查 None 等单例。
    return left == right


def main():
    first_bad = append_bad("A")
    second_bad = append_bad("B")
    print("坏默认参数，两次结果：", first_bad, second_bad)
    first_fixed = append_fixed("A")
    second_fixed = append_fixed("B")
    print("修正默认参数，两次结果：", first_fixed, second_fixed)
    left = [1, 2]
    right = [1, 2]  # 单独创建，保证不是同一个列表，避开字符串/整数驻留干扰。
    print("相同内容用 is：", same_content_bad(left, right))
    print("相同内容用 ==：", same_content_fixed(left, right))


if __name__ == "__main__":
    main()
