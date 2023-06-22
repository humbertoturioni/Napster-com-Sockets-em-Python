import socket
import threading

class PeerServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 7777
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.connections = []
        self.file_addresses = {
            'file1.txt': 'http://peerx.com/file1.txt',
            'file2.txt': 'http://peery.com/file2.txt',
            'file3.txt': 'http://peerz.com/file3.txt'
        }

    def listen(self):
        self.server.listen(5)
        print(f"PeerServer listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server.accept()
            self.connections.append(conn)
            print(f"Connected to {addr}")

            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        request = conn.recv(1024).decode()
        if request == 'get_file_addresses':
            conn.send(str(self.file_addresses).encode())
        conn.close()

    def close(self):
        self.server.close()

class Peer:
    def __init__(self, name):
        self.name = name
        self.host = 'localhost'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_server_address = ('localhost', 7777)
        self.file_addresses = {}

    def connect_to_peer_server(self):
        self.server.connect(self.peer_server_address)
        self.server.send('get_file_addresses'.encode())
        self.file_addresses = eval(self.server.recv(1024).decode())
        self.server.close()
        print(f"{self.name} connected to PeerServer")

    def download_file(self, filename):
        if filename not in self.file_addresses:
            print(f"{self.name}: File '{filename}' not found.")
            return

        file_address = self.file_addresses[filename]
        print(f"{self.name}: Downloading file '{filename}' from {file_address}")

        # Implement your file download logic here
        # You can use libraries like 'requests' or 'urllib' to download the file

    def close(self):
        self.server.close()

if __name__ == '__main__':
    peer_server = PeerServer()
    peer_server_thread = threading.Thread(target=peer_server.listen)
    peer_server_thread.start()

    peer_x = Peer('PeerX')
    peer_y = Peer('PeerY')
    peer_z = Peer('PeerZ')

    peer_x.connect_to_peer_server()
    peer_y.connect_to_peer_server()
    peer_z.connect_to_peer_server()

    # Example file download
    peer_x.download_file('file1.txt')

    peer_server.close()
    peer_x.close()
    peer_y.close()
    peer_z.close()
    peer_server_thread.join()
