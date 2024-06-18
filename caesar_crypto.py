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

With both methods, any characters except spaces not included in ascii_lowercase (such as puncuation or unicode like é) are retained as-is.
"""

from collections import deque
from pathlib import Path
from string import ascii_lowercase

import click
from icecream import ic

ALPHABET = deque(ascii_lowercase + " ")
METHODS: list[str] = ["deque", "modular"]


@click.command(help="Provide either a file or a [MESSAGE] to encrypt. Decrypt the encrypted message in \"encrypted.txt\".", epilog="Any text file can be encrypted. Encrypted text is saved in \"encrypted.txt\" and decrypted text is saved in \"decrypted.txt\". Encryption and decryption use the same value for \"rotate\". To decrypt a message previously encrypted, only change --encrypt to --decrypt.\n\nEXAMPLE USAGE\n\ncaesar_crypto.py \"The boats launch at midnight.\" --> encrypts the message\n\ncaesar_crypto.py -d --> decrypts contents of \"encrypted.txt\"")
@click.argument("message", type=str, required=False)
@click.option("-f", "--file", type=click.Path(exists=False), help='File to encrypt.')
@click.option('-m', '--method', type=click.Choice(METHODS), default="deque", help="Choose an encryption method.")
@click.option('-r', '--rotate', type=int, default="3", help="Distance to rotate.")
@click.option('-e', '--encrypt', is_flag=True, default=False, help="Encrypt [MESSAGE]")
@click.option('-d', '--decrypt', is_flag=True, default=False, help="Decrypt an encrypted [MESSAGE]")
def cli(message: str, file: str, method: str, rotate: int, encrypt: bool, decrypt: bool) -> None:
    """
    Main organizing function for the CLI.

    Parameters
    ----------
    message : str -- message on command line to encrypt
    file : str -- file containing a message to encrypt
    method : str -- True to use deque method; False to use modular method
    rotate : int -- "distance" to rotate alphabet
    encrypt : bool -- True if user wants to encrypt a message
    decrypt : bool -- True if user wants to decrypt "encrypted.txt"
    """

    print()
    ic(message)
    ic(file)
    ic(method)
    ic(type(rotate), rotate)
    ic(encrypt)
    ic(decrypt)
    print()

    if file:
        message: str = get_text(file)

    if not message and encrypt:
        print("There is no text to encrypt.")
        exit()

    if encrypt and decrypt:
        print("Cannot encrypt and decrypt in one operation.")
        exit()

    # If neither --encrypt nor --decrypt was set, then encrypt by default.
    if not decrypt and not encrypt:
        encrypt = True

    if encrypt and method == 'deque':
        encrypted_text: str = caesar_deque(message, rotate)
        with open('encrypted.txt', 'w', encoding='utf-8') as f:
            f.write(encrypted_text)

    elif encrypt and method == 'modular':
        encrypted_text: str = caesar_mod(message, rotate)
        with open('encrypted.txt', 'w', encoding='utf-8') as f:
            f.write(encrypted_text)

    elif decrypt and method == "deque":
        rotate *= -1
        message: str = get_encrypted_text()
        decrypted_text: str = caesar_deque(message, rotate)
        with open('decrypted.txt', 'w', encoding='utf-8') as f:
            f.write(decrypted_text)

    elif decrypt and method == "modular":
        rotate *= -1
        message: str = get_encrypted_text()
        decrypted_text: str = caesar_mod(message, rotate)
        with open('decrypted.txt', 'w', encoding='utf-8') as f:
            f.write(decrypted_text)

    else:
        pass


def get_encrypted_text() -> str:
    """
    Read contents of "encrypted.txt". All encrypted text is saved in that file, so decryption always retrieves that ciphertext.

    Returns
    -------
    str -- the encrypted contents of "encrypted.txt"
    """
    with open('encrypted.txt', 'r', encoding="utf-8") as f:
        all_lines: list[str] = f.readlines()
    message: list[str] = [line.strip('\n') for line in all_lines]
    return "".join(message)


def get_text(file: str) -> str:
    """
    Given a file name, read the text into a single string.

    Parameters
    ----------
    file : str -- file containing text to be encrypted

    Returns
    -------
    str -- text in file
    """

    filename: Path = Path(file)
    if filename.exists():
        with open(filename, 'r', encoding='utf-8') as f:
            text: list[str] = f.readlines()

        text = [x.strip('\n') for x in text]

        return "".join(text)

    else:
        print(f'Could not find {file}.')
        exit()


def caesar_deque(text: str, r: int) -> str:
    """
    Get a list of indexes for all the characters in "text".
    Rotate the alphabet and then use those indexes to get the corresponding letter in the rotated alphabet.

    Parameters
    ----------
    text : str -- text to encrypt or decrypt
    r : int -- distance to rotate alphabet

    Returns
    -------
    str -- encrypted or decrypted text
    """
    rotated: deque[str] = ALPHABET.copy()
    rotated.rotate(r)

    char_list: list[str] = []
    ic(text)
    for c in text:
        c_lower: str = c.lower()
        if c_lower not in ALPHABET:
            char_list.append(c_lower)
            continue

        # Find the index of the letter in ALPHABET.
        ndx: int = ALPHABET.index(c_lower)

        # Re-capitalize the letter, if the original was a capital.
        if ord(c) < 97 and ord(c) > 32:
            char_list.append(rotated[ndx].upper())
        else:
            char_list.append(rotated[ndx])

    return "".join(char_list)


def caesar_mod(text: str, r: int) -> str:
    """
    Use modular arithmetic to get the rotated character.

    Parameters
    ----------
    text : str -- text to encrypt or decrypt
    r : int -- distance to rotate alphabet

    Returns
    -------
    str -- encrypted or decrypted text
    """

    char_list: list[str] = []
    for c in text:
        c_lower: str = c.lower()

        if c_lower not in ALPHABET:
            char_list.append(c_lower)
            continue

        ndx: int = (ALPHABET.index(c_lower) - r) % 27

        # Re-capitalize the letter, if the original was a capital.
        if ord(c) < 97 and ord(c) > 32:
            char_list.append(ALPHABET[ndx].upper())
        else:
            char_list.append(ALPHABET[ndx])

    return "".join(char_list)


if __name__ == '__main__':

    plaintext = "In the café, the bánh mì sandwich is a popular choice among the regulars. The flaky baguette, stuffed with savory grilled pork, pickled daikon and carrots, fresh cilantro, and a dollop of sriracha mayo, is the perfect lunchtime indulgence. As I sipped my matcha latte, I noticed the barista's shirt had a cute ねこ (neko, or cat) graphic on it. It reminded me of the time I visited Tokyo and saw the famous 東京タワー (Tokyo Tower) at night, aglow with colorful lights. The world is full of unique and beautiful symbols, and Unicode makes it possible to express them all in one cohesive language."

    plaintext = "Hello world"

    # print("\nUSING DEQUE TO DO THE ROTATION.")
    # main_deque(plaintext)

    # print()

    # print('USING MODULAR ARITHMETIC TO DO THE ROTATION.')
    # main_mod(plaintext)

    pass
    cli()
