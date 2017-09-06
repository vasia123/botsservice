import json
from datetime import datetime

from steampy.client import SteamClient
from steampy.guard import generate_one_time_code
from steampy.exceptions import InvalidCredentials


class Bot(object):
    __authenticator_files_path = 'files/'

    def __init__(self, steam_id, bot_type='trader'):
        self.bot_type = bot_type
        with open(self.__authenticator_files_path+steam_id+'.json') as f:
            self.config = json.load(f)

        self.auth_path = self.__authenticator_files_path+'guards/'+steam_id+'.json'
        with open(self.auth_path, 'w') as f:
            json.dump({
                "steamid": steam_id,
                "shared_secret": self.config['shared_secret'],
                "identity_secret": self.config['identity_secret'],
            }, f)
        self.client = SteamClient(self.config['apikey'])
        self.online = False

    def __str__(self):
        tmp = self.config
        tmp.pop('shared_secret')
        tmp.pop('secret_1')
        tmp.pop('apikey')
        tmp['online'] = self.online
        tmp['type'] = self.bot_type
        return json.dumps(tmp)

    def login(self):
        while True:
            try:
                self.client.login(self.config['account_name'], self.config['password'], self.auth_path)
                break
            except InvalidCredentials:
                print('Error with logging in')

    def get_code(self):
        return generate_one_time_code(self.config['shared_secret'], int(datetime.now().timestamp()))

    def make_offer(self, partner_id, item_ids):
        pass


class SteamBots(object):
    __bots_list_path = 'bots_list'

    def __init__(self):
        with open(self.__bots_list_path) as f:
            bots_list = [line.strip() for line in f]

        self.bots = [Bot(bot_id) for bot_id in bots_list]

    def __str__(self):
        return json.dumps([str(b) for b in self.bots])
