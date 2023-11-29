from aiogram import Dispatcher, Bot, executor, types
from .beautiful import ColorStart

class TgBot:

    """
    Your Telegram Bot for sent messages, photo and video
    
    
    imported in library
    :import Dispatcher
    :import Bot
    :import executor
    :import types
    :import asyncio

    All modules, without types, used for work defines in library. 
    Module types don't used in library, but you can use it instead aiogram.types .

    """

    def __init__(self,
                token: str = None,
                admin_username: str = None):
        """
        For settings, your Telegram Bot.
        
        :param token: str, token your TG Bot, from BotFather, default None
        :param admin_username: str, username from telegram admin your bot
        """

        self.token = token
        self.bot = Bot(token)
        self.dispatcher = Dispatcher(self.bot)
        self.executor = executor
        self.admin_username = admin_username


    async def send_message(self,
                       chat_id: int,
                       message: str,
                       reply_markup = None
                       ) -> None:
        """
        For sent message from your bot.

        :param chat_id: chat ID user who used bot
        :param message: your message
        :param reply_markup: your markup for message, default None

        :return None
        """

        await self.bot.send_message(chat_id=chat_id,
                                    text=message,
                                    reply_markup=reply_markup)

    async def send_photo(self,
                         chat_id: int,
                         photo: str,
                         caption: str = None) -> None:
        """
        For sent photo from your bot.

        :param chat_id: chat id user who used bot
        :param photo: you're photoed
        :param caption: text under photo in this msg, default None

        :return None
        """

        await self.bot.send_photo(chat_id=chat_id,
                                  photo=photo,
                                  caption=caption)


    async def send_video(self,
                        chat_id: int,
                        video: str) -> None:

        """
        For send video.
        
        :param chat_id: int, chat ID user who used bot
        :param video: str, link for video

        :return None
        """
        

        await self.bot.send_video(chat_id=chat_id,
                                    video=open(f'{video}.mp4', 'rb'))


    async def on_startup(self, dispatcher: Dispatcher):
        
        """
        For beautiful start your bot

        :return None
        """

        await ColorStart(admin_username=self.admin_username).on_startup()



    async def on_shutdown(self, dispatcher: Dispatcher):

        """
        For beautiful shutdown your bot

        :return None
        """

        await ColorStart().on_shutdown()


    def start_polling(self,
                      dispatcher = None,
                      skip_updates = True,
                      on_startup = None,
                      on_shutdown = None) -> None:

        """
        For start your Telegram Bot.
        
        :param dp: Dispatcher, use 'bot.dispatcher', default None
        :param skip_updates: False or True, default True
        :param on_startup: your define for startup, use 'bot.on_startup' or your define, default None
        :param on_shutdown: your define for shutdown, use 'bot.on_shutdown' or your define, default None

        :return None
        """

        self.executor.start_polling(dispatcher=dispatcher,
                                    skip_updates=skip_updates,
                                    on_startup=on_startup,
                                    on_shutdown=on_shutdown)
