import requests

"""
Generate embeddings from any huggingface embedding model
"""
def get_hf_embeddings(texts, model_name: str, token: str):
    assert isinstance(texts, list) or isinstance(texts, str)
    assert isinstance(model_name, str) and isinstance(token, str)
    HF_EMBEDDING_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
    HEADERS = {"Authorization": f"Bearer {token}"}
    response = requests.post(HF_EMBEDDING_API_URL, headers=HEADERS, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()