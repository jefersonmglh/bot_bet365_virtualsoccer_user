import sqlite3

class SQLHandler:
    def __init__(self):
        self.conn_over = sqlite3.connect('games_sended_over.db')
        self.conn_3x2 = sqlite3.connect('games_sended_3x2.db')
        self.cursor_over = self.conn_over.cursor()
        self.cursor_3x2 = self.conn_3x2.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Create tables for first database
        self.cursor_over.execute('''CREATE TABLE IF NOT EXISTS games_sended_over (
                                    mongo_ids text,
                                    league text,
                                    game_hour text,
                                    timestamp_scrap text)''')
        self.conn_over.commit()
        
        # Create tables for second database
        self.cursor_3x2.execute('''CREATE TABLE IF NOT EXISTS games_sended_3x2 (
                                    mongo_ids text,
                                    league text,
                                    game_hour text,
                                    timestamp_scrap text)''')
        self.conn_3x2.commit()

    def check_data_exists(self, mongo_id, db_name):
        cursor = self.conn_over.cursor() if db_name == 'games_sended_over' else self.conn_3x2.cursor()
        cursor.execute(f"SELECT * FROM {db_name} WHERE mongo_ids=?", (mongo_id,))
        data = cursor.fetchall()
        return True if data else False

    def insert_data(self, msg_dict, db_name):
        cursor = self.conn_over.cursor() if db_name == 'games_sended_over' else self.conn_3x2.cursor()
        cursor.execute(f"INSERT INTO {db_name} VALUES (?,?,?,?)", (msg_dict.get('mongo_ids'), msg_dict.get('league'), msg_dict.get('game_hour'), msg_dict.get('timestamp')))
        self.conn_over.commit() if db_name == 'games_sended_over' else self.conn_3x2.commit()

    def view_all_docs(self, db_name):
        cursor = self.conn_over.cursor() if db_name == 'games_sended_over' else self.conn_3x2.cursor()
        cursor.execute(f"SELECT * FROM {db_name}")
        rows = cursor.fetchall()
        
        return rows

