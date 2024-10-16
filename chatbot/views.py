from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def chatbot_page(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def get_chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        
        # Here you would implement your chatbot logic
        # For now, we'll just echo the user's message
        bot_response = f"You said: {user_message}"
        
        return JsonResponse({'response': bot_response})
    return JsonResponse({'error': 'Invalid request'}, status=400)