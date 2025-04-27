import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime

from ui.styles import (
    MAIN_BG_COLOR,
    TITLE_FONT,
    BUTTON_FONT,
    LABEL_FONT_ITALIC,
    ACCENT_COLOR,
    LIGHT_BG_COLOR,
    BORDER_COLOR,
    BORDER_THICKNESS,
    configure_button_style,
)
from ui.file_list import FileListPanel
from models.file_info import FileInfo

# Import pour le drag & drop
try:
    from tkinterdnd2 import DND_FILES

    has_dnd = True
except ImportError:
    has_dnd = False


class UploadPanel:
    def __init__(self, parent, status_callback=None):
        self.parent = parent
        self.status_callback = status_callback
        self.selected_files = []

        # Création du panneau
        self.frame = tk.Frame(parent, bg=MAIN_BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Initialisation de l'interface
        self._setup_ui()

    def _setup_ui(self):
        # Titre principal
        title_label = tk.Label(
            self.frame,
            text="Upload de CSV ou Excel",
            font=TITLE_FONT,
            bg=MAIN_BG_COLOR,
            fg="#000000",
        )
        title_label.pack(pady=(80, 20))

        # Zone de dépôt (drop zone) avec style arrondi
        self.drop_frame = tk.LabelFrame(
            self.frame,
            text="",
            bg=LIGHT_BG_COLOR,
            width=300,
            height=100,
            highlightbackground=ACCENT_COLOR,
            highlightthickness=2,
            bd=0,
        )
        self.drop_frame.pack(pady=10)
        self.drop_frame.pack_propagate(False)  # Maintient la taille fixe

        # Label dans la zone de dépôt
        self.drop_label = tk.Label(
            self.drop_frame,
            text="DROP or SELECT",
            font=BUTTON_FONT,
            bg=LIGHT_BG_COLOR,
            fg=ACCENT_COLOR,
            cursor="hand2",
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True)

        # Configurer le drag & drop si disponible
        if has_dnd:
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind("<<Drop>>", self._on_drop)
            self.drop_label.drop_target_register(DND_FILES)
            self.drop_label.dnd_bind("<<Drop>>", self._on_drop)

        # Clic sur la zone pour ouvrir la boîte de dialogue
        self.drop_frame.bind("<Button-1>", lambda e: self._select_files())
        self.drop_label.bind("<Button-1>", lambda e: self._select_files())

        # Effets visuels pour le hover
        self.drop_frame.bind("<Enter>", self._on_drop_area_hover)
        self.drop_label.bind("<Enter>", self._on_drop_area_hover)
        self.drop_frame.bind("<Leave>", self._on_drop_area_leave)
        self.drop_label.bind("<Leave>", self._on_drop_area_leave)

        # Section "Fichiers sélectionnés"
        files_label = tk.Label(
            self.frame,
            text="Fichier sélectionnés",
            font=LABEL_FONT_ITALIC,
            bg=MAIN_BG_COLOR,
            fg="#000000",
            anchor="w",
        )
        files_label.pack(anchor="w", pady=(20, 5))

        # Panneau de liste de fichiers
        self.file_list_panel = FileListPanel(self.frame, on_remove=self._remove_file)

        # Initialiser la liste vide
        self.file_list_panel.update_file_list([])

    def _on_drop_area_hover(self, event):
        self.drop_frame.config(highlightbackground="#3A6CFF")
        self.drop_label.config(fg="#3A6CFF")

    def _on_drop_area_leave(self, event):
        self.drop_frame.config(highlightbackground=ACCENT_COLOR)
        self.drop_label.config(fg=ACCENT_COLOR)

    def _on_drop(self, event):
        # Récupérer les chemins de fichiers
        file_paths = self.drop_frame.tk.splitlist(event.data)

        # Effet visuel pour confirmer le dépôt
        self.drop_frame.config(highlightbackground="#4CAF50")  # Vert pour succès
        self.drop_label.config(fg="#4CAF50")
        self.drop_frame.after(
            1000, lambda: self.drop_frame.config(highlightbackground=ACCENT_COLOR)
        )
        self.drop_label.after(1000, lambda: self.drop_label.config(fg=ACCENT_COLOR))

        # Ajouter les fichiers
        self._add_files_to_list(file_paths)

    def _select_files(self):
        filetypes = [
            ("Fichiers de données", "*.csv *.xlsx *.xls"),
            ("Fichiers CSV", "*.csv"),
            ("Fichiers Excel", "*.xlsx *.xls"),
        ]

        files = filedialog.askopenfilenames(
            title="Sélectionner les fichiers à analyser", filetypes=filetypes
        )

        if files:
            self._add_files_to_list(files)

    def _add_files_to_list(self, file_paths):
        added_count = 0

        for file_path in file_paths:
            # Pour Windows: enlever les accolades que dnd peut ajouter
            file_path = file_path.strip("{}")

            # Vérifier si c'est un CSV ou Excel
            ext = os.path.splitext(file_path)[1].lower()
            if ext in [".csv", ".xlsx", ".xls"]:
                file_info = FileInfo(file_path)
                self.selected_files.append(file_info)
                added_count += 1

        if added_count > 0:
            # Mettre à jour l'affichage
            self.file_list_panel.update_file_list(self.selected_files)

            # Mettre à jour le statut
            if self.status_callback:
                self.status_callback(f"{added_count} fichier(s) ajouté(s)")

    def _remove_file(self, index):
        if 0 <= index < len(self.selected_files):
            del self.selected_files[index]
            self.file_list_panel.update_file_list(self.selected_files)

            # Mettre à jour le statut
            if self.status_callback:
                self.status_callback(
                    f"Fichier retiré. {len(self.selected_files)} fichier(s) restant(s)"
                )
