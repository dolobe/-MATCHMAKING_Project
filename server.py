import socket
import threading
import time
from database import Database
from game import Game

HOST = '0.0.0.0'
PORT = 9000
db = Database()  # La connexion reste ouverte
print("Connexion réussie !")

queue_lock = threading.Lock()
waiting_clients = []

def matchmaking_loop():
    while True:
        time.sleep(2)
        with queue_lock:
            if len(waiting_clients) >= 2:
                player1 = waiting_clients.pop(0)
                player2 = waiting_clients.pop(0)

                match_id = db.create_match(player1, player2)
                print(f"[MATCH #{match_id}] {player1['pseudo']} VS {player2['pseudo']}")

                # Démarre le jeu dans un thread séparé
                threading.Thread(target=Game, args=(match_id, player1, player2, db), daemon=True).start()

def handle_client(client_sock, client_addr):
    try:
        pseudo = client_sock.recv(1024).decode().strip()
        print(f"[🎮] Nouveau client : {pseudo} ({client_addr})")

        client_data = {
            'socket': client_sock,
            'pseudo': pseudo,
            'ip': client_addr[0],
            'port': client_addr[1]
        }

        db.add_to_queue(client_data['ip'], client_data['port'], pseudo)

        with queue_lock:
            waiting_clients.append(client_data)

        client_sock.sendall(f"Bienvenue {pseudo}, en attente d'un autre joueur...".encode())

    except Exception as e:
        print(f"[!] Erreur avec le client {client_addr}: {e}")
        client_sock.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[⚙️ SERVEUR] En écoute sur {HOST}:{PORT}")

    # Démarre le thread de matchmaking
    threading.Thread(target=matchmaking_loop, daemon=True).start()

    while True:
        client_sock, client_addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
