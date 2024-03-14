import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet
import os

def generate_key_and_save_to_file(filename="GroupB.key"):
    # check key exist before generating
    if os.path.exists(filename):
        with open(filename, "rb") as key_file:
            _key = key_file.read()
        return _key

    _key = Fernet.generate_key()
    with open(filename, "wb") as key_file:
        key_file.write(_key)
    return _key

# Generate a key for Fernet encryption
key = generate_key_and_save_to_file()
cipher = Fernet(key)

def decrypt_file(encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

def save_data(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def handle_client(conn, addr, pickling_format, save_to_file=False):
    print(f"Connection from {addr} has been established.")
    
    # Receive pickled data based on selected format
    data = b''
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    
    if pickling_format == "binary":
        received_dict = pickle.loads(data)
    elif pickling_format == "json":
        received_dict = json.loads(data.decode('utf-8'))
    elif pickling_format == "xml":
        root = ET.fromstring(data)
        received_dict = {}
        for child in root:
            received_dict[child.tag] = child.text
    else:
        raise ValueError("Invalid pickling format")
    
    # Receive and decrypt text file
    encrypted_data = b''
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        encrypted_data += chunk
    
    decrypted_data = decrypt_file(encrypted_data)
    with open("GroupB_sample_textfile_Decryp.txt", "wb") as f:
        f.write(decrypted_data)
    
    if save_to_file:
        save_data(received_dict, "received_data.pkl")
    
    print("Data and file received successfully.")

    conn.close()

def start_server(pickling_format, save_to_file=False):
    HOST = '127.0.0.1'
    PORT = 6868

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server listening on port", PORT)

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr, pickling_format, save_to_file)

if __name__ == "__main__":
    pickling_format = "json"  # Change this to "binary", "json", or "xml" as desired
    start_server(pickling_format, save_to_file=True)  # Set save_to_file to True if you want to save received data to a file
