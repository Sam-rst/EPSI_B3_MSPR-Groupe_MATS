import tkinter as tk
from ui.main_window import MainWindow
from configapp import APP_TITLE, DEFAULT_SIZE, MIN_WIDTH, MIN_HEIGHT

# Gestion du drag & drop
try:
    from tkinterdnd2 import TkinterDnD
    has_dnd = True
except ImportError:
    has_dnd = False
    print("tkinterdnd2 n'est pas installé. Le glisser-déposer ne sera pas disponible.")

def main():
    if has_dnd:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
        
    root.title(APP_TITLE)
    root.geometry(DEFAULT_SIZE)
    
    # Définir la taille minimale de la fenêtre
    root.minsize(MIN_WIDTH, MIN_HEIGHT)
    
    # Configurer le redimensionnement
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    app = MainWindow(root)
    
    # Démarrage de l'application
    root.mainloop()

if __name__ == "__main__":
    main()