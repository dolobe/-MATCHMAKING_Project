from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class TicTacToeGUI(QWidget):
    def __init__(self, sock, pseudo):
        super().__init__()
        self.sock = sock
        self.pseudo = pseudo
        self.board = [" "] * 9
        self.current_player = "X"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Morpion - Joueur : {self.pseudo}")
        self.setGeometry(100, 100, 400, 450)

        self.layout = QVBoxLayout()

        # Titre
        self.title = QLabel("Morpion - En attente d'un autre joueur...", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 18px; color: blue;")
        self.layout.addWidget(self.title)

        # Plateau de jeu
        self.grid_layout = QGridLayout()
        self.board_buttons = []
        for i in range(9):
            button = QPushButton(" ", self)
            button.setFixedSize(100, 100)
            button.setFont(QFont("Arial", 24))
            button.setStyleSheet("background-color: lightgray;")
            button.clicked.connect(self.make_move(i))
            self.board_buttons.append(button)
            self.grid_layout.addWidget(button, i // 3, i % 3)

        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)

    def make_move(self, idx):
        def move():
            if self.board[idx] == " " and self.current_player == "X":
                self.board[idx] = "X"
                self.board_buttons[idx].setText("X")
                self.board_buttons[idx].setStyleSheet("color: green; font-weight: bold;")
                self.sock.sendall(str(idx + 1).encode())  # Envoie le coup au serveur
                self.current_player = "O"
                self.title.setText("En attente du coup de l'adversaire...")
        return move

    def update_board(self, move, player):
        self.board[move] = player
        self.board_buttons[move].setText(player)
        self.board_buttons[move].setStyleSheet("color: red; font-weight: bold;" if player == "O" else "color: green; font-weight: bold;")

    def display_winner(self, winner):
        if winner == "X":
            self.title.setText("Vous avez gagné ! 🎉")
            self.title.setStyleSheet("color: green; font-size: 20px;")
        elif winner == "O":
            self.title.setText("Vous avez perdu... 😢")
            self.title.setStyleSheet("color: red; font-size: 20px;")
        else:
            self.title.setText("Match nul ! 🤝")
            self.title.setStyleSheet("color: orange; font-size: 20px;")

    def listen_server(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                if not msg:
                    print("[❌] Déconnecté du serveur.")
                    break
                if msg.startswith("Plateau:"):
                    # Mise à jour du plateau
                    board_state = msg.split(":")[1].strip()
                    self.update_board_state(board_state)
                elif msg.startswith("Vous avez gagné"):
                    self.display_winner("X")
                    break
                elif msg.startswith("Vous avez perdu"):
                    self.display_winner("O")
                    break
                elif msg.startswith("Match nul"):
                    self.display_winner("draw")
                    break
            except Exception as e:
                print(f"[!] Erreur : {e}")
                break

    def update_board_state(self, board_state):
        for i, cell in enumerate(board_state):
            if cell != " ":
                self.update_board(i, cell)

    def start_game(self):
        self.title.setText("Votre tour !")
        self.title.setStyleSheet("color: blue; font-size: 18px;")
        self.listen_server()