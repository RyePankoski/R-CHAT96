from client import Client
from network_manager import NetworkManager


class Controller:
    def __init__(self):
        self.network_manager = NetworkManager()
        self.client = Client(self.network_manager)

        # menu, in_chat
        self.state = 'menu'

    def run(self):
        if self.state == 'menu':
            self.menu()
        elif self.state == 'in_chat':
            self.client.run()


    def menu(self):
        print("1: To start server, press s")
        print("2: To stop server, press q")
        print("3: To join server, press j")

        choice = input()

        if choice == "s":
            print("Starting server...")
            self.network_manager.host()
            self.network_manager.host = True
            self.state = 'in_chat'
        elif choice == "q":
            print("Stopping server...")
            self.network_manager.close()
            self.state = 'menu'
        elif choice == "j":
            print("Joining server...")
            self.network_manager.connect_to("174.29.116.168", 4242)
            self.network_manager.host = False
            self.state = 'in_chat'
        else:
            print("Invalid choice")
            return




