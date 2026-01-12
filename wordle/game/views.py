from django.shortcuts import render
from django.http import JsonResponse
from .models import Word
import json, random

def index(request):
    # Pokud nemáme v session vybrané slovo, jedno náhodné z DB vybereme
    if 'wordle_word' not in request.session:
        words = Word.objects.filter(is_active=True)
        if words.exists():
            request.session['wordle_word'] = random.choice(words).text.upper()
        else:
            request.session['wordle_word'] = "STROM" # Záloha
    return render(request, 'game/index.html')

def check_guess(request):
    data = json.loads(request.body)
    guess = data.get('guess', '').upper()
    secret = request.session.get('wordle_word')
    
    result = []
    for i in range(5):
        if guess[i] == secret[i]:
            result.append('correct')
        elif guess[i] in secret:
            result.append('present')
        else:
            result.append('absent')
            
    return JsonResponse({'result': result, 'win': guess == secret})