import csv
import re
import os
from flask import Flask, render_template, request
import asyncio
from telethon import TelegramClient, events
from openai import OpenAI

client = OpenAI(api_key= "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")
OpenAI.api_key = "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"

# API ID for the Telegram application
api_id = 27512487#change this with your api id
#  #int
# API Hash for the Telegram application
api_hash = "8c10f7903a9bd569a6f573985f0f42ed"#chane this with your api hash #str
# Link to the Telegram group 
group_link ="https://t.me/+0bFbTyoUEFUwYTlh" #str

def chat_with_gpt(prompt):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4-1106-preview"
    )
    return(chat_completion.choices[0].message.content)

async def go(api_id, api_hash, group_link):
    conversation = ""
    all_messages = []

    client = TelegramClient("testing", api_id, api_hash)
    await client.start()
    # Fetching the group entity using the group link
    group = await client.get_entity(group_link)
    # Iterating over all messages in the group
    async for message in client.iter_messages(group):
        # Appending each message to the list
        all_messages.append(message.text)

    # Extracting all links from the messages using regex
    for message in all_messages:
        try:
            conversation+= message + "\n"
        except:
            break
    with open("convo.txt", "w") as f:
        f.write(conversation)
    

    await client.disconnect()
    return conversation

# Running the main function
# Importing necessary libraries


app = Flask(__name__)

# Function to fetch and write messages to a CSV file


# Flask route to handle form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        api_id = int(request.form['api_id'])
        api_hash = request.form['hash']
        group_link = request.form['link']

        # Run the async function
        chat_logs = asyncio.run(go(api_id, api_hash, group_link))
        summary = chat_with_gpt("Summarize this conversation:" + chat_logs)
        with open("final.txt", "w") as f:
            f.write(summary)
        
        

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



