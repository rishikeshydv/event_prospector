import re

def event_search_prompter(text:str)->str:
    if len(text) == 0:
        return ""
    event_search_prompt = f"""
    You are an event search assistant. You will be provided with a brief description of the company.
    Your task is to find upcoming virtual events or physical events in 1-2 weeks max that are relevant to the company's services and customers.
    Please return a list of JSON objects, each containing the following fields:
    - event_name: The name of the event.
    - event_date: The date of the event in YYYY-MM-DD format.
    - event_type: The type of the event (e.g., webinar, conference, workshop, etc.).
    - event_location: The location of the event.
    - event_description: A brief description of the event.
    - event_url: A URL where more information about the event can be found.
    - event_registration_url: A URL where users can register for the event.
    - event_relevance: A brief explanation of why this event is relevant to the company based on the provided description.
    Here is the company description:
    {text}
    Please do not include any description or explanation in your response, only return the list of JSON objects as specified above.
    """
    return event_search_prompt.strip()

def company_brief_normalize(text:str)->str:
    if len(text) == 0:
        return ""
    normalized_text = []
    for line in text.splitlines():
        line = line.lower()
        line = re.sub(r'[^\w\s]', '', line)
        line = re.sub(r'\s+', ' ', line).strip()
        normalized_text.append(line)
    return "\n".join(normalized_text)
