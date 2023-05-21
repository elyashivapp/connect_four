import socket

PORT = 8789

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen()
print("Listening...")

player_1_socket, player_1_address = server_socket.accept()
print("Player 1 connected!")

player_2_socket, player_2_address = server_socket.accept()
print("Player 2 connected!")

while True:
    player_1_move = player_1_socket.recv(1024)
    player_2_socket.send(player_1_move)

    player_2_move = player_2_socket.recv(1024)
    player_1_socket.send(player_2_move)
