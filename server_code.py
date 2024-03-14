import socket
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet
import os

SERIALIZE_FORMAT = {
    "plaintext": 0,
    "binary": 1,
    "json": 2,
    "xml": 3
}

HEADER_LENGTH = 4
MSG_FORMAT_LENGTH = 1

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


def process_msg(msg, msg_format):
    if msg_format == SERIALIZE_FORMAT["binary"]:
        received_dict = pickle.loads(msg)
    elif msg_format == SERIALIZE_FORMAT["json"]:
        received_dict = json.loads(msg.decode('utf-8'))
    elif msg_format == SERIALIZE_FORMAT["xml"]:
        root = ET.fromstring(msg)
        received_dict = {}
        for child in root:
            received_dict[child.tag] = child.text
    elif msg_format == SERIALIZE_FORMAT["plaintext"]:
        received_dict = decrypt_file(msg.decode('utf-8'))
        with open("GroupB_sample_textfile_Decryp.txt", "wb") as f:
            f.write(received_dict)
    else:
        raise ValueError("Invalid pickling format")
    return received_dict


def handle_client(conn, addr, pickling_format, save_to_file=False):
    print(f"Connection from {addr} has been established.")
    
    # Receive pickled data based on selected format
    data = b''

    while True:
        # chunk = conn.recv(4096)
        # if not chunk:
        #     break
        # data += chunk

        header = conn.recv(HEADER_LENGTH)
        if not header:
            # no header received
            break

        msg_len = int.from_bytes(header[0:HEADER_LENGTH], byteorder='big')
        file_format_bytes = conn.recv(MSG_FORMAT_LENGTH)
        file_format = int.from_bytes(file_format_bytes, byteorder='big')

        print(f"msg_len = {msg_len}, file_format = {file_format}")

        chunks = []
        bytes_received = 0
        while bytes_received < msg_len:
            chunk = conn.recv(min(4096, msg_len - bytes_received))
            if not chunk:
                break
            chunks.append(chunk)
            bytes_received += len(chunk)

        data = b"".join(chunks)
        received_dict = process_msg(data, file_format)
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
