from config import Config
from telebot import logger, TeleBot, types
import logging
import os
import mc
import traceback

TEXT_FILE = 'text.txt'

bot_logger = logger
logger.setLevel(logging.DEBUG)

bot = TeleBot(Config.BOT_TOKEN, parse_mode=None)


class Generator:
    def __init__(self):
        if not os.path.exists(TEXT_FILE):
            raise TextFileIsNotExists
        with open(TEXT_FILE, encoding='utf8') as f:
            model = f.readlines()

        self._generator = mc.PhraseGenerator(samples=model)

    def generate(self):
        phrase = self._generator.generate_phrase(
            attempts=10,
            validators=[mc.builtin.validators.words_count(minimal=7, maximal=15)],
            formatters=[mc.builtin.formatters.usual_syntax]
        )
        return phrase


class TextFileIsNotExists(Exception):
    """file with text is not exists"""


commands = {
    'start': 'Get used to the bot',
    'generate': 'generate text'
}

generator = Generator()


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, {}!'.format(message.from_user.first_name))


@bot.inline_handler(lambda query: query.query is not None)
def generate_text_handler(inline_query):
    try:
        phrase = generate_sentence()
        r = types.InlineQueryResultArticle(
            '1',
            'default',
            types.InputTextMessageContent(phrase)
        )
        bot.answer_inline_query(inline_query.id, [r])
    except Exception:
        print(traceback.format_exc())


@bot.message_handler(commands=['help'])
def start(message):
    cid = message.chat.id
    help_text = 'The following commands are available: \n'
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


def generate_sentence():
    return generator.generate()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    response = 'I don\'t understand {text}. Maybe try the help page at /help'.format(
        text=message.text
    )
    bot.send_message(message.chat.id, text=response)
