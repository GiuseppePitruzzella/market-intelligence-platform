import os
import praw
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file credentials.env
load_dotenv('.env')

# --- CONFIGURAZIONE ---
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USER_AGENT = os.getenv('REDDIT_USER_AGENT')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')

# Subreddit da cui estrarre i dati
TARGET_SUBREDDIT = 'investing'
POST_LIMIT = 5

def test_reddit_connection():
    """
    Funzione per testare l'autenticazione all'API di Reddit e recuperare i post.
    """
    print(f"▶️  Tentativo di connessione a Reddit e al subreddit r/{TARGET_SUBREDDIT}")

    # Controlla che tutte le credenziali siano state caricate
    if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT, USERNAME, PASSWORD]):
        print("❌ ERRORE: Una o più credenziali di Reddit non sono state trovate.")
        print("Assicurati che 'credentials.env' contenga tutti i campi REDDIT_* necessari.")
        return

    try:
        # Autenticazione tramite PRAW
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            username=USERNAME,
            password=PASSWORD,
        )

        # La chiamata seguente verifica che l'autenticazione sia valida
        # e non solo in modalità di sola lettura.
        print(f"✅ Autenticazione a Reddit come utente '{reddit.user.me()}' riuscita!")

        # Seleziona il subreddit
        subreddit = reddit.subreddit(TARGET_SUBREDDIT)
        print(f"✅ Accesso al subreddit r/{subreddit.display_name} effettuato.")

        # Recupera i post più popolari (hot)
        hot_posts = subreddit.hot(limit=POST_LIMIT)

        print(f"\n--- Primi {POST_LIMIT} post 'hot' da r/{TARGET_SUBREDDIT} ---")
        for i, post in enumerate(hot_posts):
            # Stampa titolo, punteggio (upvotes - downvotes) e URL
            print(f"  {i+1}. \"{post.title}\" (Score: {post.score})")
            # print(f"     URL: {post.url}") # Puoi decommentare per vedere l'URL
        print("---------------------------------------------\n")
    except Exception as e:
        print(f"❌ Si è verificato un errore inaspettato: {e}")


if __name__ == "__main__":
    test_reddit_connection()