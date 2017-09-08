from cryptography.fernet import Fernet
import socket
import sys


def ExecuteRemoteCommand(host, port, command):
    print("Sent:     {}".format(command))

    #cryptography
    key = b'Z7KxlRurgMcxBt7F54zteD2mHVkOrZdF2ycz7eMvIII='
    fernet_key = Fernet(key)

    token = fernet_key.encrypt(command.encode('utf-8'))

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to server and send data
    sock.connect((host, port))
    sock.sendall(token)

    # Receive data from the server and shut down
    response = ''
    while(True):
        chunk = sock.recv(1024)
        if(not chunk):
            break
        response += str(chunk, 'utf-8')
        
    response = fernet_key.decrypt(response.encode('utf-8'))

    
    
    print("Received: {}".format(response))

    return response


if __name__ == "__main__":
    HOST, PORT = "90.0.2.174", 9999
    data = " ".join(sys.argv[1:])

    ExecuteRemoteCommand(HOST, PORT, data)

    
