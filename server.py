import socket
import threading


class ChatServer:
    """
    A simple chat server that allows multiple clients to connect and exchange messages in real-time.

    Attributes:
        host (str): The IP address the server binds to.
        port (int): The port the server listens on.
        server_socket (socket.socket): The main server socket for accepting client connections.
        clients (list): A list of connected client sockets.
    """

    def __init__(self, host="127.0.0.1", port=3030):
        """
        Initializes the ChatServer with a host and port.

        Args:
            host (str): The IP address the server will bind to. Defaults to "127.0.0.1".
            port (int): The port the server will listen on. Defaults to 3030.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start_server(self):
        """
        Starts the chat server, binds it to the host and port, and listens for client connections.
        Each client connection is handled in a separate thread.
        """
        try:
            # Bind the server to the specified host and port
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)  # Allow up to 5 queued connection attempts
            print(f"Server started on {self.host}:{self.port}")

            while True:
                # Accept a new client connection
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from: {client_address}")

                # Add the client socket to the list of clients
                self.clients.append(client_socket)

                # Start a new thread to handle communication with this client
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        """
        Handles communication with a connected client.

        Args:
            client_socket (socket.socket): The client's socket.
        """
        try:
            while True:
                # Receive a message from the client
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break  # If the client sends an empty message, disconnect

                print(f"Received message: {message}")
                # Broadcast the message to all other clients
                self.broadcast_message(message, client_socket)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            # Remove the client from the list and close its connection
            print("Client disconnected.")
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()

    def broadcast_message(self, message, sender_socket):
        """
        Sends a message to all connected clients except the sender.

        Args:
            message (str): The message to broadcast.
            sender_socket (socket.socket): The socket of the client that sent the message.
        """
        for client in self.clients:
            if client != sender_socket:  # Avoid sending the message back to the sender
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error broadcasting to a client: {e}")


if __name__ == "__main__":
    # Create and start the chat server
    server = ChatServer()
    server.start_server()
