import requests
from abc import ABC, abstractmethod
from config.huggingface_config import HuggingFaceConfig
from config.openai_config import OpenAIConfig
from typing import Union, List

class Embedder(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def embed(self):
        pass

class HuggingFaceAPIEmbedder(Embedder):
    def __init__(self, config: HuggingFaceConfig):
        assert isinstance(config, HuggingFaceConfig)
        self.config = config

    def embed(self, model: str, texts: Union[List, str]):
        HF_EMBEDDING_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}"
        HEADERS = {"Authorization": f"Bearer {self.config.api_key}"}
        response = requests.post(HF_EMBEDDING_API_URL, headers=HEADERS, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()

class OpenAIAPIEmbedder(Embedder):
    def __init__(self, config: OpenAIConfig):
        assert isinstance(config, OpenAIConfig)
        self.config = config

    def embed(self, model: str, texts: Union[List, str]):
        HEADERS = {"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"}
        URL = "https://api.openai.com/v1/embeddings"
        response = requests.post(URL, headers=HEADERS, json={"input": texts, "model":model, "encoding_format": "float"}).json()
        embeddings = list(map(lambda element:element['embedding'], response['data']))
        if isinstance(texts, str):
            return embeddings[0]
        return embeddings
        