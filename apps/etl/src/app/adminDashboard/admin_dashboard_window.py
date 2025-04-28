import tkinter as tk
from tkinter import ttk, messagebox
import os

# Importer les modules du dashboard
from app.adminDashboard.models import UserManager


class AdminDashboardWindow(tk.Frame):
    def __init__(self, master, language_manager):
        super().__init__(master)
        self.master = master
        self.language_manager = language_manager

        # Available roles and regions for dropdown menus
        self.available_roles = ["admin", "user", "manager", "analyst", "guest"]
        self.available_regions = [
            "global",
            "france",
            "états-unis",
            "allemagne",
            "royaume-uni",
            "espagne",
            "italie",
        ]

        # Language selector
        self.language_frame = tk.Frame(self)
        self.language_frame.pack(anchor="ne", padx=10, pady=5)

        self.language_label = tk.Label(
            self.language_frame, text=self.language_manager.get_text("language")
        )
        self.language_label.pack(side=tk.LEFT, padx=5)

        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(
            self.language_frame,
            textvariable=self.language_var,
            values=["Français", "English", "Español", "Italiano", "Deutsch"],
            width=10,
            state="readonly",
        )

        # Mapping of display names to language codes
        self.language_mapping = {
            "Français": "fr",
            "English": "en",
            "Español": "es",
            "Italiano": "it",
            "Deutsch": "de",
        }

        # Set default language
        language_keys = list(self.language_mapping.keys())
        language_values = list(self.language_mapping.values())
        current_language_index = language_values.index(
            self.language_manager.current_language
        )
        self.language_dropdown.current(current_language_index)

        self.language_dropdown.pack(side=tk.LEFT)
        self.language_dropdown.bind("<<ComboboxSelected>>", self._language_changed)

        self._create_widgets()

    def _language_changed(self, event):
        selected_language = self.language_var.get()
        language_code = self.language_mapping[selected_language]

        if self.language_manager.set_language(language_code):
            # Update UI with new language
            self._update_text()

    def _create_widgets(self):
        # Titre
        self.title_label = tk.Label(
            self,
            text=self.language_manager.get_text("dashboard_title"),
            font=("Arial", 16, "bold"),
        )
        self.title_label.pack(pady=10)

        # Main container (split in two)
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left side - Add user form
        self.left_frame = tk.LabelFrame(
            self.main_container, text=self.language_manager.get_text("add_user_frame")
        )
        self.left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.form_frame = tk.Frame(self.left_frame)
        self.form_frame.pack(pady=10, padx=10, fill="both")

        # Username
        self.username_label = tk.Label(
            self.form_frame, text=self.language_manager.get_text("username")
        )
        self.username_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.new_username = tk.Entry(self.form_frame, width=25)
        self.new_username.grid(row=0, column=1, padx=5, pady=5)

        # Password
        self.password_label = tk.Label(
            self.form_frame, text=self.language_manager.get_text("password")
        )
        self.password_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.new_password = tk.Entry(self.form_frame, show="*", width=25)
        self.new_password.grid(row=1, column=1, padx=5, pady=5)

        # Role (dropdown)
        self.role_label = tk.Label(
            self.form_frame, text=self.language_manager.get_text("role")
        )
        self.role_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.role_var = tk.StringVar()
        self.role_dropdown = ttk.Combobox(
            self.form_frame,
            textvariable=self.role_var,
            values=self.available_roles,
            width=22,
            state="readonly",
        )
        self.role_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.role_dropdown.current(1)  # Default to "user"

        # Region (dropdown)
        self.region_label = tk.Label(
            self.form_frame, text=self.language_manager.get_text("region")
        )
        self.region_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.region_var = tk.StringVar()
        self.region_dropdown = ttk.Combobox(
            self.form_frame,
            textvariable=self.region_var,
            values=self.available_regions,
            width=22,
            state="readonly",
        )
        self.region_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.region_dropdown.current(0)  # Default to "global"

        # Add button
        self.add_button = tk.Button(
            self.form_frame,
            text=self.language_manager.get_text("add_button"),
            command=self._add_user,
        )
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Right side - User list
        self.right_frame = tk.LabelFrame(
            self.main_container, text=self.language_manager.get_text("user_list_frame")
        )
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Treeview for users
        columns = ("login", "role", "region")
        self.user_tree = ttk.Treeview(
            self.right_frame, columns=columns, show="headings"
        )

        # Define headings
        self.user_tree.heading("login", text=self.language_manager.get_text("user_col"))
        self.user_tree.heading("role", text=self.language_manager.get_text("role_col"))
        self.user_tree.heading(
            "region", text=self.language_manager.get_text("region_col")
        )

        # Define columns
        self.user_tree.column("login", width=120)
        self.user_tree.column("role", width=100)
        self.user_tree.column("region", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.right_frame, orient="vertical", command=self.user_tree.yview
        )
        self.user_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.user_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Button frame
        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.pack(pady=10, fill="x")

        # Delete button
        self.delete_button = tk.Button(
            self.button_frame,
            text=self.language_manager.get_text("delete_button"),
            command=self._delete_user,
        )
        self.delete_button.pack(side="left", padx=5)

        # Refresh button
        self.refresh_button = tk.Button(
            self.button_frame,
            text=self.language_manager.get_text("refresh_button"),
            command=self._refresh_user_list,
        )
        self.refresh_button.pack(side="right", padx=5)

        # Bottom button frame (pour le bouton de retour)
        self.bottom_button_frame = tk.Frame(self)
        self.bottom_button_frame.pack(fill="x", pady=10, padx=10)

        # Charger la liste des utilisateurs
        self.user_manager = UserManager()
        self._refresh_user_list()

    def _update_text(self):
        # Update all text elements with current language
        self.title_label.config(text=self.language_manager.get_text("dashboard_title"))
        self.left_frame.config(text=self.language_manager.get_text("add_user_frame"))
        self.username_label.config(text=self.language_manager.get_text("username"))
        self.password_label.config(text=self.language_manager.get_text("password"))
        self.role_label.config(text=self.language_manager.get_text("role"))
        self.region_label.config(text=self.language_manager.get_text("region"))
        self.add_button.config(text=self.language_manager.get_text("add_button"))
        self.right_frame.config(text=self.language_manager.get_text("user_list_frame"))
        self.delete_button.config(text=self.language_manager.get_text("delete_button"))
        self.refresh_button.config(
            text=self.language_manager.get_text("refresh_button")
        )
        self.language_label.config(text=self.language_manager.get_text("language"))

        # Update treeview headers
        self.user_tree.heading("login", text=self.language_manager.get_text("user_col"))
        self.user_tree.heading("role", text=self.language_manager.get_text("role_col"))
        self.user_tree.heading(
            "region", text=self.language_manager.get_text("region_col")
        )

        # Refresh the list to update displayed data
        self._refresh_user_list()

    def _add_user(self):
        login = self.new_username.get()
        password = self.new_password.get()
        role = self.role_var.get()
        region = self.region_var.get()

        # Vérification de la longueur du login et du mot de passe
        if len(login) > 100 or len(password) > 100:
            messagebox.showwarning(
                self.language_manager.get_text("warning"),
                self.language_manager.get_text("max_length_exceeded"),
            )
            return

        if not login or not password:
            messagebox.showwarning(
                self.language_manager.get_text("warning"),
                self.language_manager.get_text("fill_all_fields"),
            )
            return

        if self.user_manager.add_user(login, password, role, region):
            messagebox.showinfo(
                self.language_manager.get_text("success"),
                self.language_manager.get_text("user_added", login=login),
            )
            self._refresh_user_list()

            # Clear form
            self.new_username.delete(0, tk.END)
            self.new_password.delete(0, tk.END)

    def _delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showinfo(
                self.language_manager.get_text("info"),
                self.language_manager.get_text("select_user_delete"),
            )
            return

        login = self.user_tree.item(selected_item[0], "values")[0]

        if messagebox.askyesno(
            self.language_manager.get_text("info"),
            self.language_manager.get_text("confirm_delete", login=login),
        ):
            # Récupérer l'ID utilisateur à partir du login
            user_info = self.user_manager.get_user_info(login)
            if user_info and self.user_manager.delete_user(user_info["id"]):
                messagebox.showinfo(
                    self.language_manager.get_text("success"),
                    self.language_manager.get_text("user_deleted", login=login),
                )
                self._refresh_user_list()

    def _refresh_user_list(self):
        # Clear the tree
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        # Add all users except admin
        for user in self.user_manager.get_all_users():
            self.user_tree.insert(
                "", tk.END, values=(user.username, user.role, user.region)
            )
