from openai import OpenAI
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Initialize an empty chat history
chat_history = []

def generate_image(text):
    client = OpenAI(api_key='YOUR_API_KEY')

    response = client.images.generate(
        model="dall-e-3",
        prompt=f"create a photo that suits the content of this given text.{text}",
        size="1024x1024",
        quality="standard",
        n=1,    
)
    image_url= response.data[0].url
    return image_url
    

def summary_chat_gpt(metin):
    client1 = OpenAI(api_key='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')
    model = "gpt-3.5-turbo"

    messages = [
        {"role": "system", "content": f"Lütfen aşağıdaki metni kısa ve öz bir şekilde özetle: {metin}"},
    ]

    response = client1.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=400,
    )
    model_response = response.choices[0].message.content
    return model_response

def chat_with_gpt(prompt, role):
    global chat_history
    #expertise = decide_expertise(prompt)
    
    client = OpenAI(api_key='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')
    model = "gpt-3.5-turbo" 

    # Add the user's input to the chat history
    chat_history.append({"role": "user", "content": prompt})

    messages = [
        {"role": "system", "content": role},
    ]

    # Add all previous messages to the conversation
    messages.extend(chat_history)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
    )

    # Get the model's response
    model_response = response.choices[0].message.content

    # Add the model's response to the chat history
    chat_history.append({"role": "assistant", "content": model_response})

    return model_response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    # Define roles
    with open("prompt.json", "r", encoding="utf-8") as file:
        roles_data = json.load(file)

    fitness_trainer_role = roles_data["fitness_trainer_role"]   
    dietitian_role = roles_data["dietitian_role"]
    life_coach_role = roles_data["life_coach_role"]

    roles = [fitness_trainer_role, dietitian_role, life_coach_role]

    combined_response = ""
    for role in roles:
        response = chat_with_gpt(user_input, role)
        with open ("dosya.txt", "a") as file:
            file.write(response+ "\n\n")
        
    file = open("dosya.txt","r")
    combined_response = file.read()
    file2 = open("dosya.txt","w")
    file2.write("")
    file.close()
    summary = summary_chat_gpt(combined_response)
    image_url = generate_image(summary)
    return jsonify({'summary':summary,'image_url':image_url})

if __name__ == '__main__':
    app.run(debug=True)
