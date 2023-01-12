import configparser

config = configparser.ConfigParser()
config.read_file(open(r'config.txt'))

TOKEN = config.get('bot_config', 'TOKEN')
CHAT_ID = int(config.get('bot_config', 'CHAT_ID'))

API_KEY = config.get('mongo_api_key', 'API_KEY')
