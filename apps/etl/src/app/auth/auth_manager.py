import hashlib
import os
from app.auth.api_service import api_service


class AuthManager:
    """
    Gestionnaire d'authentification pour gérer les utilisateurs et l'authentification
    via l'API
    """

    def __init__(self):
        self.current_user = None
        self.api_service = api_service

    def authenticate(self, username, password):
        """Authentifie un utilisateur avec son nom d'utilisateur et mot de passe via l'API"""
        user_data = self.api_service.authenticate(username, password)

        if user_data:
            self.current_user = {
                "id": user_data.get("id"),
                "firstname": user_data.get("firstname"),
                "lastname": user_data.get("lastname"),
                "username": user_data.get("username"),
                "email": user_data.get("email"),
                "role": user_data.get("role"),
                "region": user_data.get("region"),
                "access_token": user_data.get("access_token"),
            }
            return True
        return False

    def get_current_user(self):
        """Renvoie l'utilisateur actuellement connecté"""
        return self.current_user

    def logout(self):
        """Déconnecte l'utilisateur actuel"""
        self.current_user = None
        self.api_service.token = None

    def is_authenticated(self):
        """Vérifie si un utilisateur est connecté"""
        if not self.current_user or not self.current_user.get("access_token"):
            return False

        # Vérifier que le token est toujours valide
        return self.api_service.verify_token(self.current_user.get("access_token"))

    def has_permission(self, required_role=None):
        """Vérifie si l'utilisateur actuel a le rôle requis"""
        if not self.is_authenticated():
            return False

        if required_role is None:
            return True

        user_role = self.current_user.get("role")

        # Les rôles 0 et 1 correspondent aux admins
        if required_role == "admin":
            return user_role <= 1

        # Vérifier si le rôle de l'utilisateur correspond au rôle requis
        if isinstance(required_role, int):
            return user_role <= required_role

        # Convertir les noms de rôle en IDs
        role_mapping = {"admin": 0, "manager": 1, "user": 2, "analyst": 3, "guest": 4}

        role_id = role_mapping.get(required_role.lower(), 999)
        return user_role <= role_id
