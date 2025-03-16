import tkinter as tk
import os
from ui.upload_panel import UploadPanel
from ui.styles import MAIN_BG_COLOR

class MainWindow:
    """
    Classe pour la fenêtre principale de l'application
    Gère l'organisation des différents panneaux et la navigation
    """
    
    def __init__(self, root):
        """
        Initialise la fenêtre principale.
        
        Args:
            root (tk.Tk): La racine Tkinter
        """
        self.root = root
        self.root.configure(bg=MAIN_BG_COLOR)
        
        # État de l'application
        self.current_panel = None
        
        # Initialisation de l'interface
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur principale"""
        # Frame principal avec marge
        self.main_frame = tk.Frame(self.root, bg=MAIN_BG_COLOR, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Essai de chargement de l'image de fond
        try:
            # Vérifier si le fichier image existe
            logo_path = "analyzeitlogo.png"
            if os.path.exists(logo_path):
                # Créer une image de fond
                self.bg_image = tk.PhotoImage(file=logo_path)
                
                # Créer un label pour l'image
                bg_label = tk.Label(self.main_frame, image=self.bg_image, bg=MAIN_BG_COLOR)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label.lower()  # Mettre l'image en arrière-plan
        except Exception as e:
            print(f"Erreur lors du chargement de l'image: {e}")
        
        # Container pour les panneaux (pour switcher entre les vues)
        self.panel_container = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        self.panel_container.pack(fill=tk.BOTH, expand=True)
        
        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt à charger des fichiers")
        self.status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=10,
            font=("Arial", 10)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Afficher le panneau d'upload par défaut
        self.show_upload_panel()
    
    def show_upload_panel(self):
        """Affiche le panneau d'upload de fichiers"""
        # Nettoyer le container
        for widget in self.panel_container.winfo_children():
            widget.destroy()
        
        # Créer et afficher le panneau d'upload
        self.upload_panel = UploadPanel(
            self.panel_container,
            status_callback=self.update_status
        )
        self.current_panel = "upload"
    
    def update_status(self, message):
        """
        Met à jour le message de la barre de statut.
        
        Args:
            message (str): Le nouveau message à afficher
        """
        self.status_var.set(message)