import os
import requests
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file credentials.env
load_dotenv('.env')

# --- CONFIGURAZIONE ---
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
SYMBOL = 'INTC'  # Simbolo del titolo da testare (es. Intel Corporation)
FUNCTION = 'TIME_SERIES_INTRADAY'
INTERVAL = '5min'  # Intervallo: 1min, 5min, 15min, 30min, 60min

# Costruisci l'URL per la richiesta API
URL = f'https://www.alphavantage.co/query?function={FUNCTION}&symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}'

def test_api_connection():
    """
    Funzione per testare la connessione all'API Alpha Vantage e recuperare i dati.
    """
    print(f"[INFO]  Tentativo di connessione all'API per il simbolo: {SYMBOL}")

    # Controlla se la chiave API è stata caricata correttamente
    if not API_KEY:
        print("[ERROR]  Chiave API Alpha Vantage non trovata.")
        print("Assicurati di aver creato il file 'credentials.env' e di aver impostato ALPHA_VANTAGE_API_KEY.")
        return

    try:
        # Esegui la richiesta GET
        response = requests.get(URL)
        # Lancia un'eccezione se la richiesta ha avuto un esito negativo (es. 404, 500)
        response.raise_for_status()

        data = response.json()

        # Alpha Vantage potrebbe restituire un messaggio di errore nel JSON anche con status 200
        if "Error Message" in data:
            print(f"[ERROR]  {data['Error Message']}")
            return
        
        # Cerca la chiave principale dei dati della serie temporale
        time_series_key = f"Time Series ({INTERVAL})"
        if time_series_key not in data:
            print(f"[ERROR] La risposta JSON non contiene la chiave '{time_series_key}'.")
            print("Risposta ricevuta:", data)
            return

        print("[SUCCESS] Connessione all'API riuscita e dati ricevuti correttamente!")
        
        # Estrai e stampa l'ultimo dato disponibile per conferma
        time_series = data[time_series_key]
        latest_timestamp = next(iter(time_series)) # Prende la prima chiave (la più recente)
        latest_data = time_series[latest_timestamp]

        print("\n--- Esempio Dati Ricevuti ---")
        print(f"Timestamp più recente: {latest_timestamp}")
        print(f"  Apertura (1. open):   {latest_data['1. open']}")
        print(f"  Massimo (2. high):    {latest_data['2. high']}")
        print(f"  Minimo (3. low):     {latest_data['3. low']}")
        print(f"  Chiusura (4. close):  {latest_data['4. close']}")
        print(f"  Volume (5. volume):   {latest_data['5. volume']}")
        print("-----------------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR]  Connessione: {e}")
    except KeyError:
        print("[ERROR]  Struttura del JSON ricevuto non è quella prevista.")
    except Exception as e:
        print(f"Si è verificato un errore inaspettato: {e}")

if __name__ == "__main__":
    test_api_connection()