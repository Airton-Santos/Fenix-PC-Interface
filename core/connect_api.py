import requests

def chamar_feni_na_nuvem(mensagem):
    # Definimos a URL base da sua API FastAPI
    url = "https://fenix-brain-production.up.railway.app/comunicar"
    
    try:
        # Como a API usa @app.get, enviamos a mensagem como um parâmetro (params)
        params = {"mensagem": mensagem}
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            try:
                data = response.json()
                return data.get("Feni", "Não recebi resposta da Feni.")
            except ValueError:
                return "Erro: O servidor respondeu, mas o formato dos dados está incorreto."
        else:
            return f"Erro no servidor: Status {response.status_code}"
            
    except Exception as e:
        return f"Falha de conexão com o núcleo: {e}"