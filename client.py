import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Initialize colors
init()

# Set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]

# Choose a random color for the client
client_color = random.choice(colors)

# Server's IP address
# If the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "192.168.1.56"
SERVER_PORT = 8000  # Server's port
separator_token = "<SEP>"  # We will use this to separate the client name & message

# Initialize TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    # Connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")
    # Prompt the client for a name
    name = input("Enter your name: ").strip()
    print('send the lowercase letter "q" to leave the chat')

    # Function to listen for messages from the server
    def listen_for_messages():
        while True:
            try:
                message = s.recv(1024).decode()
            except ConnectionAbortedError:
                print(f"\n[!] Connection to {SERVER_HOST}:{SERVER_PORT} was closed.")
                break
            print(message)

    # Create a thread that listens for messages to this client & prints them
    t = Thread(target=listen_for_messages)
    # Make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # Start the thread
    t.start()

    # Loop to send messages to the server
    while True:
        # Input message we want to send to the server
        to_send = input().strip()
        # A way to exit the program
        if to_send.lower() == 'q':
            break
        # Add the datetime, name, and the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
        # Finally, send the message
        try:
            s.send(to_send.encode())
        except ConnectionAbortedError:
            print(f"\n[!] Connection to {SERVER_HOST}:{SERVER_PORT} was closed.")
            break

# End of program
