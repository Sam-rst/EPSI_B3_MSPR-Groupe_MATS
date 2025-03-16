import tkinter as tk

from ui.styles import (
    LIGHT_BG_COLOR, BORDER_COLOR, BORDER_THICKNESS,
    ITEM_BG_COLOR, ITEM_FONT, ITEM_FONT_BOLD,
    ITEM_PADDING_X, ITEM_PADDING_Y
)

class FileListPanel:
    def __init__(self, parent, on_remove=None):
        self.parent = parent
        self.on_remove = on_remove
        
        # Création du cadre principal
        self.frame = tk.Frame(
            parent,
            bg=LIGHT_BG_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=BORDER_THICKNESS
        )
        self.frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Container pour les entrées de fichiers
        self.files_container = tk.Frame(self.frame, bg=LIGHT_BG_COLOR)
        self.files_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_file_list(self, file_list):
        # Effacer l'affichage actuel
        for widget in self.files_container.winfo_children():
            widget.destroy()
        
        # Afficher chaque fichier
        for i, file_info in enumerate(file_list):
            file_frame = self._create_file_entry(file_info, i)
            file_frame.pack(fill=tk.X, pady=2)
    
    def _create_file_entry(self, file_info, index):
        # Cadre pour un fichier avec fond gris clair arrondi
        file_frame = tk.Frame(self.files_container, bg=ITEM_BG_COLOR, padx=ITEM_PADDING_X, pady=ITEM_PADDING_Y)
        
        # Nom du fichier
        name_label = tk.Label(
            file_frame,
            text=file_info.name,
            font=ITEM_FONT,
            bg=ITEM_BG_COLOR,
            fg="#000000",
            width=30,
            anchor="w"
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
            anchor="w"
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
            anchor="w"
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
            anchor="e"
        )
        size_label.pack(side=tk.LEFT, padx=10)
        
        # Case à cocher
        check_var = tk.BooleanVar(value=file_info.selected)
        check = tk.Checkbutton(
            file_frame,
            variable=check_var,
            bg=ITEM_BG_COLOR,
            activebackground=ITEM_BG_COLOR,
            command=lambda: self._toggle_selection(index, check_var.get())
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
            cursor="hand2"
        )
        delete_button.pack(side=tk.LEFT, padx=10)
        
        return file_frame
    
    def _toggle_selection(self, index, is_selected):
        # Cette méthode serait plus utile si FileListPanel avait accès à la liste
        # Pour l'instant, elle est principalement un placeholder
        pass
    
    def _remove_file(self, index):
        if self.on_remove:
            self.on_remove(index)