from openai import OpenAI
openai_api_key = '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'

client = OpenAI(
    api_key=openai_api_key
    )

def summarize_text(text):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes news articles in a way that a 10th grader can understand. At the end of each summary, describe the potential impact the news might have on the stock mentioned in the article."
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        max_tokens=100,  # Adjusted max_tokens to allow for more detailed summaries
    )
    
    return chat_completion.choices[0].message.content
