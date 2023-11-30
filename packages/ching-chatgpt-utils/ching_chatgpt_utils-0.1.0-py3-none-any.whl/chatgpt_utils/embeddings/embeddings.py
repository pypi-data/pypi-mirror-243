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


def get_openai_embeddings(texts, model_name, token):
    HEADERS = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    URL = "https://api.openai.com/v1/embeddings"
    response = requests.post(URL, headers=HEADERS, json={"input": texts, "model":model_name, "encoding_format": "float"}).json()
    if len(response['data']) == 1:
        return response['data'][0]['embedding']
    return list(map(lambda element:element['embedding'], response['data']))