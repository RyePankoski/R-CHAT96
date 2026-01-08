import socket

class NetworkManager:
    def __init__(self):
        self.server_socket = None  # Only used if we're hosting
        self.connection_socket = None  # The actual connection for communication
        self.is_server = False
        self.message_queue = []

    def host(self, port=4242):
        self.is_server = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(1)
        print(f"Hosting on port {port}, waiting for connection...")

        # Accept the connection
        self.connection_socket, address = self.server_socket.accept()
        self.connection_socket.setblocking(False)  # Make non-blocking
        print(f"Partner connected from {address}")

    def connect_to(self, host, port=4242):
        self.is_server = False
        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.connect((host, port))
        self.connection_socket.setblocking(False)  # Make non-blocking
        print(f"Connected to {host}:{port}")

    def send_data(self, data):
        if self.connection_socket:
            self.connection_socket.send(data)

    def receive(self, buffer_size=1024):
        if self.connection_socket:
            try:
                data = self.connection_socket.recv(buffer_size)
                if data:
                    self.message_queue.append(data)
            except BlockingIOError:
                pass  # No data available right now

    def search_queue(self):
        if self.message_queue:
            message = self.message_queue.pop(0)
            return message.decode('utf-8')
        return None

    def close(self):
        if self.connection_socket:
            self.connection_socket.close()
        if self.server_socket:
            self.server_socket.close()