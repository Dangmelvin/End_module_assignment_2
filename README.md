### End_Module_Assignment_Group B
### Members: Aljunaydi, Azmi Chahal, Dang Dong, Thomas Lundie, Adhir Soechit
### Overview
This project implements a client-server network where the client can send dictionary data or text files to the server. The client can specify the pickling format for dictionary data and also choose to encrypt files before sending.

### Architecture
        +-------------------+           +-------------------+
        |                   |           |                   |
        |      Client       |           |      Server       |
        |                   |           |                   |
        +-------------------+           +-------------------+
                 |                               |
                 |          Localhost            |
                 | <---------------------------> |
                 |                               |
                 |      Send pickled data        |
                 | ----------------------------> |
                 |                               |
                 |     Encrypt & send file       |
                 | ----------------------------> |
                 |                               |
                 |                               |
                 |        Receive pickled data   |
                 | <---------------------------- |
                 |                               |
                 |   Receive and decrypt file    |
                 | <---------------------------- |
                 |                               |
                 |     Save decrypted file       |
                 |                               |
##### Both the client and the server run on the same localhost.
##### The client encrypts the data and sends it over a socket connection to the server.
##### The server receives the serialized dictionary, decrypts it, and processes it.
##### The server receives the encrypted data, decrypts it, and processes it.
##### IP (127.0.0.1) /port (6688) communication is established between the client and the server using sockets.               


### Unit test
to be updated.

### license
Distributed under the MIT License. See LICENSE.txt for more information.

### Instructions:

#### Running the Server:
##### Open a terminal or command prompt.
##### Navigate to the directory containing server.py.
##### Run the command: python server.py
##### The server will start listening for incoming connections on the specified host and port as above architectre

#### Running the Client:
##### Open another terminal or command prompt.
##### Navigate to the directory containing client.py.
##### Run the command: python client.py
##### The client will connect to the server and send dictionary data and files
