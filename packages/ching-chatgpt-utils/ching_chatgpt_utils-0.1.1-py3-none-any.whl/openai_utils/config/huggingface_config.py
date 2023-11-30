from pydantic import BaseModel

class HuggingFaceConfig(BaseModel):
    api_key: str
