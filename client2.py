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

    # Attendre le rôle du serveur
    role = None
    while True:
        role_msg = sock.recv(1024).decode()
        print(f"[DEBUG] Message reçu du serveur : {role_msg}")
        if role_msg.startswith("ROLE:"):
            role = role_msg.split(":")[1]
            print(f"[✅] Vous jouez en tant que : {role}")
            break
        else:
            print(role_msg)  # Affiche les autres messages (comme le message de bienvenue)

    # Lancer l'interface graphique
    window = TicTacToeGUI(sock, pseudo, role)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
