from django.shortcuts import render
from django.http import JsonResponse
from .models import Word
import json
import random

def index(request):
    """
    Zobrazí hlavní stránku hry a vybere tajné slovo, 
    které uloží do session uživatele.
    """
    # Pokud uživatel přijde poprvé (nebo restartuje hru), vybereme slovo
    if 'wordle_word' not in request.session:
        words = Word.objects.all()
        if words.exists():
            # Vybereme náhodné slovo z databáze
            request.session['wordle_word'] = random.choice(words).text.upper()
        else:
            # Záložní slovo, pokud je databáze prázdná
            request.session['wordle_word'] = "STROM"
            
    return render(request, 'game/index.html')

def check_guess(request):
    """
    Přijme pokus od uživatele přes JavaScript (POST),
    porovná ho s tajným slovem v session a vrátí výsledek.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            guess = data.get('guess', '').upper()
            secret = request.session.get('wordle_word', 'STROM')

            if len(guess) != 5:
                return JsonResponse({'error': 'Slovo musí mít 5 písmen'}, status=400)

            # Logika vyhodnocení barev
            result = []
            for i in range(5):
                if guess[i] == secret[i]:
                    result.append('correct')  # Zelená (shoda písmene i pozice)
                elif guess[i] in secret:
                    result.append('present')  # Žlutá (písmeno tam je, ale jinde)
                else:
                    result.append('absent')   # Šedá (písmeno ve slově není)

            return JsonResponse({
                'result': result,
                'win': guess == secret
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Pouze POST požadavky jsou povoleny'}, status=405)