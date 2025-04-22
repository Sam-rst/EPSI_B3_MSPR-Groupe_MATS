import requests
import json
import hashlib
from typing import Dict, List, Optional

class APIService:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.users_endpoint = f"{base_url}/api/users"
        self.auth_endpoint = f"{base_url}/api/auth"
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """
        Authentifie un utilisateur via l'API.
        Retourne les informations de l'utilisateur si l'authentification réussit, sinon None.
        """
        # Hasher le mot de passe avant de l'envoyer pour sécuriser la transmission
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            response = requests.post(
                self.auth_endpoint,
                json={"username": username, "password_hash": hashed_password}
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erreur lors de l'authentification: {e}")
            return None
    
    def get_users(self) -> List[Dict]:
        """
        Récupère la liste des utilisateurs via l'API.
        """
        try:
            response = requests.get(self.users_endpoint)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs: {e}")
            return []
    
    def add_user(self, username: str, password: str, role_id: int, region_id: int) -> bool:
        """
        Ajoute un nouvel utilisateur via l'API.
        Le mot de passe sera hashé côté serveur.
        """
        # Préparer le payload selon le format attendu par l'API
        payload = {
            "username": username,
            "password": password,  # L'API devrait hasher le mot de passe côté serveur
            "role_id": role_id,
            "region_id": region_id,
            "email": f"{username}@analyseit.com"  # Email généré automatiquement
        }
        
        try:
            response = requests.post(self.users_endpoint, json=payload)
            return response.status_code in [200, 201, 204]
        except Exception as e:
            print(f"Erreur lors de l'ajout d'un utilisateur: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """
        Supprime un utilisateur via l'API.
        """
        try:
            response = requests.delete(f"{self.users_endpoint}/{user_id}")
            return response.status_code in [200, 204]
        except Exception as e:
            print(f"Erreur lors de la suppression d'un utilisateur: {e}")
            return False