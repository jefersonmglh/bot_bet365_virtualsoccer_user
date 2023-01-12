import telebot
from var_config import TOKEN, CHAT_ID

class Tele_Bot:

    def __init__(self,TOKEN=TOKEN, CHAT_ID=CHAT_ID):

        
        self.CHAT_ID = CHAT_ID
        self.TOKEN = TOKEN


    def bot_init(self):
        self.bot = telebot.TeleBot(self.TOKEN)
        # self.bot.config['api_key'] = self.TOKEN
        init_confirmation = self.bot.send_message(self.CHAT_ID, "\U0001F916 Bot iniciado com sucesso \U0001F916\n\U0000231B Checando jogos de futebol virtual \U000026BD")

        if not init_confirmation:
            raise ValueError('TeleBot credentials ERROR')
        

    def send_message_over(self, msg_dict):
        self.msg = f'''
\U0001F6A9 ALERTA OVER 1.5 \U0001F6A9

\U0001F440 4 PARTIDAS ABAIXO DE 1.5 GOLS/PARTIDA \U0001F440

\U0001F4DC
Liga: {msg_dict.get('league')}
Código da última partida: {msg_dict.get('game_hour')}
\U0001F51A
        '''

        if self.bot.send_message(self.CHAT_ID, self.msg):
            return True


    def send_message_3x2(self, msg_dict):
        self.msg = f'''
\U0001F6A9 ALERTA 3X2 \U0001F6A9

\U000026BD PARTIDA COM PLACAR 3X2 ENCONTRADA \U000026BD


\U0001F4DC
Liga: {msg_dict.get('league')}
Código da última partida: {msg_dict.get('game_hour').split('-')[0]}
\U0001F51A
        '''
        

    
        if self.bot.send_message(self.CHAT_ID, self.msg):
            return True

