from django.shortcuts import render, HttpResponse


# Create your views here.
import openai
from django.http import JsonResponse
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def home(request):
    return render(request,'home.html')

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            query = data.get('query')
            print(query)
            
            # Make a call to OpenAI GPT-3
            response = chat_with_gpt3(query)

            # Send the response to the front end
            return JsonResponse({'response': response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

def chat_with_gpt3(query):
    openai.api_key = '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'

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ]
    )

    return response.choices[0].message['content']



from sentence_transformers import SentenceTransformer
import pinecone


def find_match(input):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    pinecone.init(api_key='936c8e40-4b60-4d19-a550-a71009e8dc70', environment='gcp-starter')
    index = pinecone.Index('test')
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

@csrf_exempt
def chat_with_company_data(request):
     openai.api_key = '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'

     if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            query = data.get('query')
            print(query)

            context = find_match(query)
            response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot assistant for Knovatek Inc. Your goal is to assist customers with inquiries related to our products and services. Provide helpful and accurate information. If needed, ask clarifying questions for better understanding. Be customer-centric and maintain a professional tone. Thank you!"},
                {"role": "user", "content": context},
                {"role": "user", "content": query},
            ]
        )

            # Get response from ChatGPT API
            chat_response = response['choices'][0]['message']['content']
            return JsonResponse({'response': chat_response})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    