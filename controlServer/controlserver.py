from cryptography.fernet import Fernet
from datetime import datetime
import socketserver
import controls

class ControlServerTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    #cryptography
    key = b'Z7KxlRurgMcxBt7F54zteD2mHVkOrZdF2ycz7eMvIII='
    fernet_key = Fernet(key)
    sc = controls.ServerControls('h1')

    #def __init__(self, request, client_address, server):
    #    super(self.__class__, self).__init__(request, client_address, server)
        
    def LogMsg(self, msg):
        print('[{0}] - {1}'.format(datetime.now(), msg))

    def handle(self):
        # self.request is the TCP socket connected to the client
        client_address = self.client_address[0]
        self.data = self.request.recv(1024).strip()        
        self.LogMsg("{0} wrote: {1}".format(client_address, self.data))
    
        request = self.fernet_key.decrypt(self.data)
        request = str(request,'utf-8')
        self.LogMsg('{0} call: {1}'.format(client_address, request))
        command = request.split('->')

        class_name = command[0]
        method_name = command[1]
        params = command[2:]

        log = '{0} wrote: class.method={1}.{2}({3})'.format(client_address, class_name, method_name, ', '.join(params))
        self.LogMsg(log)

        try:
            obj = self.sc.factory[class_name]
            method = getattr(obj, method_name)
            data = method(*params)
            if(type(data) is str):
                data = data.encode('utf-8')

            self.LogMsg(data)
        except:
            data = 'Ocorreu um erro no processamento'.encode('utf-8')
            self.LogMsg(data)
            raise

        data = self.fernet_key.encrypt(data)

        self.LogMsg(data)

        # just send back the same data, but upper-cased
        self.request.sendall(data)


if __name__ == "__main__":
    HOST, PORT = "0", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), ControlServerTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
server.serve_forever()