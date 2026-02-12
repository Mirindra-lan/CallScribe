import requests
import json
from dotenv import load_dotenv
import os
class LlmApi:
    def __init__(self):
        load_dotenv()
        self.apiKey = os.getenv("OPENAI_API_KEY")
        self.url = os.getenv("OPENAI_URL")
        self.modelLlm = os.getenv("MODEL")
        self.prompt = """
        Tu dois répondre UNIQUEMENT avec un JSON valide.
        AUCUN texte avant ou après.

        Format EXACT à respecter :
            {"res": [
                "réponse 1",
                "réponse 2",
                "réponse 3",
                "réponse 4"
            ]}

            Règles :
            - JSON valide uniquement
            - guillemets doubles obligatoires
            - aucune explication
            - pas de markdown
            - exactement 4 éléments dans "res"
            - réponses professionnelles et polies 

        Contexte : 
        """
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.apiKey}"
        }
    def getSuggestions(self, context):
        self.payload = {
            "model": f"{self.modelLlm}",
            "messages": [
            {
            "role": "user",
            "content": f"{self.prompt} {context}"
            }
            ],
            "temperature": 0.1,
            "max_tokens": 256
        }

        try:
            res = requests.post(
                self.url,
                headers=self.headers,
                json=self.payload,
                timeout=(5, 30)  # toujours mettre timeout
            )

            # Vérifie code HTTP
            res.raise_for_status()

        except requests.exceptions.Timeout:
            print("Timeout API")
            return None
        except requests.exceptions.RequestException as e:
            print("Erreur requête:", e)
            return None

        # Vérifie que la réponse est JSON valide
        try:
            response_json = res.json()
        except ValueError:
            print("Réponse non JSON")
            return None

        # Vérifie la structure attendue
        try:
            content = response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            print("Structure inattendue:", response_json)
            return None

        # Vérifie que content existe
        if not content:
            print("Content vide")
            return None

        # Si le modèle retourne du JSON sous forme de string
        try:
            jsonData = json.loads(content)
        except json.JSONDecodeError:
            print("Le content n'est pas un JSON valide")
            return None

        return jsonData
