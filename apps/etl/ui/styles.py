# Couleurs principales
MAIN_BG_COLOR = "#C5D5F0"
ACCENT_COLOR = "#4A7CFF"
TEXT_COLOR = "#000000"
LIGHT_BG_COLOR = "#FFFFFF"
ITEM_BG_COLOR = "#EEEEEE"

# Bordures
BORDER_COLOR = "#CCCCCC"
BORDER_THICKNESS = 1 

# Polices
TITLE_FONT = ("Arial", 30, "bold")
SUBTITLE_FONT = ("Arial", 14, "bold")
BUTTON_FONT = ("Arial", 12, "bold")
LABEL_FONT = ("Arial", 12)
LABEL_FONT_ITALIC = ("Arial", 12, "italic")
ITEM_FONT = ("Arial", 11)
ITEM_FONT_BOLD = ("Arial", 11, "bold")

# Dimensions
BUTTON_PADDING_X = 20
BUTTON_PADDING_Y = 5
ITEM_PADDING_X = 10
ITEM_PADDING_Y = 8

# Styles pour les boutons
def configure_button_style(button, is_primary=True):
    if is_primary:
        button.configure(
            font=BUTTON_FONT,
            bg=ACCENT_COLOR,
            fg="white",
            padx=BUTTON_PADDING_X,
            pady=BUTTON_PADDING_Y,
            relief="flat",  # Style plat pour plus de modernité
            borderwidth=0,
            activebackground="#3A6CFF",
            activeforeground="white",
            cursor="hand2"
        )
    else:
        button.configure(
            font=BUTTON_FONT,
            bg="#F0F0F0",
            fg=TEXT_COLOR,
            padx=BUTTON_PADDING_X,
            pady=BUTTON_PADDING_Y,
            relief="flat",
            borderwidth=0,
            activebackground="#E0E0E0",
            activeforeground=TEXT_COLOR,
            cursor="hand2"
        )

# Fonction pour créer un bouton arrondi via Canvas
def create_rounded_button(canvas, x, y, width, height, radius, fill_color, text, command):
    # Points pour créer un polygone arrondi
    x1, y1 = x, y
    x2, y2 = x + width, y + height
    
    # Dessiner un rectangle avec des coins arrondis
    button_bg = canvas.create_polygon(
        x1+radius, y1,
        x2-radius, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2-radius,
        x1, y1+radius,
        fill=fill_color,
        outline=fill_color,
        smooth=True,
        tags="button_bg"
    )
    
    # Ajouter le texte
    button_text = canvas.create_text(
        x + width/2, y + height/2,
        text=text,
        fill="white",
        font=BUTTON_FONT,
        tags="button_text"
    )
    
    # Ajouter les gestionnaires d'événements
    canvas.tag_bind("button_bg", "<Button-1>", lambda e: command())
    canvas.tag_bind("button_text", "<Button-1>", lambda e: command())
    
    # Effet de survol
    canvas.tag_bind("button_bg", "<Enter>", 
                  lambda e: canvas.itemconfig("button_bg", fill="#3A6CFF"))
    canvas.tag_bind("button_text", "<Enter>", 
                  lambda e: canvas.itemconfig("button_bg", fill="#3A6CFF"))
    canvas.tag_bind("button_bg", "<Leave>", 
                  lambda e: canvas.itemconfig("button_bg", fill=fill_color))
    canvas.tag_bind("button_text", "<Leave>", 
                  lambda e: canvas.itemconfig("button_bg", fill=fill_color))
    
    return (button_bg, button_text)