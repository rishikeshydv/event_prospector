from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv
import json
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_MODEL="gpt-4.1"
client = OpenAI(api_key=OPENAI_API_KEY)

async def web_search_results(query:str)->List[dict]:
    if query == "":
        return []
    res_str = await client.responses.create(
        model=OPENAI_MODEL,
        tools=[{"type": "web_search"}],
        input=[{"role": "user", "content": query}]
    )
    #TODO: check res_str enums + any extra texts to be implemented later
    res_json = json.loads(res_str.output_text) 
    return res_json
    

