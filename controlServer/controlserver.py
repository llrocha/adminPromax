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

    def call_method(self, class_name, method_name, params = []):
        self.LogMsg("CLASS=>METHOD({0}.{1})".format(class_name, method_name))
        self.LogMsg("CLASS=>({0})".format(type(class_name)))
        try:
            class_type = getattr(controls, class_name)
        except AttributeError as e:
            class_type = None
            self.LogMsg("Attribute Error({0}): {1}".format(e.errno, e.strerror))

        try:
            method = getattr(controls, class_name)
        except AttributeError as e:
            method = None
            self.LogMsg("Attribute Error({0}): {1}".format(e.errno, e.strerror))

        geo = 'h1'
        try:
            obj = class_type(geo)
            method = getattr(obj, method_name)
            data = method(*params)

            if(type(data) is str):
                return self.fernet_key.encrypt(data.encode('utf-8'))
            else:
                return self.fernet_key.encrypt(data)
        except:
            data = 'Ocorreu um erro no processamento'.encode('utf-8')
            return self.fernet_key.encrypt(data)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        self.LogMsg("{0} wrote: {1}".format(self.client_address[0], self.data))
    
        request = self.fernet_key.decrypt(self.data)
        request = str(request,'utf-8')
        self.LogMsg('CALL={0}'.format(request))
        command = request.split('->')

        class_name = command[0]
        method_name = command[1]
        params = command[2:]

        self.LogMsg('class={0}'.format(class_name))
        self.LogMsg('method={0}'.format(method_name))
        c = 0
        for param in params:
            self.LogMsg('param{0}={1}'.format(c, param))
            c += 1

        #data = self.call_method(class_name, method_name, params)
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

        self.fernet_key.encrypt(data)

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