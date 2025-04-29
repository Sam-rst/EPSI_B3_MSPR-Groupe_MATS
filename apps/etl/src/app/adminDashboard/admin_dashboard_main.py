"""
Fichier principal du dashboard administrateur.
Ce fichier permet de lancer le dashboard depuis le lanceur principal.
"""

import tkinter as tk
import os
from tkinter import messagebox

from app.adminDashboard.translations import LanguageManager
from app.adminDashboard.admin_dashboard_window import AdminDashboardWindow


class AdminDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - ETL")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Centrer la fenêtre
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 500) // 2
        self.root.geometry(f"800x500+{x}+{y}")

        # Initialiser le gestionnaire de langue
        self.language_manager = LanguageManager()

        # Créer et afficher le dashboard
        self.dashboard = AdminDashboardWindow(self.root, self.language_manager)
        self.dashboard.pack(fill="both", expand=True, padx=10, pady=10)


if __name__ == "__main__":
    # Ce code ne sera exécuté que si ce fichier est le point d'entrée principal
    root = tk.Tk()
    app = AdminDashboardApp(root)
    root.mainloop()
