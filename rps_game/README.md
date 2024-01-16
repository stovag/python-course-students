# Rock - Paper - Scissors game

**Custom Player class:**

```
rps_client_adaptive_player.py
```

**Some custom players classes:**

```
rps_client_custom_players.py
```

**Client app:**

```
rps_client_app.py
```

**From Command line:**

```
python -m rps_game.rps_client_app
python -m rps_game.rps_client_app -a euclid.ee.duth.gr -p 4455
python -m rps_game.rps_client_app -c RPSMyPlayer
```

**Server app:**

```
rps_server_app.py
```

**From Command line:**

```
python -m rps_game.rps_server_app
```

## MyAdaptivePlayer Class

MyAdaptivePlayer features several improvements upon the base MyPlayer Class.

- **Counter Moves Dictionary**:
  - The improved version introduces a ``counter_moves`` dictionary to keep track of counter moves for each possible move in the game (rock, paper, and scissors). This dictionary is used in the next_move method to make strategic moves based on the opponent's historical choices.
- **Logging and Bias Calculation**:
  - Logging has been introdced as well by extending the ``rps_client.py`` mofule. Now at the end of each round the moves and results of the round are recorded in a log file located in:
  
    ```
    rps_game\logs\result_log.csv
    ```

  - A new method, ``get_bot_bias``, is introduced to calculate the frequency of each move made by the bot in the recent game rounds. It reads logs specific to the current game instance, calculates move frequencies, and returns a bias (a Pandas Series) that represents the likelihood of each move being chosen.
- **Improved Move Selection**:
  - The ``next_move()`` method now incorporates a more sophisticated move selection strategy.
    - It first checks for biases in the bot's recent moves using the ``get_bot_bias()`` method. If a move bias is detected (one move occurring more than x_1 of the time), the player selects the counter move for that biased move.
    - If a move is underrepresented, having a very low frequency then it is safe to assume that a new bias has been established, and the player selects the counter of the second most frequent move, as this is most likely the new bias.
    - If no obvious bias is detected, the player makes a move based on the frequencies of its recent moves.
- **Pandas Usage**:
  - The improved version utilizes the Pandas library to read and analyze logs. It reads the last 25 rounds from the log file and calculates move frequencies.

These changes aim to make the player more adaptive by considering historical move data and adjusting its strategy accordingly. The introduction of the counter_moves dictionary and the get_bot_bias method enhances the player's decision-making process.

## Move Selection Process

In order to correctly 

- **Calculate Bias**:
  - The ``get_bot_bias`` method is called to obtain the bias or frequency of each move made by the bot in the last 25 rounds.

- **Check for Bias**:
  - If there is a bias (bias is not None), the biases are sorted in descending order.
  - If the maximum bias is greater than 50%, it indicates a clear bias towards a specific move.

- **Decision-Making based on Bias**:
  - If there is a clear bias, the method iterates over possible moves to find the move with the maximum bias.
  - It selects the counter move for the move with the highest bias.

- **Decision-Making without Bias**:
  - If there is no clear bias (maximum bias <= 50%), it chooses a move based on the frequencies of the moves.
  - It uses random.choices to select a move with probabilities based on the observed frequencies.
  - The selected move is then mapped to its counter move.

- **Random Move if No Bias Information**:
  - If no bias information is available (less than 50 rounds played), it selects a random move from the possible moves.
