import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def add_to_queue(self, ip, port, pseudo):
        self.cursor.execute(
            "INSERT INTO queue (ip, port, pseudo, entry_time) VALUES (%s, %s, %s, NOW())",
            (ip, port, pseudo)
        )
        self.conn.commit()

    def get_queue(self):
        self.cursor.execute("SELECT * FROM queue ORDER BY entry_time ASC")
        return self.cursor.fetchall()

    def remove_from_queue(self, id):
        self.cursor.execute("DELETE FROM queue WHERE id = %s", (id,))
        self.conn.commit()

    def create_match(self, player1, player2):
        self.cursor.execute("""
            INSERT INTO matchs (
                player1_ip, player1_port, player2_ip, player2_port,
                board_state, is_finished, result
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            player1['ip'], player1['port'],
            player2['ip'], player2['port'],
            " " * 9, False, "none"
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def save_turn(self, match_id, player, move_position):
        self.cursor.execute("""
            INSERT INTO turns (match_id, player, move_position)
            VALUES (%s, %s, %s)
        """, (match_id, player, move_position))
        self.conn.commit()

    def update_board_state(self, match_id, board_state):
        self.cursor.execute("""
            UPDATE matchs
            SET board_state = %s
            WHERE id = %s
        """, (board_state, match_id))
        self.conn.commit()

    def end_match(self, match_id, result):
        self.cursor.execute("""
            UPDATE matchs
            SET is_finished = %s, result = %s
            WHERE id = %s
        """, (True, result, match_id))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
