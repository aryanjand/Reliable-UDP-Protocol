from SessionManagement.ServerConnectionToClient import ServerConnectionToClient

if __name__ == "__main__":
    print("TCP like Server Started!\n")
    server = ServerConnectionToClient()
    server.bind(("127.0.0.1", 8000))
    server.listen(5)
    server.accept()

    server.shutdown()
    server.close()
