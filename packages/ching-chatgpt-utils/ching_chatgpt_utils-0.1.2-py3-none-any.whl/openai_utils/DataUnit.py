"""
DataUnit is a piece of grounding information for LLM in a Retrieval Augmented Generation
"""
from docarray import BaseDoc
from docarray.typing import NdArray
from typing import Optional
from docarray.typing import ID

class DataUnit(BaseDoc):
    id: ID
    llm_view: str                    # what the LLM sees
    embedding_text: Optional[str] = None   # for generating embedding
    embedding: Optional[NdArray]  = None # NdArray   # for semantic retrieval  
    tags: Optional[dict] = None      # for filtering
    