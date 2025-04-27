import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime

from ui.styles import (
    LIGHT_BG_COLOR,
    BORDER_COLOR,
    BORDER_THICKNESS,
    ITEM_BG_COLOR,
    ITEM_FONT,
    ITEM_FONT_BOLD,
    ITEM_PADDING_X,
    ITEM_PADDING_Y,
)


class FileInfo:
    """Classe pour stocker les informations sur un fichier"""

    def __init__(self, path, selected=True):
        self.path = path
        self.name = os.path.basename(path)
        self.format = os.path.splitext(path)[1].lower()
        self.selected = selected

        # Obtenir la taille du fichier
        try:
            self.size_kb = round(os.path.getsize(path) / 1024, 1)
        except:
            self.size_kb = 0

        # Obtenir la date de modification
        try:
            mtime = os.path.getmtime(path)
            self.date = datetime.fromtimestamp(mtime)
            self.date_display = self.date.strftime("%d/%m/%Y")
        except:
            self.date = None
            self.date_display = "Unknown"

        # Formater l'affichage selon le type de fichier
        if self.format.lower() in [".csv", "csv"]:
            self.format_display = "CSV"
            self.format_color = "#007bff"  # Bleu
        else:
            self.format_display = self.format.upper().replace(".", "")
            self.format_color = "#6c757d"  # Gris

        # Couleur selon la taille
        if self.size_kb < 100:
            self.size_color = "#28a745"  # Vert
        elif self.size_kb < 1000:
            self.size_color = "#ffc107"  # Jaune
        else:
            self.size_color = "#dc3545"  # Rouge


class FileListPanel:
    def __init__(self, parent, on_remove=None, on_selection_change=None):
        self.parent = parent
        self.on_remove = on_remove
        self.on_selection_change = on_selection_change
        self.file_list = []

        # Création du cadre principal
        self.frame = tk.Frame(
            parent,
            bg=LIGHT_BG_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=BORDER_THICKNESS,
        )
        self.frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Créer un frame pour la liste avec scrollbar
        list_frame = tk.Frame(self.frame, bg=LIGHT_BG_COLOR)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar verticale
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas pour contenir les widgets avec scrolling
        self.canvas = tk.Canvas(
            list_frame, bg=LIGHT_BG_COLOR, yscrollcommand=scrollbar.set
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuration de la scrollbar
        scrollbar.config(command=self.canvas.yview)

        # Container pour les entrées de fichiers
        self.files_container = tk.Frame(self.canvas, bg=LIGHT_BG_COLOR)
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.files_container,
            anchor="nw",
            tags="files_container",
            width=self.canvas.winfo_width(),
        )

        # Mettre à jour la largeur du container lorsque le canvas change de taille
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.files_container.bind("<Configure>", self._on_container_configure)

        # Permettre le défilement avec la molette de la souris
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        # Ajuster la largeur du container à celle du canvas
        self.canvas.itemconfig("files_container", width=event.width)

    def _on_container_configure(self, event):
        # Mettre à jour la région de défilement lorsque le contenu change
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        # Faire défiler avec la molette de la souris (compatible avec Windows)
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_files(self, file_paths):
        """Ajoute des fichiers à la liste"""
        # Filtrer pour ne conserver que les fichiers CSV
        csv_paths = [path for path in file_paths if path.lower().endswith(".csv")]

        for path in csv_paths:
            # Vérifier si le fichier est déjà dans la liste
            if not any(file_info.path == path for file_info in self.file_list):
                self.file_list.append(FileInfo(path))

        self.update_file_list()
        return self.file_list

    def update_file_list(self):
        """Met à jour l'affichage de la liste des fichiers"""
        # Effacer l'affichage actuel
        for widget in self.files_container.winfo_children():
            widget.destroy()

        # Afficher chaque fichier
        for i, file_info in enumerate(self.file_list):
            file_frame = self._create_file_entry(file_info, i)
            file_frame.pack(fill=tk.X, pady=2, padx=5)

        # Mettre à jour le canvas pour ajuster la région de défilement
        self.files_container.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _create_file_entry(self, file_info, index):
        # Cadre pour un fichier avec fond gris clair arrondi
        file_frame = tk.Frame(
            self.files_container,
            bg=ITEM_BG_COLOR,
            padx=ITEM_PADDING_X,
            pady=ITEM_PADDING_Y,
        )

        # Nom du fichier
        name_label = tk.Label(
            file_frame,
            text=file_info.name,
            font=ITEM_FONT,
            bg=ITEM_BG_COLOR,
            fg="#000000",
            width=30,
            anchor="w",
        )
        name_label.pack(side=tk.LEFT, padx=(5, 10))

        # Type de fichier (CSV ou XLSX avec couleur)
        ext_label = tk.Label(
            file_frame,
            text=file_info.format_display,
            font=ITEM_FONT_BOLD,
            bg=ITEM_BG_COLOR,
            fg=file_info.format_color,
            width=6,
            anchor="w",
        )
        ext_label.pack(side=tk.LEFT, padx=10)

        # Date du fichier
        date_label = tk.Label(
            file_frame,
            text=file_info.date_display,
            font=ITEM_FONT,
            bg=ITEM_BG_COLOR,
            fg="#000000",
            width=12,
            anchor="w",
        )
        date_label.pack(side=tk.LEFT, padx=10)

        # Taille du fichier
        size_label = tk.Label(
            file_frame,
            text=f"{file_info.size_kb} Ko",
            font=ITEM_FONT_BOLD,
            bg=ITEM_BG_COLOR,
            fg=file_info.size_color,
            width=10,
            anchor="e",
        )
        size_label.pack(side=tk.LEFT, padx=10)

        # Case à cocher
        check_var = tk.BooleanVar(value=file_info.selected)
        check = tk.Checkbutton(
            file_frame,
            variable=check_var,
            bg=ITEM_BG_COLOR,
            activebackground=ITEM_BG_COLOR,
            command=lambda: self._toggle_selection(index, check_var.get()),
        )
        check.pack(side=tk.LEFT, padx=10)

        # Bouton de suppression (X)
        delete_button = tk.Button(
            file_frame,
            text="✕",
            font=ITEM_FONT_BOLD,
            fg="red",
            bg=ITEM_BG_COLOR,
            bd=0,
            command=lambda idx=index: self._remove_file(idx),
            cursor="hand2",
        )
        delete_button.pack(side=tk.LEFT, padx=10)

        return file_frame

    def _toggle_selection(self, index, is_selected):
        """Change l'état de sélection d'un fichier"""
        if 0 <= index < len(self.file_list):
            self.file_list[index].selected = is_selected
            if self.on_selection_change:
                self.on_selection_change(self.file_list)

    def _remove_file(self, index):
        """Supprime un fichier de la liste"""
        if 0 <= index < len(self.file_list):
            del self.file_list[index]
            self.update_file_list()
            if self.on_remove:
                self.on_remove(index)

    def get_selected_files(self):
        """Renvoie la liste des fichiers sélectionnés"""
        return [file_info for file_info in self.file_list if file_info.selected]
