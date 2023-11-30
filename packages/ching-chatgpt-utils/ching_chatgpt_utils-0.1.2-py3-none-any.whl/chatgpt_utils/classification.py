import openai
from .parse import extract_json_from_string


"""
Given a query, classify using ChatGPT.

INPUT:
intructions - using few shot prompting as ChatGPT to output classification in JSON. Give ChatGPT an 'out' too.
query - user's query
categories - list of classes 
out_value - category to output if classification fails
key - the key that maps to the category {'key':'category'}

OUTPUT:
category - [category1|category2|out_value]
"""
def classify_query_chatgpt(instructions: str, query: str, categories: list, out_value: str = "undefined", key:str = "category"):
    # type validation
    assert isinstance(instructions, str) and isinstance(query, str) and isinstance(categories, list) and isinstance(out_value, str) and isinstance(key, str)
    
    # ask chatgpt to classify
    completion = openai.ChatCompletion.create(
                    model="gpt-4",    # gpt-4|gpt-3.5-turbo
                    messages = [{"role":"system", "content":instructions}, {"role":"user", "content":query}],
                    top_p = 0.2,
                    temperature = 0
                )
    response = completion['choices'][0]['message']['content']

    # parse response
    json_response = extract_json_from_string(response)

    # output validation
    category = json_response.get(key)
    if category is None or category not in categories+[out_value]:
        category = out_value
    return category


def classify_query_chatgpt_azure(instructions: str, query: str, categories: list, engine, out_value: str = "undefined", key:str = "category"):
    # type validation
    assert isinstance(instructions, str) and isinstance(query, str) and isinstance(categories, list) and isinstance(out_value, str) and isinstance(key, str)
    
    # ask chatgpt to classify
    completion = openai.ChatCompletion.create(
                    engine=engine,    # gpt-4|gpt-3.5-turbo
                    messages = [{"role":"system", "content":instructions}, {"role":"user", "content":query}],
                    top_p = 0.2,
                    temperature = 0
                )
    response = completion['choices'][0]['message']['content']

    # parse response
    json_response = extract_json_from_string(response)

    # output validation
    category = json_response.get(key)
    if category is None or category not in categories+[out_value]:
        category = out_value
    return category


"""
Perform the categorization of user's query. The labels are [country|division|overall|undefined]. Here are some examples with the required output format:
What is the best performing country this year? // {'category':'country'}
Give me the best performing product this year // {'category':'division'}
How did we perform this year? // {'category':'overall'}
Why is the sky blue? //  {'category':'undefined'}
How did sales compare to budget? // {'category':'overall'}
How were the margins in Pakistan? // {'category':'country'}
Tell me about the stock market outlook //  {'category':'undefined'}
Tell me the sales from air condition last year. // {'category':'division'}
"""