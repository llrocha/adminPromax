from cryptography.fernet import Fernet
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

    def call_method(self, class_name, method_name, params = []):
        print("CLASS=>METHOD({0}.{1})".format(class_name, method_name))
        print("CLASS=>({0})".format(type(class_name)))
        try:
            class_type = getattr(controls, class_name)
        except AttributeError as e:
            class_type = None
            print("Attribute Error({0}): {1}".format(e.errno, e.strerror))

        try:
            method = getattr(controls, class_name)
        except AttributeError as e:
            method = None
            print("Attribute Error({0}): {1}".format(e.errno, e.strerror))

        geo = 'h1'
        if(class_type and method):
            obj = class_type(geo)
            method = getattr(obj, method_name)
            data = method()
        else:
            data = 'None'
        if(type(data) is str):
            return self.fernet_key.encrypt(data.encode('utf-8'))
        else:
            return self.fernet_key.encrypt(data)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{0} wrote: {1}".format(self.client_address[0], self.data))
    
        request = self.fernet_key.decrypt(self.data)
        request = str(request,'utf-8')
        print('CALL={0}'.format(request))
        command = request.split('.')
        #for item in command:
        #    print(item)
        class_name = command[0]
        method_name = command[1]
        print('CALL={0}'.format(class_name))
        print('CALL={0}'.format(method_name))

        data = self.call_method(class_name, method_name)

        # just send back the same data, but upper-cased
        self.request.sendall(data)


if __name__ == "__main__":
    HOST, PORT = "0", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), ControlServerTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
