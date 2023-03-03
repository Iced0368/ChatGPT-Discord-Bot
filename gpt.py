from dlist import DoublyLinkedList
import os, re, time
import openai
from util import *
from datetime import datetime
from pytz import timezone

CHATGPT_KEY = os.environ['CHATGPT_KEY']
BOTNICK = '지피티'

class GPTBot:
    def __init__(self):
        self.MEMORY = int(os.environ['MEMORY'])
        self.CHARACTER = '챗봇'
        self.RELATIONSHIP = '주인'
        self.chat_log = DoublyLinkedList()
        self.boot_time = datetime.now()

    def get_log(self):
        return self.chat_log

    def clear_log(self):
        self.chat_log = DoublyLinkedList()

    def set_character(self, c, r):
        self.CHARACTER, self.RELATIONSHIP = c, r

    def chatGPT(self, prompt, API_KEY, transfer=True):
        # set api key
        openai.api_key = API_KEY   

        origin_lang = translator.detect(prompt).lang
        if transfer:
            prompt = translate_text(prompt, 'en')
        # Call the chat GPT API
        completion = openai.Completion.create(
                engine = 'text-davinci-003'     # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
                , prompt = prompt
                , temperature = 0.5
                , max_tokens = 2048
                , top_p = 1
                , frequency_penalty = 0
                , presence_penalty = 0)
        chat = completion['choices'][0]['text'].split('\n', 1)[-1].strip()
        print(chat)

        if transfer:
            chat = translate_text(chat, origin_lang)
        return chat


    def log_integrate(self):
        memory = ''
        for username, text in self.chat_log.traverse_forward():
            if username != BOTNICK:
                memory += f'{username}: {text}\n\n'
            else:
                memory += f'{text}\n\n'
        return memory


    def prompt_format(self, username):
        return f'너는 "{BOTNICK}"라는 이름을 가진 {self.CHARACTER}이다. 다음은 너와 다른 {self.RELATIONSHIP}들의 채팅내역이다.\n{username}의 채팅에 {self.CHARACTER}를 연기해서 인사는 생략하고 대답해라. 만약 대답에 프로그래밍 코드가 포함되어 있다면, 코드를 언어 이름을 포함한 마크다운 코드블럭 문법으로 감싸라.\n{self.log_integrate()}'


    def ask(self, text, username):
        print("Get command")
        self.chat_log.put_back([username, text])

        s_time = time.time()
        while self.chat_log.size > self.MEMORY:
            self.chat_log.remove_front()
        while True:
            try:
                prompt = self.prompt_format(username)
                answer = self.chatGPT(prompt, CHATGPT_KEY)
                break
            except openai.error.InvalidRequestError: #Over Max tokens
                self. chat_log.remove_front()
                print("Memory popped")
        print(f"Time: {time.time()-s_time}")

        answer = answer_strip(answer)

        self.chat_log.put_back([BOTNICK, answer])
        return answer
    
