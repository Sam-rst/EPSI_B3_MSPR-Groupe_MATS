import hashlib
import os
from auth.api_service import APIService

class AuthManager:
    """
    Gestionnaire d'authentification pour gérer les utilisateurs et l'authentification
    via l'API
    """
    def __init__(self):
        self.current_user = None
        self.api_service = APIService()
    
    def authenticate(self, username, password):
        """Authentifie un utilisateur avec son nom d'utilisateur et mot de passe via l'API"""
        user_data = self.api_service.authenticate(username, password)
        
        if user_data:
            self.current_user = {
                "login": username,
                "role": user_data["role"],
                "region": user_data["region"]
            }
            return True
        return False
    
    def get_current_user(self):
        """Renvoie l'utilisateur actuellement connecté"""
        return self.current_user
    
    def logout(self):
        """Déconnecte l'utilisateur actuel"""
        self.current_user = None
    
    def is_authenticated(self):
        """Vérifie si un utilisateur est connecté"""
        return self.current_user is not None
    
    def has_permission(self, required_role=None):
        """Vérifie si l'utilisateur actuel a le rôle requis"""
        if not self.is_authenticated():
            return False
        
        if required_role is None:
            return True
        
        if required_role == "admin":
            return self.current_user["role"] == "admin"
        
        return self.current_user["role"] in ["admin", required_role]