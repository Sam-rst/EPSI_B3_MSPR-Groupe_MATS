import os
import sys
import requests
from typing import Dict, List
from tkinter import messagebox

# Ajouter le répertoire parent au path pour l'importation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.api_service import APIService

class User:
    """
    Classe représentant un utilisateur du système.
    """
    def __init__(self, id: int, username: str, role: str, region: str):
        self.id = id
        self.username = username
        self.role = role
        self.region = region
    
    @classmethod
    def from_api_data(cls, data: Dict):
        """
        Crée un objet User à partir des données de l'API.
        """
        try:
            # Debug: afficher les clés disponibles
            print(f"Clés disponibles dans les données: {data.keys()}")
            
            return cls(
                id=data.get("id", 0),
                username=data.get("username", ""),
                role=data.get("role_id", ""),
                region=data.get("region", "")
            )
        except Exception as e:
            print(f"Erreur lors de la création d'un utilisateur: {e}")
            # Retourner un utilisateur par défaut
            return cls(0, "Erreur", "Inconnu", "Global")


class UserManager:
    """
    Gestionnaire pour les opérations liées aux utilisateurs.
    """
    def __init__(self):
        self.api = APIService()
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authentifie un utilisateur avec son username et mot de passe.
        """
        user_data = self.api.authenticate(username, password)
        return user_data is not None
    
    def get_user_info(self, username: str) -> Dict:
        """
        Récupère les informations d'un utilisateur par son nom d'utilisateur.
        """
        try:
            headers = {}
            if self.api.token:
                headers["Authorization"] = f"Bearer {self.api.token}"
            
            # Utiliser la route spécifique pour récupérer un utilisateur par son nom
            response = requests.get(f"{self.api.users_endpoint}/username/{username}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "item" in data:
                    return data["item"]
            
            # Si la route directe ne fonctionne pas, essayer de parcourir tous les utilisateurs
            users = self.api.get_users()
            for user in users:
                if user.get("username") == username:
                    return user
                    
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération des informations de l'utilisateur {username}: {e}")
            return None
    
    def add_user(self, username: str, password: str, role: str, region: str) -> bool:
        """
        Ajoute un nouvel utilisateur via l'API.
        """
        # Vérification de la longueur du username et du mot de passe
        if len(username) > 100 or len(password) > 100:
            messagebox.showwarning("Attention", "Le nom d'utilisateur et le mot de passe ne doivent pas dépasser 100 caractères.")
            return False
        
        # Convertir le rôle et la région en ID
        role_id = self._get_role_id(role)
        region_id = self._get_region_id(region)
        
        if role_id is None or region_id is None:
            messagebox.showwarning("Attention", "Rôle ou région invalide.")
            return False
        
        # Ajouter l'utilisateur via l'API
        success = self.api.add_user(username, password, role_id, region_id)
        
        if not success:
            messagebox.showwarning("Attention", f"Impossible d'ajouter l'utilisateur {username}.")
        
        return success
    
    def get_all_users(self) -> List[User]:
        """
        Récupère tous les utilisateurs via l'API.
        """
        users = []
        users_data = self.api.get_users()
        
        print(f"Données brutes des utilisateurs: {users_data}")
        
        for user_data in users_data:
            if user_data.get("username") and user_data.get("role_id") != 0:  # Exclure l'admin
                try:
                    user = User.from_api_data(user_data)
                    users.append(user)
                except Exception as e:
                    print(f"Erreur lors de la création d'un objet User: {e}")
        
        return users
        
    def delete_user(self, user_id: int) -> bool:
        """
        Supprime un utilisateur via l'API.
        """
        if user_id is None:
            print("ID utilisateur invalide")
            return False
        
        try:
            # Tenter la suppression via l'API
            success = self.api.delete_user(user_id)
            
            if not success:
                print(f"Échec de la suppression de l'utilisateur ID {user_id}")
            else:
                print(f"Utilisateur ID {user_id} supprimé avec succès")
                
            return success
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur {user_id}: {e}")
            return False
    
    def _get_role_id(self, role_name: str) -> int:
        """
        Convertit un nom de rôle en ID.
        """
        role_mapping = {
            "admin": 1,
            "user": 2,
            "manager": 3,
            "analyst": 4,
            "guest": 5
        }
        return role_mapping.get(role_name.lower())
    
    def _get_region_id(self, region_name: str) -> int:
        """
        Convertit un nom de région en ID.
        """
        region_mapping = {
            "global": 1,
            "france": 2,
            "états-unis": 3,
            "allemagne": 4,
            "royaume-uni": 5,
            "espagne": 6,
            "italie": 7,
            "chine": 8,
            "japon": 9
        }
        return region_mapping.get(region_name.lower())
    
    def _get_user_by_id(self, user_id: int) -> Dict:
        """
        Récupère les informations d'un utilisateur par son ID via l'API.
        """
        users = self.api.get_users()
        for user in users:
            if user["id"] == user_id:
                return user
        return None