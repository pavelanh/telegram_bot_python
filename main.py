import logging

import requests as requests
from flask import Flask, request, Response
from jproperties import Properties

import driver
import logger

app = Flask(__name__)


def get_property(prop):
    configs = Properties()
    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)
        return configs.get(prop).data


TOKEN = get_property('TOKEN')


def setup_webhook():
    """
    This function setting up webhook for telegram bot through ngrok
    Selenium Chrome webdriver uses in headless mode
    """
    driver.open_page('http://127.0.0.1:4040/inspect/http')
    try:
        driver.click_elem('//button[text()="Clear Requests"]')
    finally:
        tunnel_url = driver.get_text_from_element('//*[@class="tunnels"]//li')

    driver.open_new_tab()
    driver.open_page(f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={tunnel_url}')

    if driver.get_text_from_element('//pre').__contains__('ok":true,"result":true'):
        logging.info('webhook is set up')
    driver.tear_down()


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    return requests.post(url, json=payload)


def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': 'https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg',
        'caption': 'This is a sample image'
    }
    return requests.post(url, json=payload)


def tel_send_audio(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAudio'
    payload = {
        'chat_id': chat_id,
        'audio': 'http://www.largesound.com/ashborytour/sound/brobob.mp3',
    }
    return requests.post(url, json=payload)


def tel_send_video(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
    payload = {
        'chat_id': chat_id,
        'video': 'https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4',
    }
    return requests.post(url, json=payload)


def tel_send_file(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    payload = {
        'chat_id': chat_id,
        'document': 'http://www.africau.edu/images/default/sample.pdf'
    }
    return requests.post(url, json=payload)


def tel_send_poll(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPoll'
    from flask import json
    payload = {
        'chat_id': chat_id,
        'question': 'In which direction does the sun rise?',
        'options': json.dumps(['North', 'South', 'East', 'West']),
        'is_anonymous': False,
        'type': 'quiz',
        'correct_option_id': 2
    }
    return requests.post(url, json=payload)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        from parser import MessageParser
        msg = request.get_json()
        parsed_message = MessageParser(msg)
        logging.info(f'message -> {parsed_message.message}')
        txt = parsed_message.get_json_entity('txt')
        chat_id = parsed_message.get_json_entity('chat_id')
        user_name = parsed_message.get_json_entity('first_name')

        if txt == 'hi':
            logging.info(f'user_name -> {user_name}')
            tel_send_message(chat_id, f'Hello {user_name}!!')
        elif txt == 'image':
            tel_send_image(chat_id)
        elif txt == 'audio':
            tel_send_audio(chat_id)
        elif txt == 'video':
            tel_send_video(chat_id)
        elif txt == 'file':
            tel_send_file(chat_id)
        elif txt == 'poll':
            tel_send_poll(chat_id)
        else:
            tel_send_message(chat_id, 'from webhook')

        return Response('ok', status=200)
    else:
        return '<h1>Welcome!</h1>'


if __name__ == '__main__':
    logger.setup_logging()
    setup_webhook()
    app.run(debug=True, use_reloader=True)
