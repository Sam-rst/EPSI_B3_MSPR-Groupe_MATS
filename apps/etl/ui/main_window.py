import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
sys.path.append('..')

from etl.extractor import FileListPanel
from etl.pipeline import ETLPipeline
from configapp import DEFAULT_OUTPUT_DIR
# Importer les styles existants
from ui.styles import (
    MAIN_BG_COLOR, ACCENT_COLOR, LIGHT_BG_COLOR, 
    BUTTON_FONT, TITLE_FONT, ITEM_FONT, configure_button_style
)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=MAIN_BG_COLOR)
        
        # Initialisation des variables
        self.output_dir = DEFAULT_OUTPUT_DIR
        
        # Initialisation du pipeline ETL
        self.pipeline = ETLPipeline(output_dir=self.output_dir)
        
        # Création de l'interface utilisateur
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principale avec disposition en pack pour être responsive
        self.main_frame = tk.Frame(self.root, bg=MAIN_BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre de l'application
        title_label = tk.Label(
            self.main_frame,
            text="Nettoyage de données COVID-19",
            font=TITLE_FONT,
            bg=MAIN_BG_COLOR
        )
        title_label.pack(pady=(0, 20))
        
        # Frame pour les boutons en haut
        top_button_frame = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        top_button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Bouton pour ajouter des fichiers
        add_button = tk.Button(
            top_button_frame,
            text="Ajouter des fichiers CSV",
            font=BUTTON_FONT,
            padx=20,
            pady=10,
            command=self.add_files
        )
        configure_button_style(add_button, is_primary=True)
        add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Texte d'aide pour le glisser-déposer
        help_text = tk.Label(
            top_button_frame,
            text="ou glissez-déposez vos fichiers CSV ici",
            font=ITEM_FONT,
            bg=MAIN_BG_COLOR
        )
        help_text.pack(side=tk.LEFT, padx=(10, 0))
        
        # Frame pour contenir la liste de fichiers
        file_list_container = tk.Frame(self.main_frame, bg=LIGHT_BG_COLOR)
        file_list_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Panneau de liste de fichiers avec scrollbar
        self.file_list_panel = FileListPanel(
            file_list_container,
            on_remove=self.on_file_removed,
            on_selection_change=self.on_selection_changed
        )
        
        # Frame pour le choix du répertoire de sortie
        output_dir_frame = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        output_dir_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Label du répertoire de sortie
        output_dir_label = tk.Label(
            output_dir_frame,
            text="Répertoire de sortie :",
            font=ITEM_FONT,
            bg=MAIN_BG_COLOR
        )
        output_dir_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Affichage du répertoire actuel
        self.output_dir_display = tk.Label(
            output_dir_frame,
            text=self.output_dir,
            font=ITEM_FONT,
            bg=LIGHT_BG_COLOR,
            padx=10,
            pady=5,
            relief=tk.GROOVE,
            width=40,
            anchor="w"
        )
        self.output_dir_display.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Bouton pour changer le répertoire
        change_dir_button = tk.Button(
            output_dir_frame,
            text="Changer",
            font=ITEM_FONT,
            command=self.change_output_dir
        )
        configure_button_style(change_dir_button, is_primary=False)
        change_dir_button.pack(side=tk.RIGHT)
        
        # Frame pour les boutons en bas
        bottom_button_frame = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        bottom_button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Bouton pour exécuter le pipeline
        process_button = tk.Button(
            bottom_button_frame,
            text="Traiter les fichiers",
            font=BUTTON_FONT,
            padx=20,
            pady=10,
            command=self.run_pipeline
        )
        configure_button_style(process_button, is_primary=True)
        process_button.pack(pady=10)
        
        # Étiquette pour afficher les statuts
        self.status_label = tk.Label(
            self.main_frame,
            text="",
            font=ITEM_FONT,
            bg=MAIN_BG_COLOR
        )
        self.status_label.pack(pady=10)
    
    def change_output_dir(self):
        """Permet à l'utilisateur de choisir un nouveau répertoire de sortie"""
        new_dir = filedialog.askdirectory(
            title="Sélectionner le répertoire de sortie",
            initialdir=self.output_dir
        )
        
        if new_dir:  # Si l'utilisateur a sélectionné un répertoire
            self.output_dir = new_dir
            # Mettre à jour l'affichage
            self.output_dir_display.config(text=self.output_dir)
            # Mettre à jour le pipeline
            self.pipeline = ETLPipeline(output_dir=self.output_dir)
            self.update_status(f"Répertoire de sortie changé: {self.output_dir}")
    
    def add_files(self):
        """Ouvre une boîte de dialogue pour sélectionner des fichiers CSV uniquement"""
        filetypes = [
            ("Fichiers CSV", "*.csv"),
            ("Tous les fichiers", "*.*")
        ]
        
        file_paths = filedialog.askopenfilenames(
            title="Sélectionner des fichiers CSV",
            filetypes=filetypes
        )
        
        if file_paths:
            # Filtrer pour ne garder que les fichiers CSV
            csv_files = [path for path in file_paths if path.lower().endswith('.csv')]
            
            if len(csv_files) != len(file_paths):
                messagebox.showwarning("Format non supporté", 
                                      f"{len(file_paths) - len(csv_files)} fichier(s) ignoré(s) car non CSV.")
            
            if csv_files:
                self.file_list_panel.add_files(csv_files)
                self.update_status(f"{len(csv_files)} fichier(s) CSV ajouté(s)")
    
    def on_drop(self, event):
        """Gère le glisser-déposer de fichiers CSV uniquement"""
        file_paths = self.root.tk.splitlist(event.data)
        
        # Filtrer pour ne garder que les fichiers CSV
        csv_files = [path for path in file_paths if path.lower().endswith('.csv')]
        
        if len(csv_files) != len(file_paths):
            messagebox.showwarning("Format non supporté", 
                                  f"{len(file_paths) - len(csv_files)} fichier(s) ignoré(s) car non CSV.")
        
        if csv_files:
            self.file_list_panel.add_files(csv_files)
            self.update_status(f"{len(csv_files)} fichier(s) CSV ajouté(s) par glisser-déposer")
    
    def on_file_removed(self, index):
        """Callback quand un fichier est supprimé"""
        self.update_status("Fichier supprimé")
    
    def on_selection_changed(self, file_list):
        """Callback quand la sélection change"""
        selected_count = sum(1 for file_info in file_list if file_info.selected)
        total_count = len(file_list)
        self.update_status(f"{selected_count}/{total_count} fichiers sélectionnés")
    
    def update_status(self, message):
        """Met à jour le message de statut"""
        self.status_label.config(text=message)
    
    def run_pipeline(self):
        """Exécute le pipeline ETL sur les fichiers sélectionnés"""
        print("Démarrage du pipeline ETL")  # Message de débogage
        selected_files = self.file_list_panel.get_selected_files()
        
        print(f"Fichiers sélectionnés : {len(selected_files)}")  # Message de débogage
        if not selected_files:
            messagebox.showwarning("Attention", "Aucun fichier sélectionné")
            return
        
        # Afficher une barre de progression ou un message de chargement
        self.update_status("Traitement en cours...")
        self.root.update()
        
        try:
            # Mettre à jour le pipeline avec le répertoire de sortie actuel
            self.pipeline = ETLPipeline(output_dir=self.output_dir)
            
            # Exécuter le pipeline
            success = self.pipeline.run(selected_files)
            
            if success:
                output_dir = os.path.abspath(self.output_dir)
                message = f"Traitement terminé avec succès !\nLes fichiers nettoyés sont disponibles dans :\n{output_dir}"
                messagebox.showinfo("Succès", message)
                self.update_status("Traitement terminé")
            else:
                messagebox.showerror("Erreur", "Le traitement a échoué")
                self.update_status("Échec du traitement")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
            self.update_status("Erreur pendant le traitement")
            print(f"Erreur : {str(e)}")