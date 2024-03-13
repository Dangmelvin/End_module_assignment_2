import unittest
import pickle
import socket
import threading
from End_module_assignment_final.Client_code import send_data_to_server
from End_module_assignment_final.Server_code import decrypt_file, save_data

class TestClient(unittest.TestCase):
    def setUp(self):
        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=start_server_thread)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        # Stop the server
        stop_server()

    def test_send_data_to_server(self):
        # Test data
        data = {'key1': 'Aljunaydi', 'Azmi': 'Dong', 'Thomas': 'Adhir'}
        file_path = "test_textfile.txt"
        with open(file_path, "w") as f:
            f.write("Test data for encryption")

        # Send data to the server
        send_data_to_server(data, file_path)

        # Check if the server received the data and file successfully
        received_data, received_file = read_received_data()
        
        # Check if the received data matches the sent data
        self.assertEqual(data, received_data)

        # Check if the received file matches the sent file after decryption
        with open("test_textfile.txt", "rb") as f:
            sent_file_content = f.read()
        self.assertEqual(sent_file_content, received_file)

def start_server_thread():
    save_to_file = True
    HOST = '127.0.0.1'
    PORT = 6868

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr, save_to_file)

def stop_server():
    # Connect to the server just to break its loop
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 6868))
    client_socket.close()

def handle_client(conn, addr, save_to_file=False):
    # Receive pickled dictionary
    data = conn.recv(4096)
    received_dict = pickle.loads(data)
    
    # Receive and decrypt text file
    encrypted_data = b''
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        encrypted_data += chunk
    
    decrypted_data = decrypt_file(encrypted_data)
    
    if save_to_file:
        save_data(received_dict, "received_data.pkl")
        with open("received_textfile.txt", "wb") as f:
            f.write(decrypted_data)
    
    conn.sendall(b'Data and file received successfully.')

def read_received_data():
    with open("received_data.pkl", "rb") as f:
        received_data = pickle.load(f)
    with open("received_textfile.txt", "rb") as f:
        received_file = f.read()
    return received_data, received_file

if __name__ == '__main__':
    unittest.main()
