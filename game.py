class Game:
    def __init__(self, match_id, player1, player2, db):
        self.match_id = match_id
        self.player1 = player1
        self.player2 = player2
        self.db = db
        self.plateau = [" "] * 9
        self.joueur_actuel = "X"
        self.current_player = player1
        self.next_player = player2
        self.run_game()

    def verifier_victoire(self):
        combinaisons = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # lignes
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colonnes
            [0, 4, 8], [2, 4, 6]  # diagonales
        ]
        for comb in combinaisons:
            if self.plateau[comb[0]] == self.plateau[comb[1]] == self.plateau[comb[2]] != " ":
                return self.plateau[comb[0]]
        return None

    def verifier_egalite(self):
        return " " not in self.plateau

    def jouer_tour(self, coup):
        if 0 <= coup <= 8 and self.plateau[coup] == " ":
            self.plateau[coup] = self.joueur_actuel
            return True
        return False

    def run_game(self):
        while True:
            try:
                # Envoie l'état du plateau et demande un coup
                self.current_player['socket'].sendall(f"Plateau: {''.join(self.plateau)}\nVotre tour ({self.joueur_actuel}). Choisissez une case (1-9): ".encode())
                coup = int(self.current_player['socket'].recv(1024).decode()) - 1

                if not self.jouer_tour(coup):
                    self.current_player['socket'].sendall("Case invalide, essayez encore.".encode())
                    continue

                # Sauvegarde le coup dans la base de données
                self.db.save_turn(self.match_id, self.joueur_actuel, coup)
                self.db.update_board_state(self.match_id, "".join(self.plateau))

                # Vérifie la victoire
                winner = self.verifier_victoire()
                if winner:
                    self.current_player['socket'].sendall(f"Vous avez gagné ! ({self.joueur_actuel})".encode())
                    self.next_player['socket'].sendall(f"Vous avez perdu ! ({self.joueur_actuel})".encode())
                    self.db.end_match(self.match_id, winner)
                    break

                # Vérifie l'égalité
                if self.verifier_egalite():
                    self.current_player['socket'].sendall("Match nul !".encode())
                    self.next_player['socket'].sendall("Match nul !".encode())
                    self.db.end_match(self.match_id, "draw")
                    break

                # Change de joueur
                self.joueur_actuel = "O" if self.joueur_actuel == "X" else "X"
                self.current_player, self.next_player = self.next_player, self.current_player

            except Exception as e:
                print(f"[!] Erreur dans le match {self.match_id}: {e}")
                break

        # Ferme les connexions
        self.player1['socket'].close()
        self.player2['socket'].close()


class TicTacToeClient:
    def __init__(self, sock, pseudo):
        self.sock = sock
        self.pseudo = pseudo
        self.board = [" "] * 9
        self.current_player = "X"

    def start_game(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                if not msg:
                    print("[❌] Déconnecté du serveur.")
                    break
                print(msg)
            except Exception as e:
                print(f"[!] Erreur : {e}")
                break