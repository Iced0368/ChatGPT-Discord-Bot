from typing import Dict
from gpt import GPTBot

class BotManager:
    def __init__(self):
        self.bot = {}
    
    def createBot(self, id):
        self.bot[id] = GPTBot()