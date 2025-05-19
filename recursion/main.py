from __future__ import annotations

"""
Recursion playground!
"""


def sum(number: int) -> int:
    """
    Makes the sum of all the numbers before <number>

    This function uses recursion to sum up all the numbers that come before of the given <number> arg.

    Args:
        number (int): given number to get sum of

    Returns:
        int: {4:Description of the returned object.}

    Example:
        # Example of how to use it
        sum(5) -> 5 + 4 + 3 + 2 + 1 + 0 -> 15
    """

    if number < 0:
        raise Exception("Negative numbers not allowed")
    if number == 0:
        return 0
    return number + sum(number - 1)


def max_in_list(ll: list):
    """
    Use recursion to grab the max element in a list

    Using recursion, this function will search throuth the given list
    and find the max element, just like using `max(list)`.

    Args:
        ll: list of SupportsRichComparison type

    Returns:
        The max element of the list
    """

    if len(ll) == 0:
        raise Exception("Empty List")
    if len(ll) == 1:
        return ll[0]

    return max(ll[0], max_in_list(ll[1:]))


def min_max[T](array: list[T]) -> tuple[T, T] | None:
    """
    Grab the `min` and `max` value of a given list.
     
    :param (list[T]) array: A list to compare `min` and `max`
    :return: A tuple with the `min` value and the `max` value 
    """
    if len(array) == 0:
        return None

    if len(array) == 1:
        return array[0], array[0]

    if len(array) == 2:
        return min(array), max(array)

    # divide the list
    mid: int = len(array) // 2
    first_half: array = array[:mid]
    last_half: array = array[mid:]

    min1, max1 = min_max(first_half)
    min2, max2 = min_max(last_half)

    return min(min1, min2), max(max1, max2)


def has_more_vowels(text: str) -> bool:
    """Check if the given string has more vowels han consonants.

    :param text: Text to check for
    :type text: str
    :return: True if it has more vowels.
    :rtype: bool
    """

    def verify(s: str, vowels: int = 0, consonants: int = 0) -> bool:
        if not s:
            return vowels > consonants

        vowel_test: bool = s[0].lower() in 'aeiou'
        consonant_test: bool = not vowel_test and s[0].isalpha()
        return verify(s[1:], vowels + int(vowel_test), consonants + int(consonant_test))

    return verify(text)


def palindrome(text: str) -> bool:
    """
    Tests if the given string is a palindrome
    :param text: String to check for
    :type text: str
    :return: True if is palindrome
    :rtype: bool
    """

    clean_text = ''.join(c.lower() for c in text if c.isalnum())

    def verify(chars: str, left: int, right: int) -> bool:
        if left >= right:
            return True
        if chars[left] != chars[right]:
            return False
        return verify(chars, left + 1, right - 1)

    return verify(clean_text, 0, len(clean_text) - 1)


def more_odd_than_even(array: list[int]) -> bool:
    """
    Test if a list of ints have more odd numbers than even numbers
    :param array: list of ints
    :type array: list[int]
    :return: True if it has more odd numbers
    :rtype: bool
    """
    def verify(n: list[int], odd: int = 0, even: int = 0) -> bool:
        if not n:
            return odd > even
        test: bool = n[0] % 2 == 0
        return verify(n[1:], odd + int(not test), even + int(test))
    return verify(array)


if __name__ == "__main__":
    print(sum(5))
    print(sum(10))
    try:
        sum(-4)
    except Exception as e:
        print(e)
    ll = [5, 4, 3, 2, 1]
    print(max_in_list(ll))
    print(min_max([5,30,45]))
    print(has_more_vowels('arara'))
    print(palindrome('subi no onibus'))
    print(more_odd_than_even([1, 2, 3, 4, 5]))
