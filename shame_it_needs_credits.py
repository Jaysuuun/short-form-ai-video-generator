import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(

    api_key=os.environ.get("OPENAI_API_KEY"),

)

response = client.responses.create(

    model="gpt-5.5",
    instructions="You are a children story teller that writes stories 1-2 minutes long and an important lesson at the end",
    input="Write a random children's story"
)

print(response.output_text)