import socket
import sys

import rsa

PORT = 8789
public_key, private_key = rsa.newkeys(512)


def encrypt(msg, pub_key):
    return rsa.encrypt(msg, pub_key)


def decrypt(msg, priv_key):
    return rsa.decrypt(msg, priv_key)


def main():

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", PORT))
        server_socket.listen()
        print("Listening...")

        # send the first player the server public key
        player_1_socket, player_1_address = server_socket.accept()
        player_1_socket.send(public_key.save_pkcs1(format="DER"))

        # get the player public key
        msg = player_1_socket.recv(1024)
        player1_pub_key = rsa.key.PublicKey.load_pkcs1(msg, format="DER")

        # assigning the first player
        player_1_socket.send(encrypt("1".encode(), player1_pub_key))
        print("Player 1 connected!")

        # send the second player the server public key
        player_2_socket, player_2_address = server_socket.accept()
        player_2_socket.send(public_key.save_pkcs1(format="DER"))

        # get the player public key
        msg = player_2_socket.recv(1024)
        player2_pub_key = rsa.key.PublicKey.load_pkcs1(msg, format="DER")

        player_2_socket.send(encrypt("2".encode(), player2_pub_key))
        print("Player 2 connected!")

        player_1_socket.send(encrypt("2".encode(), player1_pub_key))  # to signal the first player he can start the game

        while True:
            # player one turn goes through the server
            player_1_enc_move = player_1_socket.recv(1024)
            print(player_1_enc_move)
            player_1_move = decrypt(player_1_enc_move, private_key)
            player_2_socket.send(encrypt(player_1_move, player2_pub_key))

            # player two turn goes through the server
            player_2_enc_move = player_2_socket.recv(1024)
            print(player_2_enc_move)
            player_2_move = decrypt(player_2_enc_move, private_key)
            print(player_2_move)

            # if the first player wins, the loop get stuck here, so this is the solution
            if player_2_move.decode() == "done":
                continue

            player_1_socket.send(encrypt(player_2_move, player1_pub_key))

    except ConnectionResetError:
        print("something went wrong")
        sys.exit()


if __name__ == "__main__":
    main()
