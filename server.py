import socket
import rsa

PORT = 8789


def encrypt(msg, pub_key):
    return rsa.encrypt(msg, pub_key)


def decrypt(msg, priv_key):
    return rsa.decrypt(msg, priv_key)


def main():
    pub_key, priv_key = rsa.newkeys(512)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen()
    print("Listening...")

    player_1_socket, player_1_address = server_socket.accept()
    player_1_socket.send("1".encode())
    player_1_socket.send(pub_key.save_pkcs1(format="DER"))
    print("Player 1 connected!")

    player_2_socket, player_2_address = server_socket.accept()
    player_2_socket.send("2".encode())
    player_2_socket.send(pub_key.save_pkcs1(format="DER"))
    print("Player 2 connected!")

    player_1_socket.send("2".encode())  # to signal the first player he can start the game

    while True:
        player_1_enc_move = player_1_socket.recv(1024)
        print(player_1_enc_move)
        player_1_move = decrypt(player_1_enc_move, priv_key)
        player_2_socket.send(player_1_move)

        player_2_enc_move = player_2_socket.recv(1024)
        print(player_2_enc_move)
        player_2_move = decrypt(player_2_enc_move, priv_key)

        # if the first player wins, the loop get stuck here, so this is the solution
        if player_2_move.decode() == "done":
            continue

        player_1_socket.send(player_2_move)


if __name__ == "__main__":
    main()
