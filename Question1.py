"""
Group Name: Sydney 11
Course Code: HIT137

Group Members:
Mohamed Hatem Moneir Mansour Elshekh - 393891
Roshan Pandey - 395865
Kamana  - 392322
Sejal Pradhan - 396928


This program reads a plaintext file "raw_text.txt", encrypts its contents using a custom
encryption scheme based on user-provided shift values (shift1 and shift2), writes the
encrypted content to "encrypted_text.txt", then decrypts it back to "decrypted_text.txt"
and verifies that decryption matches the original.

Encryption Rules:
1. Lowercase letters (a-z):
   - First half (a-m): shift forward by shift1 * shift2
   - Second half (n-z): shift backward by shift1 + shift2
2. Uppercase letters (A-Z):
   - First half (A-M): shift backward by shift1
   - Second half (N-Z): shift forward by shift2^2
3. Other characters (spaces, tabs, numbers, punctuation) remain unchanged

Important Note:
Due to the nature of these rules, some characters may map to the same encrypted character.
To guarantee correct decryption, we store a metadata line that records the "half" of the
alphabet each character came from.

In the meta data, we store whether or not the character belongs to a-m or n-z or A-M or N-Z
if it belongs to a-m we store it as a
if it belongs to n-z we store it as b
if it belongs to A-M we store it as A
if it belongs to N-Z we store it as B
if it's a special character, we store it as 0

example encrypted file with meta data:
Baa0bbaaa0abbbb0abb0ababb0bbab0baa0aabb0aba0aabaaba0baa0baaab0baaabbb0
Sgd gkhbj ahemd een iklfi eldh jgd kzpo cef adddzjg jgd igzco mhkkemi.

References

ChatGPT-5. (2025). AI assistant for code layout and documentation grammar. OpenAI. https://openai.com/chatgpt
- Used for: wording/structure of comments and docstrings (no algorithmic code copied).

Computerphile. (2021, March 5). Caesar cipher explained [Video]. YouTube. https://www.youtube.com/watch?v=sMOZf4GN3oc
- Used for: classical cipher concepts understanding.

GeeksforGeeks. (2024). ASCII values in Python. https://www.geeksforgeeks.org/ascii-in-python/
- Used for: ord/chr conversions inside encrypt_char/decrypt_char.

ness-intricity101. (2010, May 18). What is metadata? [Video]. YouTube. https://www.youtube.com/watch?v=HXAstVP3-y0
- Used for: idea of storing per-character flags to ensure reversible mapping.

W3Schools. (2024). Python file handling. https://www.w3schools.com/python/python_file_handling.asp
- Used for: basic file I/O patterns.

W3Schools. (2024). Python file write. https://www.w3schools.com/python/python_file_write.asp
- Used for: writing text files (saving encrypted/decrypted output).

Python Software Foundation. (2024). The __main__ module. https://docs.python.org/3/library/__main__.html
- Used for: standard entry-point guard (if __name__ == "__main__").

Learn By Example. (2025). Python open() function. https://www.learnbyexample.org/python-open-function/
- Used for: open(..., encoding="utf-8") usage in file reading/writing.

DataCamp. (2024). Python new line. https://www.datacamp.com/tutorial/python-new-line
- Used for: newline handling when writing metadata header and ciphertext.

Python Software Foundation. (2025). Errors and Exceptions. https://docs.python.org/3/tutorial/errors.html
- Used for: checked error types and how to catch them in except blocks.
"""

def classify_char(c):
    """
    Determine which half of the alphabet a character belongs to.

    Returns a single-character flag:
    - 'a' : lowercase a-m
    - 'b' : lowercase n-z
    - 'A' : uppercase A-M
    - 'B' : uppercase N-Z
    - '0' : other characters (unchanged)
    """
    # Check if character is lowercase letter
    if 'a' <= c <= 'z':
        # Split lowercase alphabet into two halves: a-m and n-z
        if c <= 'm':
            return 'a'  # First half: a, b, c, ..., m
        else:
            return 'b'  # Second half: n, o, p, ..., z
    
    # Check if character is uppercase letter
    if 'A' <= c <= 'Z':
        # Split uppercase alphabet into two halves: A-M and N-Z
        if c <= 'M':
            return 'A'  # First half: A, B, C, ..., M
        else:
            return 'B'  # Second half: N, O, P, ..., Z
    
    # Character is not a letter (space, number, punctuation, etc.)
    return '0'

def encrypt_char(c, flag, shift1, shift2):
    """
    Encrypt a single character based on its classification flag and shift values.
    """
    if flag == 'a':  # lowercase a-m
        shift = shift1 * shift2 #shift by shift1*shift2 in case it's lowercase a-m
        new_pos = ord(c) - ord('a') + shift #get the raw order of the shift by removing the ord of 'a' (first letter)
        while new_pos >= 26: #continuously wrap around by subtracting 26 until position is within valid range (0-25)
            new_pos = new_pos - 26
        return chr(new_pos + ord('a')) #return the character of the new position (we add ord(a) because this is the starting point of the small alphabet)
    
    if flag == 'b':  # lowercase n-z
        shift = shift1 + shift2 #shift by shift1+shift2 in case it's lowercase n-z
        new_pos = ord(c) - ord('a') - shift #get the raw order of the shift by removing the ord of 'a' (first letter)
        while new_pos < 0: #continuously shift forward by adding 26 until position is within valid range (0-25)
            new_pos = new_pos + 26
        return chr(new_pos + ord('a')) #return the character of the new position (we add ord(a) because this is the starting point of the small alphabet)
    
    if flag == 'A':  # uppercase A-M
        shift = shift1 #shift by shift1 in case it's uppercase A-M
        new_pos = ord(c) - ord('A') - shift #get the raw order of the shift by removing the ord of 'A' (first letter)
        while new_pos < 0: #continuously shift forward by adding 26 until position is within valid range (0-25)
            new_pos = new_pos + 26
        return chr(new_pos + ord('A')) #return the character of the new position (we add ord(A) because this is the starting point of the capital alphabet)
    
    if flag == 'B':  # uppercase N-Z
        shift = shift2 ** 2 #shift by shift2^2 in case it's uppercase N-Z
        new_pos = ord(c) - ord('A') + shift #get the raw order of the shift by removing the ord of 'A' (first letter)
        while new_pos >= 26: #continuously wrap around by subtracting 26 until position is within valid range (0-25)
            new_pos = new_pos - 26
        return chr(new_pos + ord('A')) #return the character of the new position (we add ord(A) because this is the starting point of the capital alphabet)
    
    return c  # other characters unchanged

def decrypt_char(c, flag, shift1, shift2):
    """
    Decrypt a single character based on its classification flag and shift values.
    """
    if flag == 'a':  # lowercase a-m
        shift = shift1 * shift2 #shift by shift1*shift2 in case it's lowercase a-m (reverse of encryption)
        new_pos = ord(c) - ord('a') - shift #get the raw order of the shift by removing the ord of 'a' (first letter)
        while new_pos < 0: #continuously shift forward by adding 26 until position is within valid range (0-25)
            new_pos = new_pos + 26
        return chr(new_pos + ord('a')) #return the character of the new position (we add ord(a) because this is the starting point of the small alphabet)
    
    if flag == 'b':  # lowercase n-z
        shift = shift1 + shift2 #shift by shift1+shift2 in case it's lowercase n-z (reverse of encryption)
        new_pos = ord(c) - ord('a') + shift #get the raw order of the shift by removing the ord of 'a' (first letter)
        while new_pos >= 26: #continuously wrap around by subtracting 26 until position is within valid range (0-25)
            new_pos = new_pos - 26
        return chr(new_pos + ord('a')) #return the character of the new position (we add ord(a) because this is the starting point of the small alphabet)
    
    if flag == 'A':  # uppercase A-M
        shift = shift1 #shift by shift1 in case it's uppercase A-M (reverse of encryption)
        new_pos = ord(c) - ord('A') + shift #get the raw order of the shift by removing the ord of 'A' (first letter)
        while new_pos >= 26: #continuously wrap around by subtracting 26 until position is within valid range (0-25)
            new_pos = new_pos - 26
        return chr(new_pos + ord('A')) #return the character of the new position (we add ord(A) because this is the starting point of the capital alphabet)
    
    if flag == 'B':  # uppercase N-Z
        shift = shift2 ** 2 #shift by shift2^2 in case it's uppercase N-Z (reverse of encryption)
        new_pos = ord(c) - ord('A') - shift #get the raw order of the shift by removing the ord of 'A' (first letter)
        while new_pos < 0: #continuously shift forward by adding 26 until position is within valid range (0-25)
            new_pos = new_pos + 26
        return chr(new_pos + ord('A')) #return the character of the new position (we add ord(A) because this is the starting point of the capital alphabet)
    
    return c  # other characters unchanged

def encrypt_file(shift1, shift2):
    """
    Encrypt the contents of "raw_text.txt" and save to "encrypted_text.txt".

    Stores a metadata line at the top indicating the classification of each character.
    """
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as f:  # Safely read the raw text file
            text = f.read()
    except Exception as e:
        print("Failed to read raw_text.txt:", e)
        return

    # Step 1: Create classification flags for each character
    # This tells us which half of the alphabet each character belongs to
    flags = ""
    for character in text:
        character_flag = classify_char(character) #Whether its from the first part or the second part, it takes one of these flags: (a,b,A,B,0), explained in detail in classify_char function.
        flags += character_flag
    
    # Step 2: Encrypt each character using its corresponding flag
    encrypted = ""
    for i in range(len(text)):
        original_char = text[i] #get the character
        char_flag = flags[i] #get its corresponding flag
        encrypted_char = encrypt_char(original_char, char_flag, shift1, shift2) #encrypt the character based on its flag
        encrypted += encrypted_char #add the character back to the encrypted string.

    try:
        with open("encrypted_text.txt", "w", encoding="utf-8") as f:  # Overwrite or create output file safely
            f.write(flags + "\n")
            f.write(encrypted)
    except Exception as e:
        print("Failed to write encrypted_text.txt:", e)
        return

def decrypt_file(shift1, shift2):
    """
    Decrypt the contents of "encrypted_text.txt" and save to "decrypted_text.txt".
    """
    try:
        with open("encrypted_text.txt", "r", encoding="utf-8") as f:  # Read the encrypted file
            first_line = f.readline()
            flags = first_line.strip()
            encrypted_text = f.read()
    except Exception as e:
        print("Failed to read encrypted_text.txt:", e)
        return

    if len(flags) != len(encrypted_text):
        print("Metadata length does not match encrypted content length")
        return
    
    # Decrypt each character using its corresponding flag
    decrypted = ""
    for i in range(len(encrypted_text)):
        encrypted_char = encrypted_text[i]  # Get the encrypted character
        char_flag = flags[i] # Get its corresponding flag
        decrypted_char = decrypt_char(encrypted_char, char_flag, shift1, shift2) #decrypt the character using the function
        decrypted += decrypted_char # Add the decrypted character to result

    try:
        with open("decrypted_text.txt", "w", encoding="utf-8") as f:  # Overwrite or create output file
            f.write(decrypted)
    except Exception as e:
        print("Failed to write decrypted_text.txt:", e)
        return

def verify():
    """
    Compare "raw_text.txt" and "decrypted_text.txt" and print whether decryption was successful.
    """
    try:
        with open("raw_text.txt", "r", encoding="utf-8") as f1, open("decrypted_text.txt", "r", encoding="utf-8") as f2:
            original = f1.read()
            decrypted = f2.read()
    except Exception as e:
        print("Failed to verify files:", e)
        return

    # Compare the two texts to see if decryption worked correctly
    if original == decrypted:
        print("Decryption Verified Successfully ") # The texts match - decryption worked
    else:
        print("Decryption failed ") # The texts don't match - something went wrong



def get_int_from_user(name): 
    """
    Take input from user and check wether if it's a string, float, or INT

    in case it's a string, ask the user to re-enter the value
    in case it's a float, round the value to the nearest int
    in case it's an int, proceed normally.
    """

    isNumber = False #Variable to keep track wether we have a number or not
    while isNumber == False: #This while loop keeps going until we have a number.
        try:
            user_input = input(str(name)) #write a custom message to the user
            try:
                val = float(user_input) #Round the float numbers to get an int (without breaking the loop to make it more smooth for the user)
                user_input = round(val)
            except (ValueError, TypeError):
                # If conversion to float fails, we'll try int() below which will also raise on invalid input
                pass

            val = int(user_input) #if this did not go to the except, we have got a valid number
            isNumber = True #mark that we got a number
            return val #Return the number and exit the while loop
        except Exception:
            print("That's not a number! Please enter a valid, correct number.")
            #Do A while loop here to get the number

def main():
    """Entry point for Question 1 encryption/decryption workflow."""
    shift1 = get_int_from_user("Enter shift1: ")
    shift2 = get_int_from_user("Enter shift2: ")

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify()


if __name__ == "__main__":
    main()
