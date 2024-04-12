from SessionManagement.ServerConnectionToClient import ServerConnectionToClient

if __name__ == "__main__":
    # print("Line 4")
    server = ServerConnectionToClient()
    server.bind(("localhost", 8000))
    server.listen(5)
    server.accept()

    server.shutdown()
    server.close()
