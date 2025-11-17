"""
config.py - Instellingen en configuratie voor de Sinterklaas game
"""

import os

# ========== TTS (Text-to-Speech) INSTELLINGEN ==========
TTS_ENABLED = True
TTS_LANG = "nl"
TTS_VOICE = "mb-nl2"  # MBROLA Nederlands
TTS_REPEAT_KEY = "r"  # Druk 'r' om vraag te herhalen
TTS_SPEED = 150       # Spreeksnelheid (woorden per minuut)

# ========== SPEL INSTELLINGEN ==========
DIFFICULTY_LEVELS = ["Makkelijk", "Normaal", "Moeilijk"]
DEFAULT_DIFFICULTY = "Normaal"

DEFAULT_NUM_QUESTIONS = 10

# ========== PUNTENTELLING ==========
POINTS_PER_QUESTION = {
    "Makkelijk": 1,
    "Normaal": 2,
    "Moeilijk": 3,
}

# Bonus punten voor snelle antwoorden
SPEED_BONUS_ENABLED = False
TIME_LIMIT_SECONDS = 30  # Per vraag

# ========== ANSI KLEUREN ==========
COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "DIM": "\033[2m",
    "ITALIC": "\033[3m",
    "UNDERLINE": "\033[4m",
    
    # Voorgronkleuren
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    
    # Heldere versies
    "BRIGHT_RED": "\033[1;31m",
    "BRIGHT_GREEN": "\033[1;32m",
    "BRIGHT_YELLOW": "\033[1;33m",
    "BRIGHT_BLUE": "\033[1;34m",
    "BRIGHT_MAGENTA": "\033[1;35m",
    "BRIGHT_CYAN": "\033[1;36m",
    "BRIGHT_WHITE": "\033[1;37m",
}

# ========== BESTANDSPADEN ==========
# CSV met vragen
QUESTIONS_CSV = os.path.join(
    os.path.dirname(__file__),
    "vragen.csv"
)

# Score history (optioneel)
SCORES_FILE = os.path.join(
    os.path.dirname(__file__),
    "scores.json"
)

# ========== CADEAU INSTELLINGEN ==========
GIFT_MIN_PERCENTAGE = 70  # Minimum percentage om cadeau te verdienen
GIFTS_ENABLED = True      # Cadeaus aan/uit

# ========== MINIGAMES INSTELLINGEN ==========
MINIGAMES = {
    "roulette": {
        "enabled": True,
        "description": "Gok een willekeurige vraag uit alle niveaus!",
        "chances": 3,
    },
    "opdracht": {
        "enabled": True,
        "description": "Voer een grappige opdracht uit van Sint!",
    },
    "soundboard": {
        "enabled": True,
        "description": "Luister naar grappige boodschappen van Sint!",
    },
}

# ========== TERMINAL INSTELLINGEN ==========
# Ondersteunt Ctrl+C gracefully
ALLOW_KEYBOARD_INTERRUPT = True

# Scherm breedte (voor ASCII art)
SCREEN_WIDTH = 60
