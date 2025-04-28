import requests
import json
import hashlib
from typing import Dict, List, Optional


class APIService:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.users_endpoint = f"{base_url}/users"
        self.auth_endpoint = f"{base_url}/auth"
        self.token = None

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """
        Authentifie un utilisateur via l'API.
        Retourne les informations de l'utilisateur si l'authentification réussit, sinon None.
        """

        try:
            response = requests.post(
                f"{self.auth_endpoint}/login",
                json={"username": username, "password": password},
            )
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                # Stocker le token pour les futures requêtes
                self.token = data.get("access_token")
                return data
            return None
        except Exception as e:
            print(f"Erreur lors de l'authentification: {e}")
            return None

    def verify_token(self, token: str = None) -> bool:
        """
        Vérifie si un token est valide via l'API.
        Retourne True si le token est valide, False sinon.
        """
        token_to_verify = token or self.token
        if not token_to_verify:
            return False

        try:
            response = requests.post(
                f"{self.auth_endpoint}/verify-token", params={"token": token_to_verify}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erreur lors de la vérification du token: {e}")
            return False

    def get_users(self) -> List[Dict]:
        """
        Récupère la liste des utilisateurs via l'API.
        """
        try:
            headers = {}
            if self.verify_token(self.token):
                headers["Authorization"] = f"Bearer {self.token}"

            response = requests.get(self.users_endpoint, headers=headers)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs: {e}")
            return []

    def add_user(
        self, username: str, password: str, role_id: int, region_id: int
    ) -> bool:
        """
        Ajoute un nouvel utilisateur via l'API.
        Le mot de passe sera hashé côté serveur.
        """

        # Préparer le payload selon le format attendu par l'API
        payload = {
            "username": username,
            "password": password,
            "role_id": role_id,
            "country_id": region_id,
        }

        try:
            response = requests.post(
                f"{self.auth_endpoint}/register", json=payload)
            return response.status_code in [200, 201, 204]
        except Exception as e:
            print(f"Erreur lors de l'ajout d'un utilisateur: {e}")
            return False

    def delete_user(self, user_id: int) -> bool:
        """
        Supprime un utilisateur via l'API.
        """
        try:
            headers = {}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"

            response = requests.delete(
                f"{self.users_endpoint}/{user_id}", headers=headers
            )
            return response.status_code in [200, 204]
        except Exception as e:
            print(f"Erreur lors de la suppression d'un utilisateur: {e}")
            return False


api_service = APIService()
