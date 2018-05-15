from PoC.server import ServerAuthenticator
from PoC.client import ClientAuthenticator

server = ServerAuthenticator()
client = ClientAuthenticator(server.export_key())

while True:
    try:
        input("Press to generate token")
        print("Server token:", server.generate_token())
        print("Client token:", client.generate_token())
    except KeyboardInterrupt:
        print("\nExiting")
        break
