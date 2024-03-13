import unittest
import socket
import threading
import pickle
from Server_code import generate_key_and_save_to_file, decrypt_file, save_data, handle_client

class TestServer(unittest.TestCase):
    def setUp(self):
        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=start_server_thread)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        # Stop the server
        stop_server()

    def test_handle_client(self):
        # Create a client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 6868))

        # Test data
        data = {'key': 'value'}
        encrypted_data = pickle.dumps(data)

        # Send data to the server
        client_socket.sendall(encrypted_data)

        # Receive acknowledgment
        response = client_socket.recv(1024)
        self.assertEqual(response, b'Data and file received successfully.')

        # Close client socket
        client_socket.close()

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

if __name__ == '__main__':
    unittest.main()
