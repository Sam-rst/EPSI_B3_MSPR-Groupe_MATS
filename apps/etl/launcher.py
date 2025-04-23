import tkinter as tk
import os
import sys
import importlib.util
from tkinter import messagebox
from configapp import APP_TITLE, DEFAULT_SIZE, MIN_WIDTH, MIN_HEIGHT

# Ajouter le répertoire courant au path pour l'importation
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from auth.db_connector import PostgresConnector
from auth.api_service import APIService

# Gestion du drag & drop pour l'ETL si nécessaire
try:
    from tkinterdnd2 import TkinterDnD

    has_dnd = True
except ImportError:
    has_dnd = False
    print(
        "tkinterdnd2 n'est pas installé. Le glisser-déposer ne sera pas disponible dans l'ETL."
    )

# Définition des chemins
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ADMIN_DASHBOARD_DIR = os.path.join(CURRENT_DIR, "adminDashboard")

# Styles de base pour l'interface
MAIN_BG_COLOR = "#C5D5F0"
ACCENT_COLOR = "#4A7CFF"
LIGHT_BG_COLOR = "#FFFFFF"
TITLE_FONT = ("Arial", 30, "bold")
BUTTON_FONT = ("Arial", 12, "bold")
LABEL_FONT = ("Arial", 12)


def configure_button_style(button, is_primary=True):
    if is_primary:
        button.configure(
            font=BUTTON_FONT,
            bg=ACCENT_COLOR,
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            borderwidth=0,
            activebackground="#3A6CFF",
            activeforeground="white",
            cursor="hand2",
        )
    else:
        button.configure(
            font=BUTTON_FONT,
            bg="#F0F0F0",
            fg="#000000",
            padx=20,
            pady=10,
            relief="flat",
            borderwidth=0,
            activebackground="#E0E0E0",
            activeforeground="#000000",
            cursor="hand2",
        )


class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(DEFAULT_SIZE)
        self.root.minsize(MIN_HEIGHT, MIN_HEIGHT)

        # Configurer le redimensionnement
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Initialisation de l'API
        self.api = APIService()

        # Cache des infos utilisateurs
        self.current_user = None

        # Démarrer avec l'écran de connexion
        self.show_login_screen()

    def show_login_screen(self):
        """Affiche l'écran de connexion"""
        # Nettoyer les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=MAIN_BG_COLOR)
        self.main_frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8
        )

        # Titre
        title_label = tk.Label(
            self.main_frame, text="Analyze IT", font=TITLE_FONT, bg=MAIN_BG_COLOR
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
        """Gère la connexion de l'utilisateur via l'API"""
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
        self.current_user = self.api.authenticate(username, password)
        if self.current_user:
            self.root.unbind("<Return>")
            # Afficher l'écran de sélection d'application si c'est un admin
            if self.current_user["role_id"] <= 1:
                self.show_app_selection_screen()
            else:
                # Les utilisateurs non-admin vont directement vers l'ETL
                self.launch_etl_app()
        else:
            # print(result)
            messagebox.showerror(
                "Erreur", "Nom d'utilisateur ou mot de passe incorrect."
            )

    def show_app_selection_screen(self):
        """Affiche l'écran de sélection entre ETL et Dashboard Admin"""
        # Nettoyer les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=MAIN_BG_COLOR)
        self.main_frame.place(
            relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8
        )

        # Informations utilisateur
        user_label = tk.Label(
            self.main_frame,
            text=f"Connecté en tant que : {self.current_user['username']} ({self.current_user['role_id']})",
            font=LABEL_FONT,
            bg=MAIN_BG_COLOR,
        )
        user_label.pack(pady=(0, 40))

        # Titre
        title_label = tk.Label(
            self.main_frame,
            text="Sélectionnez une application",
            font=TITLE_FONT,
            bg=MAIN_BG_COLOR,
        )
        title_label.pack(pady=(0, 60))

        # Boutons d'application
        apps_frame = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        apps_frame.pack(pady=20)

        etl_button = tk.Button(
            apps_frame,
            text="ETL - Traitement de données",
            font=BUTTON_FONT,
            padx=30,
            pady=20,
            width=25,
            command=self.launch_etl_app,
        )
        configure_button_style(etl_button, is_primary=True)
        etl_button.pack(pady=(0, 30))

        admin_button = tk.Button(
            apps_frame,
            text="Dashboard Administrateur",
            font=BUTTON_FONT,
            padx=30,
            pady=20,
            width=25,
            command=self.launch_admin_dashboard,
        )
        configure_button_style(admin_button, is_primary=False)
        admin_button.pack()

        # Bouton de déconnexion
        logout_button = tk.Button(
            self.main_frame, text="Déconnexion", command=self.show_login_screen
        )
        configure_button_style(logout_button, is_primary=False)
        logout_button.pack(side=tk.BOTTOM, pady=20)

    def launch_etl_app(self):
        """Lance l'application ETL"""
        try:
            # Importer dynamiquement les modules ETL
            spec = importlib.util.spec_from_file_location(
                "main_window", os.path.join(CURRENT_DIR, "ui", "main_window.py")
            )
            main_window_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_window_module)

            # Nettoyer l'écran actuel
            for widget in self.root.winfo_children():
                widget.destroy()

            # Lancer l'ETL avec l'utilisateur connecté
            main_window_module.MainWindow(self.root, self.current_user)

            print(
                f"Application ETL lancée pour l'utilisateur {self.current_user['username']}"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'ETL: {str(e)}")
            print(f"Erreur lors du lancement de l'ETL: {str(e)}")
            # Afficher les détails de l'erreur pour le débogage
            import traceback

            traceback.print_exc()
            self.show_app_selection_screen()

    def launch_admin_dashboard(self):
        """Lance le Dashboard Administrateur"""
        try:
            # S'assurer que le chemin vers adminDashboard est dans sys.path
            if ADMIN_DASHBOARD_DIR not in sys.path:
                sys.path.append(ADMIN_DASHBOARD_DIR)

            # Importer la classe AdminDashboardApp du module admin_dashboard_main
            from adminDashboard.admin_dashboard_main import AdminDashboardApp

            # Nettoyer l'écran actuel
            for widget in self.root.winfo_children():
                widget.destroy()

            # Créer l'instance du dashboard
            dashboard_app = AdminDashboardApp(self.root)

            # Ajouter un bouton de retour au lanceur
            return_button = tk.Button(
                dashboard_app.dashboard.bottom_button_frame,
                text="Retour au lanceur",
                command=self._return_to_launcher,
            )
            configure_button_style(return_button, is_primary=False)
            return_button.pack(side=tk.RIGHT, padx=10)

            print(
                f"Dashboard administrateur lancé pour l'utilisateur {self.current_user['username']}"
            )

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible de lancer le Dashboard Admin: {str(e)}"
            )
            print(f"Erreur lors du lancement du Dashboard Admin: {str(e)}")
            print(f"Type d'erreur: {type(e).__name__}")
            print(f"Détails: {str(e)}")
            import traceback

            traceback.print_exc()
            self.show_app_selection_screen()

    def _return_to_launcher(self):
        """Fonction pour retourner à l'écran de sélection"""
        # Nettoyer l'écran
        for widget in self.root.winfo_children():
            widget.destroy()

        # Réafficher l'écran de sélection d'applications
        self.show_app_selection_screen()


def main():
    """Fonction principale de lancement de l'application"""
    if has_dnd:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    app = LauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
