"""
    Filename: caesar_crypto.py
     Version: 0.1
      Author: Richard E. Rawson
        Date: 2023-04-30
 Description: A Caesar cipher involves shifting each character in a plaintext by three letters forward. Non-ASCII characters will be ignored.

a -> d, b -> e, c -> f, etc...at the end of the alphabet, the cipher mapping wraps around the end, so:

x -> a, y -> b, z -> c.for example, encrypting 'python' using a caesar cipher gives:

python
||||||
sbwkrq

We use two methods of finding the cipher text:
    1. deque allows us to actually rotate the alphabet. Then, using the index of the given letter in the alphabet, use the letter at the same index in the rotated alphabet.

    2. Modular arithmetic: Find the index of the letter and add r (the amount of rotation). This addition may result in an index greater than 26 (the number of letters in the alphabet). So, use ndx % 26 to find the "wrapped" index. Using r > 25 makes no sense since r = 26 is the same as not wrapping and r = 27 and r = 79 are both the same as r = 1.
"""

from collections import deque
from string import ascii_lowercase

from icecream import ic

ALPHABET = deque(ascii_lowercase + " ")


def caesar_deque(text: str, r: int) -> str:
    """
    Get a list of indexes for all the characters in "text".
    Rotate the alphabet and then use those indexes to get the corresponding letter in the rotated alphabet.
    """
    rotated: deque[str] = ALPHABET.copy()
    rotated.rotate(r)

    char_list: list[str] = []
    for c in text:
        c_lower: str = c.lower()
        if c_lower not in ALPHABET:
            char_list.append(c_lower)
            continue

        # Find the index of the letter in ALPHABET.
        ndx: int = ALPHABET.index(c_lower)

        # Re-capitalize the letter, if the original was a capital.
        if ord(c) < 97:
            char_list.append(rotated[ndx].upper())
        else:
            char_list.append(rotated[ndx])

    return "".join(char_list)


def caesar_mod(plaintext, r) -> str:

    char_list: list[str] = []
    for c in plaintext:
        c_lower: str = c.lower()

        if c_lower not in ALPHABET:
            char_list.append(c_lower)
            continue

        ndx: int = (ALPHABET.index(c_lower) - r) % 27

        # Re-capitalize the letter, if the original was a capital.
        if ord(c) < 97:
            char_list.append(ALPHABET[ndx].upper())
        else:
            char_list.append(ALPHABET[ndx])

    return "".join(char_list)


def main_deque(plaintext) -> None:

    r = -3  # negative rotates to the right a --> d

    ciphertext: str = caesar_deque(plaintext, r)
    print(plaintext)
    print(ciphertext)

    decrypttext: str = caesar_deque(ciphertext, -r)
    print(decrypttext)


def main_mod(plaintext) -> None:

    r = -3  # negative rotates to the right a --> d

    ciphertext: str = caesar_mod(plaintext, r)
    print(plaintext)
    print(ciphertext)

    decrypttext: str = caesar_mod(ciphertext, -r)
    print(decrypttext)


if __name__ == '__main__':

    plaintext = "In the café, the bánh mì sandwich is a popular choice among the regulars. The flaky baguette, stuffed with savory grilled pork, pickled daikon and carrots, fresh cilantro, and a dollop of sriracha mayo, is the perfect lunchtime indulgence. As I sipped my matcha latte, I noticed the barista's shirt had a cute ねこ (neko, or cat) graphic on it. It reminded me of the time I visited Tokyo and saw the famous 東京タワー (Tokyo Tower) at night, aglow with colorful lights. The world is full of unique and beautiful symbols, and Unicode makes it possible to express them all in one cohesive language."

    plaintext = "Hello world"

    print("\nUSING DEQUE TO DO THE ROTATION.")
    main_deque(plaintext)

    print()

    print('USING MODULAR ARITHMETIC TO DO THE ROTATION.')
    main_mod(plaintext)
