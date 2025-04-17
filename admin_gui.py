from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from database import Database

class AdminGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Admin - Gestion de la Base de Données")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Titre
        title = QLabel("Gestion de la Base de Données", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: blue;")
        layout.addWidget(title)

        # Boutons CRUD
        button_layout = QHBoxLayout()
        self.queue_button = QPushButton("Gérer la File d'Attente", self)
        self.queue_button.clicked.connect(self.show_queue)
        button_layout.addWidget(self.queue_button)

        self.match_button = QPushButton("Gérer les Matchs", self)
        self.match_button.clicked.connect(self.show_matches)
        button_layout.addWidget(self.match_button)

        self.turn_button = QPushButton("Gérer les Tours", self)
        self.turn_button.clicked.connect(self.show_turns)
        button_layout.addWidget(self.turn_button)

        layout.addLayout(button_layout)

        # Tableau pour afficher les données
        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        # Formulaire pour les actions CRUD
        form_layout = QHBoxLayout()
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("ID")
        form_layout.addWidget(self.id_input)

        self.action_button = QPushButton("Supprimer", self)
        self.action_button.clicked.connect(self.delete_entry)
        form_layout.addWidget(self.action_button)

        layout.addLayout(form_layout)

        self.setLayout(layout)

    def show_queue(self):
        """Affiche la file d'attente."""
        self.table.clear()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "IP", "Port", "Pseudo"])
        queue = self.db.get_queue()
        self.table.setRowCount(len(queue))
        for row_idx, row_data in enumerate(queue):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data["id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data["ip"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data["port"])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data["pseudo"]))

    def show_matches(self):
        """Affiche les matchs."""
        self.table.clear()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Joueur 1 (IP)", "Joueur 1 (Port)", "Joueur 2 (IP)", "Joueur 2 (Port)", "État du Plateau", "Résultat"])
        self.db.cursor.execute("SELECT * FROM matchs")
        matches = self.db.cursor.fetchall()
        self.table.setRowCount(len(matches))
        for row_idx, row_data in enumerate(matches):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data["id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data["player1_ip"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data["player1_port"])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data["player2_ip"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row_data["player2_port"])))
            self.table.setItem(row_idx, 5, QTableWidgetItem(row_data["board_state"]))
            self.table.setItem(row_idx, 6, QTableWidgetItem(row_data["result"]))

    def show_turns(self):
        """Affiche les tours."""
        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID Match", "Joueur", "Position Jouée"])
        self.db.cursor.execute("SELECT * FROM turns")
        turns = self.db.cursor.fetchall()
        self.table.setRowCount(len(turns))
        for row_idx, row_data in enumerate(turns):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data["match_id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data["player"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data["move_position"])))

    def delete_entry(self):
        """Supprime une entrée de la base de données."""
        selected_id = self.id_input.text().strip()
        if not selected_id:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un ID valide.")
            return

        try:
            # Suppression dans la file d'attente
            self.db.remove_from_queue(selected_id)
            QMessageBox.information(self, "Succès", f"L'entrée avec l'ID {selected_id} a été supprimée.")
            self.show_queue()  # Rafraîchit la vue
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")

    def closeEvent(self, event):
        """Ferme la connexion à la base de données lors de la fermeture de l'application."""
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = AdminGUI()
    window.show()
    app.exec()