class TicTacToeLogic:
    def __init__(self):
        # List: The game board, 9 empty spaces
        self.board = [" " for _ in range(9)]
        
        # Dictionary: Map players to roles
        self.players = {"X": "Player 1", "O": "Player 2"}
        
        # Set: Winning combinations using tuples pattern
        self.winning_combinations = {
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        }
        
        # Tuple: Used inside the set above to define immutable paths
        
        self.current_turn = "X"
        self.game_over = False
        self.winner = None

    def make_move(self, index):
        # Check if game is active and move is valid
        if self.game_over or not (0 <= index < 9) or self.board[index] != " ":
            return False
            
        # Update board using list
        self.board[index] = self.current_turn
        
        # Check winner
        self.check_winner()
        
        # Next turn
        if not self.game_over:
            self.current_turn = "O" if self.current_turn == "X" else "X"
            
        return True

    def check_winner(self):
        # Iterate over set of tuples
        for combo in self.winning_combinations:
            a, b, c = combo # tuple unpacking
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                self.game_over = True
                self.winner = self.board[a]
                return
        
        # Check for draw
        if " " not in self.board:
            self.game_over = True
            self.winner = "Draw"

    def reset(self):
        self.board = [" " for _ in range(9)]
        self.current_turn = "X"
        self.game_over = False
        self.winner = None

    def get_state(self):
        return {
            "board": self.board,
            "current_turn": self.current_turn,
            "game_over": self.game_over,
            "winner": self.winner,
            "players": self.players
        }
