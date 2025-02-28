import socket
import threading
import pickle

groups = {}
lock = threading.Lock()

class Group:
    def __init__(self, admin, client):
        self.admin = admin
        self.clients = {admin: client}
        self.allMembers = {admin}
        self.onlineMembers = {admin}
        self.joinRequests = set()
        self.waitClients = {}

    def disconnect(self, username):
        if username in self.onlineMembers:
            self.onlineMembers.remove(username)
        if username in self.clients:
            del self.clients[username]

    def connect(self, username, client):
        self.onlineMembers.add(username)
        self.clients[username] = client

    def sendMessage(self, message, sender):
        for member in self.onlineMembers:
            if member != sender:
                self.clients[member].send(f"{sender}: {message}".encode("utf-8"))

def clientHandler(client, username, groupname):
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            if msg == "/disconnect":
                groups[groupname].disconnect(username)
                print(f"User {username} disconnected from {groupname}.")
                break
            elif msg == "/messageSend":
                message = client.recv(1024).decode("utf-8")
                groups[groupname].sendMessage(message, username)
            elif msg == "/allMembers":
                client.send(pickle.dumps(groups[groupname].allMembers))
            elif msg == "/onlineMembers":
                client.send(pickle.dumps(groups[groupname].onlineMembers))
            elif msg == "/whoAdmin":
                client.send(f"Admin: {groups[groupname].admin}".encode("utf-8"))
            else:
                print("Unknown command:", msg)
        except Exception as e:
            print("Error:", e)
            break
    client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8000))
    server.listen(10)
    print("Server running...")

    while True:
        client, _ = server.accept()
        username = client.recv(1024).decode("utf-8")
        client.recv(1024)
        groupname = client.recv(1024).decode("utf-8")

        if groupname in groups:
            groups[groupname].connect(username, client)
            client.send(b"/ready")
        else:
            groups[groupname] = Group(username, client)
            client.send(b"/adminReady")

        threading.Thread(target=clientHandler, args=(client, username, groupname)).start()

if __name__ == "__main__":
    main()