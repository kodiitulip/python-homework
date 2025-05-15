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


if __name__ == "__main__":
    print(sum(5))
    print(sum(10))
    try:
        sum(-4)
    except Exception as e:
        print(e)
    ll = [5, 4, 3, 2, 1]
    print(max_in_list(ll))
