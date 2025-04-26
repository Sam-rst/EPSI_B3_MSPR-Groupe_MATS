import tkinter as tk

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


class FileListPanel:

    def __init__(self, parent, on_remove=None):
        self.parent = parent
        self.on_remove = on_remove

        self.frame = tk.Frame(
            parent,
            bg=LIGHT_BG_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=BORDER_THICKNESS,
        )
        self.frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Container pour les entrees de fichiers
        self.canvas = tk.Canvas(self.frame, bg=LIGHT_BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            self.frame, orient="vertical", command=self.canvas.yview
        )
        self.files_container = tk.Frame(self.canvas, bg=LIGHT_BG_COLOR)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.files_container, anchor="nw"
        )

        # Gestion du responsive responsive
        self.files_container.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def update_file_list(self, file_list):
        # Effacer l'affichage actuel
        for widget in self.files_container.winfo_children():
            widget.destroy()

        # Afficher chaque fichier
        for i, file_info in enumerate(file_list):
            file_frame = self._create_file_entry(file_info, i)
            file_frame.pack(fill=tk.X, padx=5, pady=2)

    def _create_file_entry(self, file_info, index):
        file_frame = tk.Frame(self.files_container, bg=ITEM_BG_COLOR)

        # Utiliser Grid pour un layout responsive
        file_frame.columnconfigure(0, weight=3)  # Nom du fichier
        file_frame.columnconfigure(1, weight=1)  # Type de fichier
        file_frame.columnconfigure(2, weight=1)  # Date
        file_frame.columnconfigure(3, weight=1)  # Taille
        file_frame.columnconfigure(4, weight=0, minsize=30)  # Checkbox
        file_frame.columnconfigure(5, weight=0, minsize=30)  # Bouton X

        # Nom du fichier
        name_label = tk.Label(
            file_frame,
            text=file_info.name,
            font=ITEM_FONT,
            bg=ITEM_BG_COLOR,
            fg="#000000",
            anchor="w",
            padx=5,
        )
        name_label.grid(row=0, column=0, sticky="ew", pady=ITEM_PADDING_Y)

        ext_label = tk.Label(
            file_frame,
            text=file_info.format_display,
            font=ITEM_FONT_BOLD,
            bg=ITEM_BG_COLOR,
            fg=file_info.format_color,
            anchor="w",
        )
        ext_label.grid(row=0, column=1, sticky="ew", pady=ITEM_PADDING_Y)

        # Date du fichier
        date_label = tk.Label(
            file_frame,
            text=file_info.date_display,
            font=ITEM_FONT,
            bg=ITEM_BG_COLOR,
            fg="#000000",
            anchor="w",
        )
        date_label.grid(row=0, column=2, sticky="ew", pady=ITEM_PADDING_Y)

        # Taille du fichier
        size_label = tk.Label(
            file_frame,
            text=f"{file_info.size_kb} Ko",
            font=ITEM_FONT_BOLD,
            bg=ITEM_BG_COLOR,
            fg=file_info.size_color,
            anchor="e",
        )
        size_label.grid(row=0, column=3, sticky="ew", pady=ITEM_PADDING_Y)

        # Case a cocher
        check_var = tk.BooleanVar(value=file_info.selected)
        check = tk.Checkbutton(
            file_frame,
            variable=check_var,
            bg=ITEM_BG_COLOR,
            activebackground=ITEM_BG_COLOR,
            command=lambda: self._toggle_selection(index, check_var.get()),
        )
        check.grid(row=0, column=4, padx=5, pady=ITEM_PADDING_Y)

        # Bouton de suppression (X), fixe a droite
        delete_button = tk.Button(
            file_frame,
            text="✕",
            font=ITEM_FONT_BOLD,
            fg="red",
            bg=ITEM_BG_COLOR,
            bd=0,
            width=2,  # Largeur fixe pour garantir la visibilité
            command=lambda idx=index: self._remove_file(idx),
            cursor="hand2",
        )
        delete_button.grid(row=0, column=5, padx=5, pady=ITEM_PADDING_Y)

        return file_frame

    def _toggle_selection(self, index, is_selected):
        pass

    def _remove_file(self, index):
        if self.on_remove:
            self.on_remove(index)
