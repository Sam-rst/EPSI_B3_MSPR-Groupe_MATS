import tkinter as tk
from ui.main_window import MainWindow
from config import APP_TITLE, DEFAULT_SIZE

# Gestion du drag & drop
try:
    from tkinterdnd2 import TkinterDnD
    has_dnd = True
except ImportError:
    has_dnd = False
    print("tkinterdnd2 n'est pas installé. Le glisser-déposer ne sera pas disponible.")

def main():
    if has_dnd:
        root = TkinterDnD.Tk()  # Utiliser TkinterDnD.Tk au lieu de tk.Tk
    else:
        root = tk.Tk()
        
    root.title(APP_TITLE)
    root.geometry(DEFAULT_SIZE)
    
    # Création de la fenêtre principale
    app = MainWindow(root)
    
    # Démarrage de l'application
    root.mainloop()

if __name__ == "__main__":
    main()

def main():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(DEFAULT_SIZE)
    
    app = MainWindow(root)
    
    # Démarrage de l'application
    root.mainloop()

if __name__ == "__main__":
    main()