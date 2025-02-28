import socket
import threading
import pickle
import sys

# Initialize state with all required keys
state = {
    "inputCondition": threading.Condition(),
    "sendMessageLock": threading.Lock(),
    "username": "",
    "groupname": "",
    "alive": False,
    "joinDisconnect": False,
    "inputMessage": True,
    "userInput": ""
}

def serverListen(serverSocket):
    while state["alive"]:
        try:
            msg = serverSocket.recv(1024).decode("utf-8")
            if not msg:
                break  # Handle unexpected disconnection

            if msg == "/viewRequests":
                serverSocket.send(b".")
                response = serverSocket.recv(1024).decode("utf-8")
                if response == "/sendingData":
                    serverSocket.send(b"/readyForData")
                    data = pickle.loads(serverSocket.recv(1024))
                    print("Pending Requests:" if data else "No pending requests.")
                    for element in data:
                        print(element)
                else:
                    print(response)

            elif msg == "/approveRequest":
                serverSocket.send(b".")
                response = serverSocket.recv(1024).decode("utf-8")
                if response == "/proceed":
                    state["inputMessage"] = False
                    print("Enter username to approve: ")
                    with state["inputCondition"]:
                        state["inputCondition"].wait()
                    state["inputMessage"] = True
                    serverSocket.send(state["userInput"].encode("utf-8"))
                    print(serverSocket.recv(1024).decode("utf-8"))
                else:
                    print(response)

            elif msg == "/disconnect":
                serverSocket.send(b".")
                state["alive"] = False
                break

            elif msg == "/messageSend":
                serverSocket.send(state["userInput"].encode("utf-8"))
                state["sendMessageLock"].release()

            elif msg in ["/allMembers", "/onlineMembers"]:
                serverSocket.send(b".")
                data = pickle.loads(serverSocket.recv(1024))
                print(f"{'Online' if msg == '/onlineMembers' else 'All'} Group Members:")
                for element in data:
                    print(element)

            elif msg in ["/changeAdmin", "/kickMember"]:
                serverSocket.send(b".")
                response = serverSocket.recv(1024).decode("utf-8")
                if response == "/proceed":
                    state["inputMessage"] = False
                    action = "Enter new admin username" if msg == "/changeAdmin" else "Enter username to kick"
                    print(action + ": ")
                    with state["inputCondition"]:
                        state["inputCondition"].wait()
                    state["inputMessage"] = True
                    serverSocket.send(state["userInput"].encode("utf-8"))
                    print(serverSocket.recv(1024).decode("utf-8"))
                else:
                    print(response)

            elif msg == "/whoAdmin":
                serverSocket.send(state["groupname"].encode("utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))

            else:
                print(msg)

        except Exception as e:
            print("Error:", e)
            break

def userInput(serverSocket):
    while state["alive"]:
        state["sendMessageLock"].acquire()
        state["userInput"] = input()
        state["sendMessageLock"].release()
        with state["inputCondition"]:
            state["inputCondition"].notify()

        command_map = {
            "/1": "/viewRequests", "/2": "/approveRequest", "/3": "/disconnect",
            "/4": "/allMembers", "/5": "/onlineMembers", "/6": "/changeAdmin",
            "/7": "/whoAdmin", "/8": "/kickMember"
        }

        if state["userInput"] in command_map:
            serverSocket.send(command_map[state["userInput"]].encode("utf-8"))
        elif state["inputMessage"]:
            state["sendMessageLock"].acquire()
            serverSocket.send(b"/messageSend")

def main():
    if len(sys.argv) < 3:
        print("USAGE: python client.py <IP> <Port>")
        return

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((sys.argv[1], int(sys.argv[2])))
        state["username"] = input("Enter username: ")
        state["groupname"] = input("Enter group name: ")

        serverSocket.send(state["username"].encode("utf-8"))
        serverSocket.recv(1024)
        serverSocket.send(state["groupname"].encode("utf-8"))
        response = serverSocket.recv(1024).decode("utf-8")

        if response == "/adminReady":
            print(f"Group {state['groupname']} created. You are the admin.")
            state["alive"] = True
        elif response == "/ready":
            print(f"Joined group {state['groupname']}.")
            state["alive"] = True
        elif response == "/wait":
            print("Join request pending admin approval.")

        userThread = threading.Thread(target=userInput, args=(serverSocket,))
        listenThread = threading.Thread(target=serverListen, args=(serverSocket,))
        userThread.start()
        listenThread.start()

        userThread.join()
        listenThread.join()
        serverSocket.close()
        print("Disconnected from PyconChat.")

    except Exception as e:
        print("Connection error:", e)

if __name__ == "__main__":
    main()