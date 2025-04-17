from database import Database

db = Database()

db.add_to_queue('127.0.0.1', 12345, 'PlayerOne')
print("Queue:", db.get_queue())

db.close()
