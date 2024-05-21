import subprocess
import json
from flask import Flask, request, render_template, redirect, flash
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'przeslane_pliki'
ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)
app.secret_key = 'MatteoJestSuperGosciem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def dozwolony_plik(nazwa_pliku):
    return '.' in nazwa_pliku and nazwa_pliku.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sprawdz_bezpieczenstwo(sciezka_pliku):
    wynik = subprocess.run(['bandit', '-q', '-ll', '-f', 'json', sciezka_pliku], capture_output=True, text=True)
    
    if wynik.returncode != 0:
        try:
            wynik_json = json.loads(wynik.stdout)
            if wynik_json['results']:
                problemy = []
                for problem in wynik_json['results']:
                    problemy.append({
                        'nazwa_pliku': problem['filename'],
                        'opis_problemu': problem['issue_text'],
                        'zakres_linii': problem['line_range'],
                        'istotnosc': problem['issue_severity'],
                        'pewnosc': problem['issue_confidence'],
                        'link_cwe': problem['issue_cwe']['link'],
                        'wiecej_info': problem['more_info'],
                        'kod': problem['code'].replace('\\n', '\n')
                    })
                return problemy
            else:
                return []
        except json.JSONDecodeError:
            return "BladJSON"
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def indeks():
    if request.method == 'POST':
        if 'plik' not in request.files:
            flash('Brak pliku')
            return redirect(request.url)
        plik = request.files['plik']
        if plik.filename == '':
            flash('Nie wybrano pliku')
            return redirect(request.url)
        if plik and dozwolony_plik(plik.filename):
            nazwa_pliku = secure_filename(plik.filename)
            sciezka_pliku = os.path.join(app.config['UPLOAD_FOLDER'], nazwa_pliku)
            plik.save(sciezka_pliku)
            problemy = sprawdz_bezpieczenstwo(sciezka_pliku)
            if problemy == "BladJSON":
                flash('Nie udało się przetworzyć pliku jako JSON.')
                return redirect(request.url)
            return render_template('index.html', problemy=problemy)
    return render_template('index.html', problemy=None)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
