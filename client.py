from ecdh import ECDH
import threading
import time
from tables import *
import random


class Client:
    def __init__(self, network_manager):
        self.network_manager = network_manager
        self.ecdh = ECDH(network_manager)
        self.running = False
        self.proposed_key = False
        self.host = False

        self.keep_scope = None

        # key_exchange, in_chat
        self.state = 'in_chat'

    def run(self):
        if not self.running:
            self.start_listener_thread()
            self.running = True

        if self.state == 'key_exchange':
            pass
        elif self.state == 'in_chat':
            self.send_message()  # Main thread handles sending only


    def start_listener_thread(self):
        listener_thread = threading.Thread(target=self.listen, daemon=True)
        listener_thread.start()


    def send_message(self):
        print("Send a message")
        while self.running:
            message = input()
            if message.lower() == 'quit':
                self.running = False
                break
            self.network_manager.send_data(message.encode())

    def listen(self):
        """Background thread - handles ALL receiving"""
        while self.running:
            self.network_manager.receive()
            msg = self.network_manager.search_queue()
            if msg:
                if self.state == 'key_exchange':
                    self.handle_key_exchange_message(msg)
                elif self.state == 'in_chat':
                    print(f"\nPartner: {msg}")
            time.sleep(0.05)

    def send_key_exchange_message(self):
        if not self.host and not self.proposed_key:
            proposed_key = random.choice(CURVES)
            self.network_manager.send_data(f"I propose {proposed_key}", "AW1", proposed_key)


    def handle_key_exchange_message(self, msg):
        # Handle key exchange protocol messages
        print(f"\nKey exchange: {msg}")

        self.keep_scope = 1

        match msg[2]:
            case "AW1":
                pass
            case "AW2":
                pass
                print("--------- Connect complete ---------")
            case "KW1":
                pass
            case "NIL":
                pass

        pass