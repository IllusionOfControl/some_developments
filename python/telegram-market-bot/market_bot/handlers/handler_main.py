from market_bot.handlers.handler_com import HandlerCommands
from market_bot.handlers.handler_all_text import HandlerAllText
from market_bot.handlers.handler_inline_query import HandlerInlineQuery


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        self.bot = bot
        self.handler_commands = HandlerCommands(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)
        self.handler_inline_query = HandlerInlineQuery(self.bot)

    def handle(self):
        self.handler_commands.handle()
        self.handler_all_text.handle()
        self.handler_inline_query.handle()