import os
import requests
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file credentials.env
load_dotenv('.env')

# --- CONFIGURAZIONE ---
API_KEY = os.getenv('NEWSAPI_KEY')
# Argomento della ricerca: puoi cambiarlo con qualsiasi azienda o keyword
QUERY = 'Tesla'
# Lingua degli articoli per coerenza
LANGUAGE = 'it' # Puoi usare 'en' per inglese, 'it' per italiano, etc.
# Ordina per popolarità, pertinenza (relevancy) o data di pubblicazione (publishedAt)
SORT_BY = 'relevancy'
# Numero di articoli da visualizzare
ARTICLE_LIMIT = 5

# Costruisci l'URL per la richiesta API all'endpoint 'everything'
URL = f'https://newsapi.org/v2/everything?q={QUERY}&language={LANGUAGE}&sortBy={SORT_BY}&apiKey={API_KEY}'


def test_newsapi_connection():
    """
    Funzione per testare la connessione a NewsAPI e recuperare articoli.
    """
    print(f"▶️  Tentativo di connessione a NewsAPI per cercare notizie su: '{QUERY}'")

    # Controlla se la chiave API è stata caricata
    if not API_KEY:
        print("❌ ERRORE: Chiave API di NewsAPI non trovata.")
        print("Assicurati di aver creato il file 'credentials.env' e di aver impostato NEWSAPI_KEY.")
        return

    try:
        # Esegui la richiesta GET
        response = requests.get(URL)
        response.raise_for_status()  # Solleva un'eccezione per status code non-200

        data = response.json()

        # NewsAPI usa un campo 'status' per comunicare l'esito
        if data.get('status') != 'ok':
            error_message = data.get('message', 'Errore sconosciuto da NewsAPI.')
            print(f"❌ ERRORE dall'API: {error_message}")
            return

        articles = data.get('articles', [])
        
        if not articles:
            print(f"✅ Connessione riuscita, ma non sono stati trovati articoli per '{QUERY}'.")
            return

        print(f"✅ Connessione all'API riuscita! Trovati {data['totalResults']} articoli.")
        
        print(f"\n--- Primi {ARTICLE_LIMIT} articoli più pertinenti per '{QUERY}' ---")
        for i, article in enumerate(articles[:ARTICLE_LIMIT]):
            source_name = article.get('source', {}).get('name', 'N/D')
            title = article.get('title', 'N/D')
            print(f"  {i+1}. \"{title}\" (Fonte: {source_name})")
        print("----------------------------------------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERRORE di connessione: {e}")
    except Exception as e:
        print(f"❌ Si è verificato un errore inaspettato: {e}")

if __name__ == "__main__":
    test_newsapi_connection()