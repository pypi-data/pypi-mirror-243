"""
A wrapper for openai.ChatCompletion
"""
import openai
from config.openai_config import OpenAIConfig, AzureOpenAIConfig
from abc import ABC, abstractmethod

class ChatGPT(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def respond(self):
        pass

    @abstractmethod
    def set_config(self):     
        pass

class OpenAIChatGPT(ChatGPT):

    def __init__(self, config: OpenAIConfig):
        self.config = config

    def respond(self, model, messages, **arguments):
        self.set_config()
        completion = openai.ChatCompletion.create(
                model = model, 
                messages = messages,
                **arguments
            )
        return completion['choices'][0]['message']['content']

    def set_config(self):     
        openai.api_key = self.config.api_key
        openai.api_base = "https://api.openai.com/v1"
        openai.api_version = ""
        openai.api_type = "open_ai"
    
class AzureOpenAIChatGPT(ChatGPT):

    def __init__(self, config: AzureOpenAIConfig):
        self.config = config

    def respond(self, engine, messages, **arguments):
        self.set_config()
        completion = openai.ChatCompletion.create(
                engine = engine, 
                messages = messages,
                **arguments
            )
        return completion['choices'][0]['message']['content']

    def set_config(self):     
        openai.api_key = self.config.api_key
        openai.api_base = self.config.api_base
        openai.api_version = self.config.api_version
        openai.api_type = "azure"
    