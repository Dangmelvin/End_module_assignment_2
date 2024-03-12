import socket
import pickle
from cryptography.fernet import Fernet
import os

def get_key_from_file(filename="GroupB.key"):
    if not os.path.exists(filename):
        raise Exception(f"{filename} file not found")

    with open(filename, "rb") as key_file:
        _key = key_file.read()
    return _key

# Generate a key for Fernet encryption
key = get_key_from_file()
cipher = Fernet(key)

def encrypt_file(file_path):
    with open(file_path, "rb") as f:
        plaintext = f.read()
        encrypted_data = cipher.encrypt(plaintext)
    return encrypted_data

def send_data_to_server(data, filename):
    HOST = '127.0.0.1'
    PORT = 6868

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Send pickled dictionary
    pickled_data = pickle.dumps(data)
    client.sendall(pickled_data)

    # Encrypt and send text file
    encrypted_data = encrypt_file(filename)
    client.sendall(encrypted_data)

    client.close()

def main():
    # Sample dictionary
    data = {'key1': 'Aljunaydi', 'Azmi': 'Dong', 'Thomas': 'Adhir'}

    # Sample text file to be encrypted
    with open("GroupB_sample_textfile.txt", "w") as f:
        f.write("We are doing the End_module Assignment for week 8 including Aljunaydi, Azmi Chahal, Dang Dong, Thomas Lundie, Adhir Soechit.")

    send_data_to_server(data, "GroupB_sample_textfile.txt")
    print("Data and file sent to server successfully.")

if __name__ == "__main__":
    main()
