from openai import OpenAI

client = OpenAI()

def process_document(content):
    response = client.completions.create(engine="text-davinci-003",
    prompt="Process the following document: " + content,
    max_tokens=1500)
    return response.choices[0].text
