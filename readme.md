# Caesar Cipher Encryption/Decryption

This Python program implements the Caesar cipher, a simple substitution cipher where each letter in the plaintext is replaced by a letter a fixed number of positions down the alphabet.

## Description

The Caesar cipher is one of the earliest known and simplest ciphers. It is a type of substitution cipher where each letter in the plaintext is replaced by a letter a fixed number of positions down the alphabet. For example, with a shift of 3, A would be replaced by D, B by E, and so on.

This program provides two methods for implementing the Caesar cipher:

1. **Deque Method**: This method uses Python's `deque` (double-ended queue) data structure to rotate the alphabet by the specified shift value. The program then finds the index of each character in the original alphabet and uses the character at the same index in the rotated alphabet as the ciphertext.

2. **Modular Arithmetic Method**: This method calculates the new index of each character by adding the shift value to its index in the alphabet and taking the result modulo 27 (since there are 26 letters in the English alphabet plus a space character).

## Usage

```
caesar_crypto.py [OPTIONS] [MESSAGE]

Options

-f, --file: Specify a file containing the message to encrypt or decrypt.
-m, --method: Choose the encryption method (deque or modular). Default is deque.
-r, --rotate: Specify the rotation value (shift distance). Default is 3.
-e, --encrypt: Encrypt the provided message or file.
-d, --decrypt: Decrypt the contents of the encrypted.txt file.
```

## Examples

**Encrypt a message, rotating the alphabet by 5 characters:**

`caesar_crypto.py -r 5 "Hello, World!"`

**Encrypt a file, using a default rotation of 3 characters:**

`caesar_crypto.py -f message.txt -e`

**Decrypt the contents of encrypted.txt, created with --rotate = 5:**

`caesar_crypto.py -r 5 -d`


## Notes

- The encrypted text is saved in the `encrypted.txt` file, and the decrypted text is saved in the `decrypted.txt` file.
- Encryption and decryption must use the same value for `--rotate`.
- If there is a `message`, but no `--encrypt` or `--decrypt` option is provided, the program defaults to encryption.
- If there are no options provided, `encrypted.txt` is decrypted.
- Non-ASCII characters (*e.g.*, punctuation, accented letters) are left unchanged.

## Dependencies
- click (for command-line interface)
- icecream (for debugging, optional)