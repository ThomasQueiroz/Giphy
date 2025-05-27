import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests

# Carrega variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    api_key = os.getenv('GIPHY_API_KEY')
    if not api_key:
        return "Erro: chave da API do Giphy não configurada", 500
    url = (
        "https://api.giphy.com/v1/gifs/search"
        f"?api_key={api_key}"
        f"&q={query}"
        "&limit=6"
    )

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json().get('data', [])
    except Exception as e:
        return f"Erro ao buscar GIFs: {e}", 500
    gifs = [
        {
            'img': gif['images']['fixed_height']['url'],
            'page': gif['url']
        }
        for gif in data
    ]
    placeholder = {
        'img': '/static/placeholder.png',
        'page': '#'
    }
    while len(gifs) < 6:
        gifs.append(placeholder)

    return render_template('results.html', gifs=gifs, query=query)


if __name__ == '__main__':
    app.run(debug=True)