"""
These classes validate the input configurations to initialise a ChatGPT instance
"""
from pydantic import BaseModel

class OpenAIConfig(BaseModel):
    api_key: str
    # api_base: Optional[str] = "https://api.openai.com/v1"
    # api_type: Optional[str] = "open_ai"
    # api_version: Optional[str] = ""

class AzureOpenAIConfig(BaseModel):
    api_key: str
    api_base: str
    api_version: str
    # api_type: Optional[str] = "azure"
