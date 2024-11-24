import socket  # For creating sockets
import threading  # For handling concurrent sending and receiving of messages
from termcolor import colored  # For adding colors to text


class ChatClient:
    """
    A class to represent a chat client with colored messages for better readability.
    """
    def __init__(self, host="127.0.0.1", port=3030, color="blue"):
        """
        Initialize the chat client.

        :param host: The server's IP address (default is localhost).
        :param port: The server's port number (default is 3030).
        :param color: The color used to display the client's messages.
        """
        self.host = host  # Server's IP address
        self.port = port  # Server's port number
        self.color = color  # Client's unique message color
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket

    def connect_to_server(self):
        """
        Connect to the chat server and start the client.
        """
        try:
            self.client_socket.connect((self.host, self.port))  # Attempt to connect to the server
            print(colored(f"Connected to server at {self.host}:{self.port}", "green"))  # Success message

            # Start a thread for receiving messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
            # Begin the sending loop on the main thread
            self.send_messages()
        except ConnectionRefusedError:
            print(colored("Connection refused. Ensure the server is running.", "red"))
        except Exception as e:
            print(colored(f"An error occurred: {e}", "red"))
        finally:
            self.client_socket.close()  # Ensure the socket is closed if connection fails

    def send_messages(self):
        """
        Handles sending messages to the server.
        """
        try:
            while True:  # Continuous loop for sending messages
                message = input(colored("You: ", self.color))  # Prompt user for input in their color
                if message.strip():  # Avoid sending empty messages
                    self.client_socket.sendall(f"[COLOR ({self.color})] said -> {message}".encode('utf-8'))  # Encode the entire string and sends it to the server for broadcasting

        except BrokenPipeError:
            print(colored("Connection to the server was lost.", "red"))
        except Exception as e:
            print(colored(f"Error sending message: {e}", "red"))
        finally:
            self.client_socket.close()
            print(colored("Disconnected from server.", "yellow"))

    def receive_messages(self):
        """
        Handles receiving messages from the server.
        """
        while True:
            try:
                # Receive and decode messages from the server
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:  # If an empty message is received, assume disconnection
                    break
                print(colored(f"\n{message}", "cyan"))  # Print messages from the server in cyan
            except ConnectionResetError:
                print(colored("Connection reset by server.", "red"))
                break
            except Exception:
                break


if __name__ == "__main__":
    # Assign a unique color to the client (e.g., blue for the current instance)
    client = ChatClient(color="blue")  # You can change the color for each instance
    client.connect_to_server()
