import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
sys.path.append('..')

from pipelines.extract import FileListPanel
from pipelines.pipeline import ETLPipeline
from configapp import DEFAULT_OUTPUT_DIR
from ui.styles import configure_button_style
from ui.styles import (
    MAIN_BG_COLOR, ACCENT_COLOR, LIGHT_BG_COLOR, 
    BUTTON_FONT, TITLE_FONT, ITEM_FONT, configure_button_style
)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=MAIN_BG_COLOR)
        
        self.output_dir = DEFAULT_OUTPUT_DIR
        
        # Initialisation du pipeline ETL
        self.pipeline = ETLPipeline(output_dir=self.output_dir)
        
        #Création de l'interface utilisateur
        self.create_widgets()
        
        try:
            print("Tentative d'enregistrement du glisser-déposer...")
            self.root.drop_target_register("DND_Files")
            self.root.dnd_bind("<<Drop>>", self.on_drop)
            print("Enregistrement du glisser-déposer réussi!")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du glisser-déposer: {e}")
            print("Le glisser-déposer ne sera pas disponible")
    
    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=MAIN_BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            self.main_frame,
            text="Analyze IT",
            font=TITLE_FONT,
            bg=MAIN_BG_COLOR
        )
        title_label.pack(pady=(0, 20))
        
        top_button_frame = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        top_button_frame.pack(fill=tk.X, pady=(0, 10))
        
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
        
        help_text = tk.Label(
            top_button_frame,
            text="ou glissez-déposez vos fichiers CSV ici",
            font=ITEM_FONT,
            bg=MAIN_BG_COLOR
        )
        help_text.pack(side=tk.LEFT, padx=(10, 0))
        
        #Frame pour contenir la liste de fichiers
        file_list_container = tk.Frame(self.main_frame, bg=LIGHT_BG_COLOR)
        file_list_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        #Panneau de liste de fichiers avec scrollbar
        self.file_list_panel = FileListPanel(
            file_list_container,
            on_remove=self.on_file_removed,
            on_selection_change=self.on_selection_changed
        )
        
        output_dir_frame = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        output_dir_frame.pack(fill=tk.X, pady=(10, 0))
        
        output_dir_label = tk.Label(
            output_dir_frame,
            text="Répertoire de sortie :",
            font=ITEM_FONT,
            bg=MAIN_BG_COLOR
        )
        output_dir_label.pack(side=tk.LEFT, padx=(0, 10))
        
        #Affichage du répertoire actuel
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
        
        #Changement de repo
        change_dir_button = tk.Button(
            output_dir_frame,
            text="Changer",
            font=ITEM_FONT,
            command=self.change_output_dir
        )
        configure_button_style(change_dir_button, is_primary=False)
        change_dir_button.pack(side=tk.RIGHT)
        
        #Frame pour les boutons en bas
        bottom_button_frame = tk.Frame(self.main_frame, bg=MAIN_BG_COLOR)
        bottom_button_frame.pack(fill=tk.X, pady=(10, 0))
        
        #Bouton pour executer la pipeline
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

        db_button = tk.Button(
            bottom_button_frame,
            text="Charger dans PostgreSQL",
            font=BUTTON_FONT,
            padx=20,
            pady=10,
            command=self.connect_to_database
        )
        configure_button_style(db_button, is_primary=False)
        db_button.pack(side=tk.BOTTOM, pady=10)
    
    def change_output_dir(self):
        """Permet à l'utilisateur de choisir un nouveau répertoire de sortie"""
        new_dir = filedialog.askdirectory(
            title="Sélectionner le répertoire de sortie",
            initialdir=self.output_dir
        )
        
        if new_dir:
            self.output_dir = new_dir
            self.output_dir_display.config(text=self.output_dir)
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
            #Filtrer pour ne garder que les fichiers CSV
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
        
        #Filtrage pour ne garder que les fichiers CSV
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
        print("Démarrage du pipeline ETL")
        selected_files = self.file_list_panel.get_selected_files()
        
        print(f"Fichiers sélectionnés : {len(selected_files)}")
        if not selected_files:
            messagebox.showwarning("Attention", "Aucun fichier sélectionné")
            return
        
        self.update_status("Traitement en cours...")
        self.root.update()
        
        try:
            self.pipeline = ETLPipeline(output_dir=self.output_dir)
            
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
            
    def connect_to_database(self):
        """Ouvre une boîte de dialogue pour se connecter à PostgreSQL et charger les données"""
        #Verifier si des fichiers ont été traités
        if not self.pipeline.transformed_datasets:
            messagebox.showwarning("Attention", "Veuillez d'abord traiter des fichiers CSV")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Connexion PostgreSQL")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        host_var = tk.StringVar(value="db")
        db_var = tk.StringVar(value="mspr")
        user_var = tk.StringVar(value="postgres")
        password_var = tk.StringVar(value="postgres")
        port_var = tk.StringVar(value="5432")
        
        #Frame principal
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Host:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(main_frame, textvariable=host_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(main_frame, text="Database:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(main_frame, textvariable=db_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(main_frame, text="User:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(main_frame, textvariable=user_var, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(main_frame, text="Password:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(main_frame, textvariable=password_var, width=30, show="*").grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(main_frame, text="Port:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(main_frame, textvariable=port_var, width=30).grid(row=4, column=1, padx=10, pady=5)
        
        # Frame pour les boutons
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        # Fonction pour tester la connexion
        def test_connection():
            try:
                from pipelines.load import PostgresConnector
                
                db = PostgresConnector(
                    host=host_var.get(),
                    database=db_var.get(),
                    user=user_var.get(),
                    password=password_var.get(),
                    port=int(port_var.get())
                )
                
                if db.connect():
                    messagebox.showinfo("Succès", "Connexion établie avec succès!")
                    db.disconnect()
                else:
                    messagebox.showerror("Erreur", "Impossible de se connecter à la base de données")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la connexion: {str(e)}")
        
        #Fonction pour charger les donnees
        def load_data():
            try:
                from pipelines.load import PostgresConnector
                
                #Recuperer le chemin du premier fichier transformz
                if not self.pipeline.transformed_datasets:
                    messagebox.showwarning("Attention", "Aucun fichier transformé disponible")
                    return
                    
                first_dataset_key = list(self.pipeline.transformed_datasets.keys())[0]
                first_dataset = self.pipeline.transformed_datasets[first_dataset_key]
                
                #Connexion a PostgreSQL
                db = PostgresConnector(
                    host=host_var.get(),
                    database=db_var.get(),
                    user=user_var.get(),
                    password=password_var.get(),
                    port=int(port_var.get())
                )
                
                if not db.connect():
                    messagebox.showerror("Erreur", "Impossible de se connecter à la base de données")
                    return
                
                self.update_status("Chargement des données dans PostgreSQL...")
                self.root.update()
                
                if db.execute_etl_process(
                    mappings_path="pipelines/mappings.yaml",
                    base_folder=self.output_dir
                ):
                    messagebox.showinfo("Succès", "Données chargées avec succès dans PostgreSQL")
                    # Supprimer le fichier CSV temporaire
                    os.remove(temp_csv_path)
                    self.update_status("Données chargées dans PostgreSQL")
                else:
                    messagebox.showerror("Erreur", "Échec du chargement des données")
                    self.update_status("Erreur lors du chargement dans PostgreSQL")
                
                db.disconnect()
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur inattendue: {str(e)}")
                self.update_status("Erreur lors du chargement dans PostgreSQL")
        
        test_button = tk.Button(button_frame, text="Tester connexion", command=test_connection)
        test_button.pack(side=tk.LEFT, padx=10)
        
        load_button = tk.Button(button_frame, text="Charger dans PostgreSQL", command=load_data)
        configure_button_style(load_button, is_primary=True)
        load_button.pack(side=tk.LEFT, padx=10)