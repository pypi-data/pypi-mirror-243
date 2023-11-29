from colorama import Fore
from sys import platform
from os import system

class ColorStart:

    """
    You can use beautifull start and shutdown message for your Telegram Bot
    """

    def __init__(self, 
                 dispatcher = None,
                 admin_username: str = None
                 ) -> None:
        
        self.dispatcher = dispatcher
        self.admin_username = admin_username


    
    async def on_startup(self):

        """
        Immutable function
        """

        if platform.startswith("win"):
            system("cls")
        else:
            system("clear")


        if self.admin_username == None:
            print(Fore.GREEN + f"~~~~~~ BOT WAS STARTED @{(await self.dispatcher.bot.get_me()).username} ~~~~~~")
        else:
            print(Fore.GREEN + f"~~~~~~ BOT WAS STARTED @{(await self.dispatcher.bot.get_me()).username} ~~~~~~")
            print(Fore.LIGHTGREEN_EX + f"~~~~~~ Bot developer @{self.admin_username} ~~~~~~" + Fore.RESET)



    async def on_shutdown(self):

        """
        Immutable function
        """

        if platform.startswith("win"):
            system("cls")
        else:
            system("clear")
        
        print(Fore.RED + f"~~~~~~ Bot was stopped! ~~~~~~\n" + Fore.RESET)

    


class YourMessages:

    def get_color(self, col: str):
            if col.upper()=='RED':
                return Fore.RED
            
            if col.upper()=='GREEN':
                return Fore.GREEN
        
            if col.upper()=='BLUE':
                return Fore.BLUE

            if col.upper()=="YELLOW":
                return Fore.YELLOW

            else:
                return Fore.RESET


    def message(self, *,
                   clear: bool = True,
                   text: str = None,
                   color: list = [None, None]
                   ) -> None:
    
        
        """
        You can make beautiful your message to console!

        :param clear: bool, if you want to clear the console, leave it unchanged, default True
        :param text: str, your text for startup message
        :param color: list, color for your text; colors that can be used: red, green, blue, yellow or empty string; default [None, None]

        :return Message to console
        """

        if clear == True:
            if platform.startswith("win"):
                system("cls")
            else:
                system("clear")
            
            print(self.get_color(color[0]) + f'{text}' + self.get_color(color[1]))
            
        else:
            print(self.get_color(color[0]) + f'{text}' + self.get_color(color[1]))