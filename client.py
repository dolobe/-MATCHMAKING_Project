import socket
import sys
from PyQt6.QtWidgets import QApplication
from gui import TicTacToeGUI

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9000

def main():
    app = QApplication(sys.argv)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionRefusedError:
        print("[❌] Impossible de se connecter au serveur. Assurez-vous qu'il est démarré.")
        sys.exit()

    pseudo = input("🎮 Entrez votre pseudo : ").strip()
    sock.sendall(pseudo.encode())

    print(f"[✅] Connecté au serveur en tant que {pseudo}. En attente d'un autre joueur...")

    # Lancer l'interface graphique
    window = TicTacToeGUI(sock, pseudo)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
