from PoC.server import ServerAuthenticator
from PoC.client import ClientAuthenticator

mfa = 'CG80ZC7LLdXqWCSZDSz6Kg=='
server = ServerAuthenticator(mfa)
client = ClientAuthenticator(server.export_key())

while True:
    try:
        print("Server previous token:", server.get_previous_token())
        print("Server token:", server.generate_token())
        print("Client token:", client.generate_token(), "\nTime left:", client.get_time_left(), "seconds |",
              client.get_percent_left(), "%")
        print("MFA :",server.export_key())
        input("Press to generate token")
    except KeyboardInterrupt:
        print("\nExiting")
        break
