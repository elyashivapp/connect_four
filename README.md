# Connect Four

Connect Four is a classic two-player board game implemented in Python. This repository contains the source code and additional resources to play the game between two players on different machines.

## Game Description

Connect Four is a strategic game where two players take turns dropping colored discs into a vertical grid. The objective is to connect four discs of the same color in a row, either horizontally, vertically, or diagonally, before your opponent does.

## Features

- **Multiplayer gameplay**: The game allows two players to compete against each other on different machines.
- **Network communication**: Players can connect to each other over a network to establish a game session.
- **Loading screen**: While the first player waits for the second player, he gets a loading screen.
- **Win detection**: The game detects and announces the winner or a draw.
- **Replay option**: After a game ends, players can choose to play again without restarting the program.

## Prerequisites

To run the Connect Four game, you need to have the following installed:

- Python 3.x

## Getting Started

1. Clone this repository using the following command:

   ```shell
   git clone https://github.com/NpFHs/connect_four.git
  
2. Navigate to the project directory:

    ```shell
    cd connect_four

3. Run the game server on one machine:

     ```shell
     python connect_four_server.py
     
4. Note the IP address and port number displayed by the server.

5. On another machine, navigate to the project directory and run the game client:
       
      ```shell
      python connect_four_client.py
      

6. Enter the server IP address and port number when prompted by the client.

7. The game will start, and players on both machines can take turns playing.

## Customizing the Game

By default, the game is implemented to be played in a command-line interface. If you want to customize or enhance the game with a graphical user interface (GUI) or other features, you can modify the source code in the `connect_four_client.py` file. Look for the `ConnectFourClient` class and its corresponding methods to make changes.

## Contributing

Contributions to this project are welcome. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them, with clear descriptions.
4. Push your changes to your forked repository.
5. Submit a pull request, explaining the changes you have made.

## License

The Connect Four game is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute it according to the terms of the license.

## Credits

This game was created by [elyashivapp](https://github.com/elyashivapp) with help from [NpFHs](https://github.com/NpFHs).

## Contact

If you have any questions, suggestions, or feedback, please feel free to [open an issue](https://github.com/NpFHs/connect_four/issues) in the repository.

