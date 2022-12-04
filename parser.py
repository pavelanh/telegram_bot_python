import logging


class MessageParser:
    def __init__(self, message):
        self.message = message

    def get_json_entity(self, json_ent):
        try:
            if json_ent == 'chat_id':
                chat_id = self.message['message']['chat']['id']
                logging.info(f'chat_id -> {chat_id}')
                return chat_id
            elif json_ent == 'txt':
                txt = self.message['message']['text']
                logging.info(f'txt -> {txt}')
                return txt
            elif json_ent == 'first_name':
                first_name = self.message['message']['chat']['first_name']
                logging.info(f'first_name -> {first_name}')
                return first_name
        except:
            pass
