'''
    any method declared here will be available for remote calling
'''
import time


def reverse_string(string: str) -> str:
    time.sleep(3)
    return string[::-1]


def shake_string(string: str) -> str:
    time.sleep(7)

    if not string:
        return ""

    result = ""
    for even, odd in zip(string[0::2], string[1::2]):
        result += odd + even
    # manually add the last character if it is odd
    if len(string) % 2 == 1:
        result += string[-1]

    return result


if __name__ == "__main__":
    print(shake_string("1123"))
    print(reverse_string("1123"))
