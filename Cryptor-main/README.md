# Cryptor: Secure Information Management Tool

Cryptor is a Python-based application designed to provide secure management for sensitive information such as login credentials, passwords, and images. It offers functionalities for storing encrypted credentials, managing images, and ensuring data confidentiality.

## Modules Used

Cryptor utilizes several Python modules to implement its features:

- `tkinter`: Used for building the user interface (UI) of the application.
- `sqlite3`: Enables interaction with the SQLite database for storing and retrieving login credentials.
- `csv`: Facilitates reading and writing CSV files, although not utilized in the final version of the application.
- `base64`: Provides functions for encoding and decoding data, used for encrypting and decrypting passwords.
- `PIL`: Python Imaging Library, used for image manipulation such as encryption and decryption.
- `os`: Used for basic operating system operations like directory creation.

## Functions and Usage

### 1. `add_login_info()`

This function is responsible for adding login information to the database. It encrypts the password using a secret key before storing it. The user is prompted to input the website, username, and password. If any of these fields are empty, an appropriate warning message is displayed.

### 2. `view_login_info()`

This function displays the saved login information from the database. It retrieves data from the SQLite database and displays it in a separate window. Passwords are decrypted using the same secret key used for encryption during storage.

### 3. `encrypt_image()` and `decrypt_image()`

These functions allow users to encrypt and decrypt images, respectively. They utilize the Python Imaging Library (PIL) for image manipulation. Images are XOR encrypted, and users can select an image file for encryption or decryption.

## How to Run

1. Ensure you have Python installed on your system (Python 3.x recommended).
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Run the following command to execute the application:

```bash
python cryptor.py
