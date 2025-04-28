import tkinter as tk
from tkinter import messagebox
import os

from app.ui.styles import (
    MAIN_BG_COLOR,
    LIGHT_BG_COLOR,
    ACCENT_COLOR,
    TITLE_FONT,
    BUTTON_FONT,
    LABEL_FONT,
)
from app.ui.styles import configure_button_style
from app.auth.api_service import api_service


class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.api = api_service

        # Création de l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=MAIN_BG_COLOR)
        self.main_frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8
        )

        # Titre
        title_label = tk.Label(
            self.main_frame,
            text="Analyze IT - Login",
            font=TITLE_FONT,
            bg=MAIN_BG_COLOR,
        )
        title_label.pack(pady=(0, 40))

        # Frame de connexion
        login_frame = tk.Frame(self.main_frame, bg=LIGHT_BG_COLOR, padx=40, pady=40)
        login_frame.pack(padx=50, pady=20)

        # Champs de saisie
        username_label = tk.Label(
            login_frame,
            text="Nom d'utilisateur:",
            font=LABEL_FONT,
            bg=LIGHT_BG_COLOR,
            anchor="w",
        )
        username_label.pack(fill=tk.X, pady=(0, 5))

        self.username_entry = tk.Entry(login_frame, font=LABEL_FONT, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 20))

        password_label = tk.Label(
            login_frame,
            text="Mot de passe:",
            font=LABEL_FONT,
            bg=LIGHT_BG_COLOR,
            anchor="w",
        )
        password_label.pack(fill=tk.X, pady=(0, 5))

        self.password_entry = tk.Entry(login_frame, font=LABEL_FONT, width=30, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 30))

        # Bouton de connexion
        login_button = tk.Button(
            login_frame,
            text="Se connecter",
            font=BUTTON_FONT,
            padx=20,
            pady=10,
            command=self._login,
        )
        configure_button_style(login_button, is_primary=True)
        login_button.pack(pady=(0, 10))

        # Bind de la touche Entrée
        self.root.bind("<Return>", lambda event: self._login())

    def _login(self):
        """Tentative de connexion avec les identifiants fournis en utilisant l'API"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Vérification de la longueur du nom d'utilisateur et du mot de passe
        if len(username) > 100 or len(password) > 100:
            messagebox.showwarning(
                "Attention",
                "Le nom d'utilisateur et le mot de passe ne doivent pas dépasser 100 caractères.",
            )
            return

        if not username or not password:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
            return

        # Authentification via l'API
        print(username, password)
        user_data = self.api.authenticate(username, password)
        print(user_data)

        if user_data:
            self.root.unbind("<Return>")
            # Sauvegarde de l'utilisateur connecté
            self.current_user = {
                "username": username,
                "role_id": user_data["role_id"],
                "country_id": user_data["country_id"],
            }
            # Appel du callback de connexion réussie
            self.on_login_success(self.current_user)
        else:
            messagebox.showerror(
                "Erreur", "Nom d'utilisateur ou mot de passe incorrect."
            )
