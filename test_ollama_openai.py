from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1/",
    # required but ignored
    api_key="ollama",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="llama3.2:1b",
)
print(chat_completion)
completion = client.completions.create(
    model="llama3.2:1b",
    prompt="Say this is a test",
)
print(completion)
