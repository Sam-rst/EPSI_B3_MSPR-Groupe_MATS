# adminDashboard/models.py
"""
Module contenant les modèles de données pour l'application Admin Dashboard.
"""

import os
import sys
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
        return cls(
            id=data["id"],
            username=data["username"],
            role=data["role_id"],
            region=data["region"]
        )


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
        Récupère les informations d'un utilisateur.
        """
        users = self.api.get_users()
        for user in users:
            if user["username"] == username:
                return user
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
        users_data = self.api.get_users()
        users = []
        
        for user_data in users_data:
            # Filtrer l'admin si nécessaire
            if user_data.get("role") != "admin":
                users.append(User.from_api_data(user_data))
        
        return users
    
    def delete_user(self, user_id: int) -> bool:
        """
        Supprime un utilisateur via l'API.
        """
        if user_id is None:
            messagebox.showwarning("Attention", "ID utilisateur invalide.")
            return False
        
        # Vérifier que ce n'est pas l'admin via l'API
        user_info = self._get_user_by_id(user_id)
        if user_info and user_info.get("role") == "admin":
            messagebox.showwarning("Attention", "Opération non autorisée.")
            return False
        
        # Supprimer via l'API
        success = self.api.delete_user(user_id)
        
        if not success:
            messagebox.showwarning("Attention", f"Impossible de supprimer l'utilisateur avec ID {user_id}.")
        
        return success
    
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