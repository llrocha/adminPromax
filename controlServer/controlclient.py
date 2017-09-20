from cryptography.fernet import Fernet
import logging
import socket
import sys





#logging.basicConfig(filename='log.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#create file handler
handler = logging.FileHandler('controlclient.log')
handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
#formatter.datefmt = '[%Y-%m-%d %H:%M:%S]'
handler.setFormatter(formatter)

logger.addHandler(handler)

#TEST
#logger.debug('debug - Watch out!')  # will print a message to the console
#logger.info('info - I told you so')  # will not print anything
#logger.warning('warning - Watch out!')  # will print a message to the console
#logger.error('error - I told you so')  # will not print anything
#logger.critical('critical - Watch out!')  # will print a message to the console



def ExecuteRemoteCommand(host, port, command):
    
    logger.debug("Sent:     {}".format(command))
    try:
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
            
        response = str(fernet_key.decrypt(response.encode('utf-8')), 'utf-8')
        
        logger.debug("Received: {}".format(response))
    except Exception as e:
        response = "Attribute Error({0}): {1}".format(e.errno, e.strerror)

    return response


if __name__ == "__main__":
    HOST, PORT = "90.0.2.174", 9999
    data = " ".join(sys.argv[1:])

    print(ExecuteRemoteCommand(HOST, PORT, data))

    
