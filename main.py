from mongo_api import MongoAPI
from sql_manager import SQLHandler
from bot_manager import Tele_Bot
from var_config import API_KEY
import time




class Main_Bot:
    def __init__(self):
        self.api_key = API_KEY
        self.dbs_name = ['zero', 'um', 'dois', 'tres']
        self.sql = SQLHandler()
        self.tele_bot = Tele_Bot()
        self.tele_bot.bot_init()


    def main_loop(self):
        
        while True:
            print('checking.....')
            for db in self.dbs_name:
                self.api = MongoAPI("all_data", db, self.api_key)
                
                recent_games = self.api.last_four_docs()
                # Verifica se a diferença de score dos jogos é menor que 1.5
                if recent_games:
                    if self.check_over(recent_games):
                        print('OVER FINDED')
                        self.signal_prep(recent_games, over=True) 

                    if self.check_3x2(recent_games[0]):
                        print('3X2 FINDED')                   
                        self.signal_prep(recent_games[0], over=False)             
                        
            time.sleep(30)



    def check_over(self, last_games:list):

        flag = 0
        for game in last_games:            
            score = game['score']
            try:
                home_score, away_score = map(int, score.split('-'))
            except:
                pass
            else:
                total_score = home_score + away_score
                if total_score <= 1.5:
                    flag += 1

        if flag == 4:
            if self.db_check_over(last_games):
                return True
        else:
            return False



    def check_3x2(self, game):

        score = game['score']
        try:
            home_score, away_score = map(int, score.split('-'))
        except:
            pass
        else:
            if home_score == 3 and away_score == 2 or home_score == 2 and away_score == 3:
                if self.db_check_3x2(game):
                    return True

    def signal_prep(self, last_games, over = False):
        if over:
            signal_data = {
                'mongo_ids' : ','.join(map(str,[x['_id'] for x in last_games])),
                'league' : last_games[0]['league'],
                'game_hour' : ','.join(map(str,[x['hour'] for x in last_games])),
                'timestamp' : last_games[0]['timestamp']
            }
            if self.tele_bot.send_message_over(signal_data):
                print('Mensagem para Telegram enviada!')
                self.sql.insert_data(msg_dict = signal_data, db_name = 'games_sended_over')

        else:
            signal_data = {
                'mongo_ids' : last_games['_id'],
                'league' : last_games['league'],
                'game_hour' : last_games['hour'],
                'timestamp' : last_games['timestamp']
            }
            if self.tele_bot.send_message_3x2(signal_data):
                print('Mensagem para Telegram enviada!')
                self.sql.insert_data(msg_dict = signal_data, db_name = 'games_sended_3x2') 


    def db_check_over(self, last_games):
        mongo_ids = ','.join(map(str,[x['_id'] for x in last_games]))
        if not self.sql.check_data_exists(mongo_id = mongo_ids, db_name='games_sended_over'):
            return True

    def db_check_3x2(self, game):
        mongo_id = str(game['_id'])
        ckecker = self.sql.check_data_exists(mongo_id = mongo_id, db_name='games_sended_3x2')
        if not ckecker:
            return True




if __name__ == '__main__':
    Main_Bot().main_loop()