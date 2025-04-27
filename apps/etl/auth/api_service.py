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
                f"{self.auth_endpoint}/verify-token", json={"token": token_to_verify}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erreur lors de la vérification du token: {e}")
            return False

    def get_users(self) -> List[Dict]:
        """
        Récupère la liste des utilisateurs via l'API.
        """
        users = []
        try:
            headers = {}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
            
            # Initialiser la variable consecutive_not_found
            consecutive_not_found = 0
            
            # Essayons de récupérer un certain nombre d'utilisateurs par ID
            max_users = 100  # On limite à 100 utilisateurs
            
            for user_id in range(1, max_users):
                try:
                    response = requests.get(f"{self.users_endpoint}/id/{user_id}", headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        consecutive_not_found = 0  # Réinitialiser le compteur
                        if "item" in data and data["item"]:
                            users.append(data["item"])
                    elif response.status_code == 404:
                        consecutive_not_found += 1
                        if consecutive_not_found >= 5:
                            # Arrêter après 5 IDs consécutifs non trouvés
                            break
                except Exception as e:
                    print(f"Erreur lors de la récupération de l'utilisateur {user_id}: {e}")
            
            return users
        except Exception as e:
            print(f"Erreur générale lors de la récupération des utilisateurs: {e}")
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
            headers = {}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"

            response = requests.post(
                f"{self.auth_endpoint}/register", json=payload, headers=headers
            )
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
                
            print(f"Tentative de suppression de l'utilisateur ID {user_id}")
            print(f"URL: {self.users_endpoint}/{user_id}")
            print(f"Headers: {headers}")
            
            # Première tentative avec la méthode DELETE standard
            response = requests.delete(f"{self.users_endpoint}/{user_id}", headers=headers)
            
            if response.status_code == 405:  # Method Not Allowed
                print("DELETE non autorisé, essai avec d'autres méthodes...")
                
                # Essayons avec POST vers un endpoint spécifique à la suppression
                response = requests.post(f"{self.auth_endpoint}/delete-user", 
                                        json={"user_id": user_id}, 
                                        headers=headers)
                
            # Afficher la réponse pour le débogage
            print(f"Réponse API: {response.status_code} - {response.reason}")
            if response.text:
                print(f"Corps de la réponse: {response.text[:200]}...")  # Afficher les 200 premiers caractères
                
            # Vérifier si l'API considère la suppression comme réussie
            return response.status_code in [200, 201, 202, 204]
        except Exception as e:
            print(f"Erreur lors de la suppression d'un utilisateur: {e}")
            return False
