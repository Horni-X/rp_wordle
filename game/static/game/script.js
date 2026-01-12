const grid = document.getElementById('grid');
const input = document.getElementById('guessInput');
const btn = document.getElementById('submitBtn');
const keyboard = document.getElementById('keyboard');
let currentRow = 0;

// 1. Generování mřížky
for (let r = 0; r < 6; r++) {
    const row = document.createElement('div');
    row.classList.add('row');
    for (let c = 0; c < 5; c++) {
        const tile = document.createElement('div');
        tile.classList.add('tile');
        tile.id = `tile-${r * 5 + c}`;
        row.appendChild(tile);
    }
    grid.appendChild(row);
}

// 2. Generování klávesnice
const layout = ["QWERTZUIOP", "ASDFGHJKL", "YXCVBNM"];
layout.forEach(rowStr => {
    const rowDiv = document.createElement('div');
    rowDiv.classList.add('keyboard-row');
    rowStr.split('').forEach(char => {
        const key = document.createElement('div');
        key.classList.add('key');
        key.textContent = char;
        key.id = `key-${char}`;
        key.addEventListener('click', () => {
            if (input.value.length < 5) input.value += char;
        });
        rowDiv.appendChild(key);
    });
    keyboard.appendChild(rowDiv);
});

// 3. Logika odeslání
async function submitGuess() {
    const guess = input.value.toUpperCase();
    if (guess.length !== 5) return;

    const response = await fetch(checkGuessUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ guess })
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    // Obarvení mřížky a klávesnice
    data.result.forEach((status, i) => {
        const tile = document.getElementById(`tile-${currentRow * 5 + i}`);
        tile.textContent = guess[i];
        tile.classList.add(status);
        
        // Update klávesnice
        const key = document.getElementById(`key-${guess[i]}`);
        if (key) {
            if (status === 'correct') key.className = 'key correct';
            else if (status === 'present' && !key.classList.contains('correct')) key.className = 'key present';
            else if (!key.classList.contains('correct') && !key.classList.contains('present')) key.className = 'key absent';
        }
    });

    if (data.win) alert("Vítězství!");
    currentRow++;
    input.value = '';
}

btn.addEventListener('click', submitGuess);
input.addEventListener('keypress', (e) => { if (e.key === 'Enter') submitGuess(); });