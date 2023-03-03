from typing import Dict
from gpt import GPTBot

class BotManager:
    def __init__(self):
        self.bot = {}
    
    def createBot(self, id):
        self.bot[id] = GPTBot()
        print(f"Registered in {id}")
        return self.bot[id]
    
    def removeBot(self, id):
        del self.bot.get(id)

    def registered(self, id):
        return id in self.bot.keys()
    
    def get(self, id):
        Bot = self.bot.get(id)
        if Bot is None:
            return self.createBot(id)
        else:
            return Bot